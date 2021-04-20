"""
Pure data classes/objects related to HTTP configurations and processes. Minimalist design.
More will be added only as needed by other tools.
"""

from core.constants.http import HttpMethod, Protocol


class HttpRequest:
    """
    Simple HTTP request data structure.
    """
    host = None
    protocol = None
    method = None
    path = None
    headers = None
    cookies = None
    params = None
    body = None
    files = None

    def __init__(self, host="localhost", protocol=Protocol.HTTP, method=HttpMethod.GET, path=None, headers=None,
                 cookies=None, params=None, body=None, files=None):
        self.host = host
        self.protocol = protocol
        self.method = method
        self.path = path
        self.headers = headers
        self.cookies = cookies
        self.params = params
        self.body = body
        self.files = files

    def clone(self):
        """
        Creates an shallow copy of this object.
        :return:
        """
        return HttpRequest(self.host, self.protocol, self.method, self.path, self.headers, self.cookies, self.params,
                           self.body, self.files)

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

    def get_content_text(self):
        """
        Retrieves the response content as a text string.
        :return:
        """
        return self.raw_resp.text

    def get_status_code(self):
        """
        Returns the status code of the response.
        :return:
        """
        return self.raw_resp.status_code
