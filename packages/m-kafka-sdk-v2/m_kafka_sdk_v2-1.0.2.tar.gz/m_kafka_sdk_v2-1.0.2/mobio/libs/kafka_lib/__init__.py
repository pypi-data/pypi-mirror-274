import os
import inspect


class ConsumerGroup:
    DEFAULT_CONSUMER_GROUP_ID = "mobio-consumers"


class RequeueStatus:
    ENABLE = 0
    DISABLE = -1


class MobioEnvironment:
    HOST = 'HOST'
    ADMIN_HOST = 'ADMIN_HOST'
    REDIS_URI = 'REDIS_URI'
    REDIS_TYPE = 'REDIS_TYPE'
    REDIS_HOST = 'REDIS_HOST'
    REDIS_PORT = 'REDIS_PORT'
    KAFKA_BROKER = 'KAFKA_BROKER'
    KAFKA_REPLICATION_FACTOR = 'KAFKA_REPLICATION_FACTOR'
    YEK_REWOP = 'YEK_REWOP'
    DEFAULT_BROKER_ID_ASSIGN = "DEFAULT_BROKER_ID_ASSIGN"
    SALE_BROKER_ID_ASSIGN = "SALE_BROKER_ID_ASSIGN"
    PROFILING_BROKER_ID_ASSIGN = "PROFILING_BROKER_ID_ASSIGN"
    JB_BROKER_ID_ASSIGN = "JB_BROKER_ID_ASSIGN"
    REDIS_CLUSTER_URI = "REDIS_CLUSTER_URI"


KAFKA_BOOTSTRAP = os.getenv(MobioEnvironment.KAFKA_BROKER)


class SingletonArgs(type):
    """ Singleton that keep single instance for single set of arguments. E.g.:
    assert SingletonArgs('spam') is not SingletonArgs('eggs')
    assert SingletonArgs('spam') is SingletonArgs('spam')
    """
    _instances = {}
    _init = {}

    def __init__(cls, name, bases, dct):
        cls._init[cls] = dct.get('__init__', None)

    def __call__(cls, *args, **kwargs):
        init = cls._init[cls]
        if init is not None:
            key = (cls, frozenset(
                           [x.__str__() for x in inspect.getcallargs(init, None, *args, **kwargs).items()]))
        else:
            key = cls

        if key not in cls._instances:
            cls._instances[key] = super(SingletonArgs, cls).__call__(*args, **kwargs)
        return cls._instances[key]
