from datetime import datetime

class ContextSingleton:
    """
    A single instance for logging and database
    """
    _self = None

    def __new__(cls, logger=None, database=None, config=None, *args, **kwargs):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls.logger = logger
            cls.database = database
            cls.config = config
            cls.init_time = datetime.utcnow()
        return cls._self
