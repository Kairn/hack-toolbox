"""
Hosts creators of content matching functions usually used as predicates.
"""

import re


def http_resp_content_regex_flagger(regex, invert=False):
    """
    Creates a function that flags when the supplied "HttpResponse" matches the regex.
    :param regex:
    :param invert:
    :return:
    """

    def predicate(resp):
        content = resp.get_content_text()
        if re.search(regex, content):
            return not invert
        else:
            return invert

    return predicate
