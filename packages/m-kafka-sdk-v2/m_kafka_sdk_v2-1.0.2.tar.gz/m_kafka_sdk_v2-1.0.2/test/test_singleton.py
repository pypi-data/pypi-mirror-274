from io_.mobio.kafka_sdk import SingletonArgs


class TestSingleton(metaclass=SingletonArgs):
    def __init__(self, bootstrap_server=None):
        pass
    pass


if __name__ == "__main__":
    if __name__ == "__main__":
        singleton = TestSingleton('127.0.0.1:9092')
        new_singleton = TestSingleton('kafka1:9092,kafka2:9092,kafka3:9092')
        new_singleton1 = TestSingleton('127.0.0.1:9092')
        singleton_non = TestSingleton()
        singleton_non1 = TestSingleton()
        singleton_kargs = TestSingleton({"abs": 1})
        singleton_kargs1 = TestSingleton({"abs": 1})

        assert singleton is new_singleton1
        assert singleton is not new_singleton
        assert singleton_non is not singleton
        assert singleton_non is singleton_non1
        assert singleton_kargs is singleton_kargs1
