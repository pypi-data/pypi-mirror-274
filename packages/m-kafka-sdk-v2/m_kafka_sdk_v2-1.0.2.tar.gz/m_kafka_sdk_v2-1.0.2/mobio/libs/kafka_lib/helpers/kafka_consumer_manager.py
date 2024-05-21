import json
from abc import abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta
from confluent_kafka.cimpl import KafkaError, KafkaException, Consumer
from mobio.libs.kafka_lib import RequeueStatus, KAFKA_BOOTSTRAP
from mobio.libs.kafka_lib.helpers import consumer_warning_slack
from mobio.libs.kafka_lib.models.mongo.requeue_consumer_model import (
    RequeueConsumerModel,
)
from time import time, sleep
from uuid import uuid4
import os
import pathlib
try:
    from mobio.libs.logging import MobioLogging
    m_log = MobioLogging()
except:
    import logging as MobioLogging
    m_log = MobioLogging


def commit_completed(err, partitions):
    if err:
        m_log.error(str(err))
    else:
        m_log.info("Committed partition offsets: " + str(partitions))


class BaseKafkaConsumer:
    def __init__(
        self,
        topic_name: object,
        group_id: object,
        client_mongo,
        retryable=True,
        session_timeout_ms=15000,
        bootstrap_server=None,
        consumer_config=None,
        lst_subscribe_topic=None,
        retry_topic=None,
        enable_bloom=False,
        auto_commit=True,
        redis_client=None
    ):
        self.client_id = str(uuid4())
        self.group_id = group_id
        self.lst_subscribe_topic = (
            lst_subscribe_topic if lst_subscribe_topic else [topic_name]
        )
        self.retry_topic = retry_topic if retry_topic else self.lst_subscribe_topic[0]
        config = {
            "bootstrap.servers": KAFKA_BOOTSTRAP
            if not bootstrap_server
            else bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": "latest",
            "session.timeout.ms": session_timeout_ms,
            "client.id": self.client_id,
            "error_cb": self.error_cb,
            "enable.auto.commit": "false" if not auto_commit else "true",
        }
        if not auto_commit:
            config["on_commit"] = commit_completed
        if consumer_config:
            config.update(consumer_config)
        self.c = Consumer(config)
        self.client_mongo = client_mongo
        self.retryable = retryable
        self.lst_processed_msg = []
        self.last_time_commit = time()
        self.st_mtime = None
        self.default_commit_time = 5

        try:
            self.c.subscribe(self.lst_subscribe_topic)
            m_log.info("start consumer with config: {}".format(config))

            # Add mapping client-id kafka and pod name
            # Lưu file consumer theo group
            DATA_DIR = os.environ.get("APPLICATION_DATA_DIR")
            folder_path = "{}/{}/{}".format(
                DATA_DIR, "kafka-liveness-consumer", group_id
            )
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # Add mapping client-id kafka and pod name
            file_path = "{folder_path}/{client_id}".format(
                folder_path=folder_path, client_id=self.client_id
            )
            # Save relationship pods and topic
            host_name = os.environ.get("HOSTNAME")
            f = open(file_path, "w")
            pod_data_info = "{host_name}".format(host_name=host_name)
            f.write(pod_data_info)
            f.close()

            # PATHLIB for control pod maintain
            pull_message_status_path = "/tmp/consumer_pull_message_status"
            if not os.path.exists(pull_message_status_path):
                fs = open(pull_message_status_path, "w")
                fs.write("")
                fs.close()
            self.pl = pathlib.Path(pull_message_status_path)

            if enable_bloom:
                from mobio.libs.kafka_lib.helpers.redisbloom_client import RedisBloomClient
                self.redis_bloom = RedisBloomClient(redis_client=redis_client)
                for t in self.lst_subscribe_topic:
                    self.redis_bloom.init_bloom_filter(
                        topic=t,
                        group=str(self.group_id),
                        capacity=666666,
                        error_rate=0.001,
                    )
            while True:
                if self.is_maintain():
                    if not auto_commit and self.lst_processed_msg:
                        self.manual_commit()
                    sleep(self.default_commit_time)
                    m_log.warning("System is Maintenance !!! Feel free and drink some tea. :)")
                    continue
                msg = self.c.poll(1.0)
                if msg is None:
                    if not auto_commit and self.lst_processed_msg:
                        self.manual_commit()
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        m_log.warning(
                            "%% %s [%d] reached end at offset %d\n"
                            % (msg.topic(), msg.partition(), msg.offset())
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    try:
                        start_time = time()
                        if enable_bloom:
                            self.pre_process_message_with_bloom(
                                msg=msg, auto_commit=auto_commit
                            )
                        else:
                            self.pre_process_message(msg=msg, auto_commit=auto_commit)

                        end_time = time()
                        m_log.info(
                            "end: {} with total time: '[{:.3f}s]".format(
                                self.lst_subscribe_topic, end_time - start_time
                            )
                        )
                    except Exception as e:
                        m_log.error(
                            "MessageQueue::run - topic: {} ERR: {}".format(
                                self.lst_subscribe_topic, e
                            )
                        )
        except RuntimeError as e:
            m_log.error(
                "something unexpected happened: {}: {}".format(
                    self.lst_subscribe_topic, e
                )
            )
        except KafkaException as e:
            m_log.error("KafkaException: {}: {}".format(self.lst_subscribe_topic, e))
        finally:
            m_log.error("consumer is stopped")
            self.c.close()
            consumer_warning_slack(
                pod_name=os.environ.get("HOSTNAME"),
                group_id=self.group_id,
                pretext="Consumer closed",
            )
            # sleep(30)
            raise Exception("Consumer closed")

    def manual_commit(self):
        now = time()
        if (now - self.last_time_commit >= self.default_commit_time and self.lst_processed_msg) or len(
            self.lst_processed_msg
        ) == 150:
            # raise Exception("break commit :)")
            self.c.commit(asynchronous=True)
            m_log.info(f"commit: {len(self.lst_processed_msg)} message")
            self.last_time_commit = now
            del self.lst_processed_msg
            self.lst_processed_msg = []

    def pre_process_message(self, msg, auto_commit=False):
        try:
            key = msg.key()
            message = msg.value().decode("utf-8")
            payload = json.loads(message)
            self.process(payload, key)
            if not auto_commit:
                self.lst_processed_msg.append(int(f"{msg.partition()}{msg.offset()}"))
                self.manual_commit()
        except Exception as e:
            m_log.error(
                "MessageQueue::run - topic: {} ERR: {}".format(
                    self.lst_subscribe_topic, e
                )
            )

    def check_msg_is_processed(self, payload: dict) -> bool:
        """
        Function cần overwrite lại nếu sử dụng bloom_filter,
        ở đây các pod xử lý logic code để check db xem message này đã được xử lý hay chưa.
        Vì Bloom Filter chỉ có thể đảm bảo được rằng message thật sự chưa tồn tại,
        còn với tình huống báo là tồn tại thì rất có thể là cảnh báo sai.
        Lúc này cần check các case cảnh báo sai, còn các case báo là chưa tồn tại thì có thể yên tâm là thật sự chưa tồn tại.

        :param payload: kafka message cần check xem đã được xử lý chưa.
        :return: True nếu muốn bỏ qua không xử lý lại message, False thì message sẽ được đưa vào function process để xử lý
        """
        return True

    def pre_process_message_with_bloom(self, msg, auto_commit=False):
        key = msg.key()
        message = msg.value().decode("utf-8")
        payload = json.loads(message)
        if not self.redis_bloom.check_bloom_filter(
            topic=msg.topic(),
            group=str(self.group_id),
            value=int(f"1{msg.partition()}{msg.offset()}"),
        ):
            self.process(payload, key)
        else:
            if self.check_msg_is_processed(payload=payload) is True:
                m_log.error(
                    "topic: {}, partition: {}, offset: {}, msg: {} already processed".format(
                        msg.topic(), msg.partition(), msg.offset(), payload
                    )
                )
            else:
                self.process(payload, key)
        if not auto_commit:
            self.lst_processed_msg.append(int(f"{msg.partition()}{msg.offset()}"))
            self.manual_commit()
        self.redis_bloom.add_bloom_filter(
            topic=msg.topic(),
            group=str(self.group_id),
            value=int(f"1{msg.partition()}{msg.offset()}"),
        )

    def is_maintain(self):
        stat = self.pl.stat()
        st_mtime = stat.st_mtime
        if self.st_mtime != st_mtime:
            print(f"stat: {stat}")
            self.st_mtime = float(st_mtime)
            # return True if self.pl.read_text().strip() == '1' else False
            return True if stat.st_size == 2 else False
        return False

    def error_cb(self, err):
        m_log.error("Client error: {}".format(err))
        consumer_warning_slack(
            pod_name=os.getenv("HOSTNAME"),
            group_id=self.group_id,
            pretext="client error: {}".format(err),
        )

    def process(self, data, key=None):
        count_err = 0
        if self.retryable:
            recall_data = deepcopy(data)
        else:
            recall_data = None
        try:
            if "count_err" in data:
                count_err = int(data.pop("count_err"))
            self.message_handle(data=data)
        except Exception as e:
            m_log.error(
                "consumer::run - topic: {} ERR: {}".format(self.lst_subscribe_topic, e)
            )
            if recall_data and self.retryable:
                count_err += 1
                data_error = {
                    "topic": self.retry_topic,
                    "key": key.decode("ascii") if key else key,
                    "data": recall_data,
                    "error": str(e),
                    "count_err": count_err,
                    "next_run": datetime.utcnow() + timedelta(minutes=5 + count_err),
                    "status": RequeueStatus.ENABLE
                    if count_err <= 10
                    else RequeueStatus.DISABLE,
                }
                result = RequeueConsumerModel(self.client_mongo).insert(data=data_error)
                m_log.info("RequeueConsumerModel result: {}".format(result))

    @abstractmethod
    def message_handle(self, data):
        pass
