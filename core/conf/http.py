"""
Pure data classes/objects related to HTTP configurations and processes. Minimalist design.
More will be added only as needed by other tools.
"""

from core.constants.http import HttpMethod, Protocol


class HttpRequest:
    """
    Simple HTTP request data structure.
    """
    protocol = None
    method = None
    host = None
    path = None
    headers = None
    cookies = None
    params = None
    body = None
    files = None

    def __init__(self, protocol=Protocol.HTTP, method=HttpMethod.GET, host=None, path=None, headers=None, params=None,
                 body=None):
        self.protocol = protocol
        self.method = method
        self.host = host
        self.path = path
        self.headers = headers
        self.params = params
        self.body = body

    def get_method(self):
        """
        Returns the HTTP method. Defaults to GET.
        :return:
        """
        if self.method is None:
            return HttpMethod.GET.value
        else:
            return self.method.value

    def get_url(self):
        """
        Parses and returns the URL string from the request.
        :return:
        """
        if self.host is None:
            return None

        if self.path is None:
            address = self.host + "/"
        elif self.path.startswith("/"):
            address = self.host + self.path
        else:
            address = "/".join((self.host, self.path))

        if self.protocol is None:
            return Protocol.HTTP.value + "://" + address
        else:
            return self.protocol.value + "://" + address


class HttpResponse:
    """
    HTTP response object that primarily serves as a parser/handler for "requests.Response".
    """
    raw_resp = None

    def __init__(self, resp):
        self.raw_resp = resp
