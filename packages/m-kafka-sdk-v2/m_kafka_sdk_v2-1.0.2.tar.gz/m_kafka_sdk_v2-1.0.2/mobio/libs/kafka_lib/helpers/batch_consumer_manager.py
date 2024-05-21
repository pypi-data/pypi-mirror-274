from abc import abstractmethod
from numbers import Number
from confluent_kafka.cimpl import KafkaError, KafkaException, Consumer
from mobio.libs.kafka_lib import KAFKA_BOOTSTRAP
from mobio.libs.kafka_lib.helpers import consumer_warning_slack
from time import time, sleep
from uuid import uuid4
import os
import pathlib
import json
try:
    from mobio.libs.logging import MobioLogging
    m_log = MobioLogging()
except Exception:
    import logging as MobioLogging

    m_log = MobioLogging


def commit_completed(err, partitions):
    if err:
        m_log.error(str(err))
    else:
        m_log.info("Committed partition offsets: " + str(partitions))


class BatchConsumerManager:
    def __init__(
        self,
        lst_subscribe_topic: list,
        group_id: object,
        bootstrap_server=None,
        # retry_topic=None,
        **kwargs,
    ):
        self.auto_commit = False
        self.has_offset = False
        self.client_id = str(uuid4())
        if not group_id or not isinstance(group_id, str):
            raise Exception("group_id: {} is not valid".format(group_id))
        self.group_id = group_id
        if not lst_subscribe_topic or any([not x or not isinstance(x, str) for x in lst_subscribe_topic]):
            raise Exception(
                "lst_subscribe_topic: {} is not valid".format(lst_subscribe_topic))
        self.lst_subscribe_topic = lst_subscribe_topic
        # self.retry_topic = retry_topic if retry_topic else self.lst_subscribe_topic[0]
        session_timeout_ms = 25000
        config = {
            "bootstrap.servers": KAFKA_BOOTSTRAP
            if not bootstrap_server
            else bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": "latest",
            "session.timeout.ms": kwargs.get("session_timeout_ms", session_timeout_ms),
            "client.id": self.client_id,
            "error_cb": self.error_cb,
            "enable.auto.commit": "false" if not self.auto_commit else True,
            "on_commit": commit_completed,
        }

        if "consumer_config" in kwargs and kwargs.get("consumer_config"):
            config.update(kwargs.get("consumer_config"))
        self.c = Consumer(config)
        self.last_time_commit = time()
        self.st_mtime = None
        self.default_commit_time = 5
        num_messages = 50
        consume_timeout = 1.0

        if 'num_messages' in kwargs and isinstance(kwargs.get('num_messages'), int):
            num_messages = kwargs.get('num_messages')
            if not (10 <= num_messages <= 1000):
                raise Exception(
                    "num_messages: {} is not valid, num_messages must between 10, 1000 messages".format(num_messages))
        else:
            m_log.warning(
                'set num_messages with default: {}'.format(num_messages))
        if 'consume_timeout' in kwargs and isinstance(kwargs.get('consume_timeout'), Number):
            consume_timeout = float(kwargs.get('consume_timeout'))
            if not (1.0 <= consume_timeout <= 30.0):
                raise Exception(
                    "consume_timeout: {} is not valid, consume_timeout must between 1, 30 seconds".format(consume_timeout))
        else:
            m_log.warning(
                'set consume_timeout with default: {}'.format(consume_timeout))

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

            while True:
                if self.is_maintain():
                    if not self.auto_commit:
                        self.manual_commit()
                    sleep(self.default_commit_time)
                    m_log.warning(
                        "System is Maintenance !!! Feel free and drink some tea. :)"
                    )
                    continue
                lst_msg = self.c.consume(
                    num_messages=num_messages, timeout=consume_timeout)
                # If consumer is end of offset, manual commit with period
                if len(lst_msg) == 0:
                    if not self.auto_commit:
                        self.manual_commit()
                    continue
                msg = lst_msg[-1]
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
                        self.process(lst_msg=lst_msg)

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
            m_log.error("KafkaException: {}: {}".format(
                self.lst_subscribe_topic, e))
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
        if now - self.last_time_commit >= self.default_commit_time:
            if self.has_offset:
                # raise Exception("break commit :)")
                self.c.commit(asynchronous=True)
                m_log.info(f"committed")
                self.last_time_commit = now
                self.has_offset = False
            else:
                pass
                # m_log.info("no offset to commit")

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

    def process(self, lst_msg):
        try:
            if lst_msg:
                self.has_offset = True
            self.message_handle(
                lst_msg=[json.loads(x.value().decode("utf-8")) for x in lst_msg])
            self.manual_commit()
        except Exception as e:
            m_log.error(
                "consumer::run - topic: {} ERR: {}".format(
                    self.lst_subscribe_topic, e)
            )

    @abstractmethod
    def message_handle(self, lst_msg):
        pass
