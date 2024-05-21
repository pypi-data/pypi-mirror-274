- **Thư viện Consumer của JB. Chạy consumer ở Process, phù hợp cho môi trường K8s** :

- **NOTE: SDK sử dụng confluent-kafka depend requirements của module. SDK không có install_requires confluent-kafka :)** ::cheers::
* Bản này yêu cầu confluent-kafka >= 1.7.0 & requests>=2.25.1
# create topic
Note:
- EnsureKafkaTopic.REPLICATION_ASSIGNMENT là giá trị các brokers isolate của từng module. Nếu giá trị này chưa được DevOps khởi tạo nó sẽ được lấy giá trị từ *DEFAULT_BROKER_ID_ASSIGN*  
```python
from mobio.libs.kafka_lib.helpers.ensure_kafka_topic import EnsureKafkaTopic
import os
from mobio.libs.kafka_lib import MobioEnvironment

EnsureKafkaTopic().create_kafka_topics(
        [
            # TEST WITH SET replica_assignment
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test1",
                EnsureKafkaTopic.NUM_PARTITIONS: 8,
                EnsureKafkaTopic.CONFIG: {"compression.type": "snappy"},
                EnsureKafkaTopic.REPLICATION_ASSIGNMENT: os.getenv(
                    MobioEnvironment.SALE_BROKER_ID_ASSIGN # SALE_BROKER_ID_ASSIGN
                ) # danh sách các broker_ids "10,20,30" ,
            },
            # TEST WITH SET replica_factor
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test2",
                EnsureKafkaTopic.REPLICATION_ASSIGNMENT: os.getenv(
                    MobioEnvironment.PROFILING_BROKER_ID_ASSIGN
                )
            },
            # TEST WITH SET config
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test3",
                EnsureKafkaTopic.NUM_PARTITIONS: 1,
                EnsureKafkaTopic.CONFIG: {"compression.type": "snappy"},
                EnsureKafkaTopic.REPLICATION_ASSIGNMENT: os.getenv(
                    MobioEnvironment.JB_BROKER_ID_ASSIGN
                )
            },
            # TEST WITHOUT manual config
            {
                EnsureKafkaTopic.TOPIC_NAME: "giang-test4",
                EnsureKafkaTopic.NUM_PARTITIONS: 1,
            },
        ]
    )
```


# Producer
```python
from mobio.libs.kafka_lib.helpers.kafka_producer_manager import KafkaProducerManager
KafkaProducerManager().flush_message(topic="test", key="uuid", value={"test":1})
```

# Consumer normal
```python
import os
from pymongo import MongoClient
from mobio.libs.kafka_lib.helpers.kafka_consumer_manager import BaseKafkaConsumer


class TestConsumer(BaseKafkaConsumer):
    def message_handle(self, data):
        print("TestConsumer: data: {}".format(data))


if __name__ == "__main__":
    url_connection = os.getenv('TEST_MONGO_URI')
    client_mongo = MongoClient(url_connection, connect=False)

    TestConsumer(topic_name="test", group_id="test", client_mongo=client_mongo, retryable=True, lst_subscribe_topic=['test', 'test1'], retry_topic='test1')
```

# Consumer with bloom filter
```python
import os
from pymongo import MongoClient
from mobio.libs.kafka_lib.helpers.kafka_consumer_manager import BaseKafkaConsumer


class TestConsumer(BaseKafkaConsumer):
    def check_msg_is_processed(self, payload: dict) -> bool:
      msg_id = payload.get("msg_id")
      exists = self.client_mongo.get_database("test_db")["test_collection"].find_one({"id": msg_id})
      return True if exists else False
      
    def message_handle(self, data):
        print("TestConsumer: data: {}".format(data))


if __name__ == "__main__":
    url_connection = os.getenv('TEST_MONGO_URI')
    client_mongo = MongoClient(url_connection, connect=False)

    TestConsumer(topic_name="test", group_id="test", client_mongo=client_mongo, retryable=True, lst_subscribe_topic=['test', 'test1'], retry_topic='test1', enable_bloom=True, auto_commit=True)
```

# change logs

* 1.0.2 (2024-05-20)
  * Build 1.0.1-rc3 thành 1.0.2, không sửa logic

* 1.0.1-rc3 (2024-03-20)
  * Batch consume message
    * Bỏ log "no offset to commit"
    * Sử dụng redisbloom<=0.4.0 do redisbloom==0.4.1 bắt buộc redis==3.5.3

* 1.0.1-rc2 (2024-03-01)
  * Batch consume message
    * Fix lỗi không commit message khi xử lý xong

* 1.0.1-rc1 (2024-02-15)
  * Batch consume message
    * Ở phiên bản hiện tại, batch consumer chưa support requeue. 

* 1.0.1 (2024-01-05)
  * Truyền redis-client trong parameters khởi tạo consumer, nếu không truyền thì tạo redis-client từ URI mặc định.
* 1.0.0 (2023-12-13):
  * Cho phép cấu hình auto/manual commit
  * Sử dụng bloom-filter để check duplicate message trong quá trình consume message
  * Yêu cầu sử dụng cùng redis-bloom nếu enable bloom
* 0.1.8 (2023-08-25):
  * thêm option lst_subscribe_topic
    * Nếu truyền lst_subscribe_topic thì bỏ qua topic_name
    * Nếu ko truyền lst_subscribe_topic thì lấy topic_name làm topic subscribe
  * thêm option retry_topic
    * Nếu không chỉ định sẽ lấy topic đầu tiên của list subscribe
    * Nếu ko truyền list subscribe thì lấy topic_name làm retry
* 0.1.7 (2023-04-18):
  * cho phép truyền vào broker khi khởi tạo consumer, producer. Nếu không truyền thì sẽ lấy mặc định trong ENV KAFKA_BROKER
  * singleton producer với *args && **kwargs
  * bỏ requirements "m-singleton>=0.3", "m-caching>=0.1.8"
* 0.1.6 (2023-04-05):
  * k8s liveness v2
* 0.1.5 (2022-10-12):
  * raise exception khi close kafka, đảm bảo k8s sẽ restart lại pod
* 0.1.4.2 (2022-09-19):
  * fix bug topic được tạo đang random vào cả các broker isolate cho module khác.
* 0.1.4.1 (2022-09-19):
  * cho phép truyền vào brokers mà topic này sẽ được replicate
* 0.1.4 (2022-08-23):
  * Bổ sung thêm phần lưu mapping pod-name và client-id vào file 
* 0.1.3:
  * Mặc định compress messages ở đầu producer
  * Function create kafka topic hỗ trợ truyền số partitions và settings của topic  

* 0.1.1: fix bug init Config