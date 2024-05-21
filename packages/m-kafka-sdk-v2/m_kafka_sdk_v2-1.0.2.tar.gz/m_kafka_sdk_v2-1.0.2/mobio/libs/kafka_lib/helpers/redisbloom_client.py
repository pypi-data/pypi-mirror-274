from mobio.libs.Singleton import Singleton
from redis.exceptions import ResponseError
import os
from mobio.libs.kafka_lib import MobioEnvironment


@Singleton
class RedisBloomClient:
    class RedisMode:
        STANDALONE = "1"
        CLUSTER = "2"

    def __int__(self, redis_client=None):
        if not redis_client:
            if os.getenv(MobioEnvironment.REDIS_TYPE) == self.RedisMode.CLUSTER:
                from redis.cluster import RedisCluster as _redis
            else:
                import redis as _redis
            self.rb = _redis.from_url(os.getenv(MobioEnvironment.REDIS_URI), decode_responses=True)
        else:
            self.rb = redis_client

    def __gen_func_name__(self, topic: str, group: str, filter_type: str) -> str:
        return f"{topic}{group}{filter_type}".replace("-", "C").replace("_", "C")

    def check_bloom_exists_filter(self, topic: str, group: str):
        key = self.__gen_func_name__(topic=topic, group=group, filter_type="Bloom")
        try:
            result = self.rb.bf().info(key)
        except ResponseError:
            print("BF.INFO {} not exists. Initially create Bloom filter".format(key))
            result = None
        return result

    def init_bloom_filter(
        self, topic: str, group: str, capacity: int, error_rate: float
    ):
        if not self.check_bloom_exists_filter(topic=topic, group=group):
            self.rb.bf().create(
                key=self.__gen_func_name__(topic=topic, group=group, filter_type="Bloom"),
                capacity=capacity,
                errorRate=error_rate,
                expansion=1
            )

    def add_bloom_filter(self, topic: str, group: str, value: object):
        return self.rb.bf().add(self.__gen_func_name__(topic=topic, group=group, filter_type="Bloom"), value)

    def check_bloom_filter(self, topic: str, group: str, value: object):
        return self.rb.bf().exists(self.__gen_func_name__(topic=topic, group=group, filter_type="Bloom"), value)

    def check_cuckoo_exists_filter(self, topic: str, group: str):
        key = self.__gen_func_name__(topic=topic, group=group, filter_type="Cuckoo")
        try:
            result = self.rb.cf().info(key)
        except ResponseError:
            print("CF.INFO {} not exists. Initially create Cuckoo filter".format(key))
            result = None
        return result

    def init_cuckoo_filter(self, topic: str, group: str, capacity: int):
        if (
            not self.check_cuckoo_exists_filter(topic=topic, group=group)
        ):
            self.rb.cf().create(
                key=self.__gen_func_name__(topic=topic, group=group, filter_type="Cuckoo"), capacity=capacity
            )

    def add_cuckoo_filter(self, topic: str, group: str, value: object):
        return self.rb.cf().add(self.__gen_func_name__(topic=topic, group=group, filter_type="Cuckoo"), value)

    def check_cuckoo_filter(self, topic: str, group: str, value: object):
        return self.rb.cf().exists(self.__gen_func_name__(topic=topic, group=group, filter_type="Cuckoo"), value)
