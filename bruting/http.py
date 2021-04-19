"""
Hosts functions for brute forcing HTTP. All word lists and other trial data should be put under the "resources" directory.
"""

import os.path as p
from concurrent.futures import ThreadPoolExecutor

import core.net.http as http
from definitions import RESOURCE_DIR
from util.extract import identity


def parallel_attack(req_template, req_gen, predicate, data_file="test.txt", extractor=identity, threads=2):
    """
    Launches the HTTP brute force attack using the specified number of threads. A list of values is generated from the
    specified file, and they are used to construct HTTP requests which are then sent in parallel. Any response that
    satisfies the predicate will be collected with an alert message printed to the console.
    :param req_template:
    :param req_gen:
    :param predicate:
    :param data_file:
    :param extractor:
    :param threads:
    :return:
    """
    file = p.join(RESOURCE_DIR, data_file)
    with open(file) as df:
        data_list = df.read().splitlines()
    data_list = [extractor(v) for v in data_list]
    hit_list = []
    attack_order = get_attack_order(req_template, req_gen, predicate, hit_list)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(attack_order, data_list)

    print("\nFinished HTTP parallel attack sequence")
    return hit_list


def get_attack_order(req_template, req_gen, predicate, hit_list):
    def attack_order(value):
        attack_req = req_gen(req_template, value)
        resp = http.send_one(attack_req)
        if predicate(resp):
            print("HTTP attack hit on value {}".format(value))
            hit_list.append(value)
        else:
            pass

    return attack_order
