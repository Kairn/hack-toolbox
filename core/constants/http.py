"""
Stores HTTP or similar web related constants used in configurations.
"""

from enum import Enum


class Protocol(Enum):
    """
    HTTP/web protocols.
    """

    HTTP = "http"
    HTTPS = "https"
    FTP = "ftp"


class ContentType(Enum):
    """
    HTTP/web content/MIME types. Each item contains the content type string used in headers and a common extension
    string.
    """

    TEXT = ("text/plain", ".txt")
    FORM_URL = ("application/x-www-form-urlencoded", "")
    JSON = ("application/json", ".json")
    XML = ("application/xml", ".xml")
    HTML = ("text/html", ".html")


class HttpMethod(Enum):
    """
    HTTP methods.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HeaderField(Enum):
    """
    HTTP header fields.
    """

    CONTENT_TYPE = "Content-Type"
    ORIGIN = "Origin"
    USER_AGENT = "User-Agent"
    ACCEPT = "Accept"
    REFERER = "Referer"
