from enum import Enum


class ResponseTypes(Enum):
    HTML = 'html'
    JSON = 'json'


class RestHeaders:
    def __init__(self, request):
        headers = request.headers
        self.host = headers['host'] if 'host' in headers else None
        self.connection = headers['connection'] if 'connection' in headers else None
        self.accept = headers['accept'] if 'accept' in headers else None
        self.accept_encoding = headers['accept_encoding'] if 'accept_encoding' in headers else None

    @property
    def response_type(self):
        if 'html' in self.accept:
            return ResponseTypes.HTML
        else:
            return ResponseTypes.JSON
