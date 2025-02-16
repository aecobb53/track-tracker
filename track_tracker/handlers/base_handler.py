from models import ContextSingleton


class BaseHandler:
    def __init__(self, *args, **kwargs):
        self.context = ContextSingleton()
