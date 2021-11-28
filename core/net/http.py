"""
Lower level specifications and functions to handle HTTP/web related operations.
"""

import requests

from core.conf.http import HttpResponse


def send_one(req):
    """
    Sends a HTTP request and retrieves a response wrapper.
    :param req:
    :return:
    """
    method = req.get_method()
    url = req.get_url()

    return HttpResponse(
        requests.request(
            method,
            url,
            params=req.params,
            data=req.body,
            headers=req.headers,
            cookies=req.cookies,
            files=req.files,
        )
    )
