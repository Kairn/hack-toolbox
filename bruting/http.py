"""
Hosts functions for brute forcing HTTP. All word lists and other trial data should be put under the "resources" directory.
"""

import os.path as p
from concurrent.futures import ThreadPoolExecutor

import core.net.http as http
from definitions import RESOURCE_DIR
from util.concurrent import AtomicInteger, ConcurrentSet
from util.extract import identity

LOG_STEP = 1000
# Never invoke more than 1 attack at a time.
GLOBAL_COUNTER = AtomicInteger(0)
FAILURES = ConcurrentSet()
STATUSES = set()


def parallel_attack(
    req_template,
    req_gen,
    predicate,
    sequence=None,
    data_file="test.txt",
    extractor=identity,
    threads=2,
):
    """
    Launches the HTTP brute force attack using the specified number of threads. A list of values is generated from the
    specified file, and they are used to construct HTTP requests which are then sent in parallel. Any response that
    satisfies the predicate will be collected with an alert message printed to the console.
    :param req_template:
    :param req_gen:
    :param predicate:
    :param sequence:
    :param data_file:
    :param extractor:
    :param threads:
    :return:
    """
    if not sequence:
        file = p.join(RESOURCE_DIR, data_file)
        with open(file, "r") as df:
            data_list = df.read().splitlines()
        data_list = [extractor(v) for v in data_list]
        data_set = set(data_list)
    else:
        data_set = set(sequence)

    print(
        "Prepare to launch parallel attack with {} orders queued".format(len(data_set))
    )
    hit_list = []
    attack_order = get_attack_order(req_template, req_gen, predicate, hit_list)

    global GLOBAL_COUNTER, FAILURES, STATUSES
    GLOBAL_COUNTER = AtomicInteger(0)
    FAILURES.clear()

    while True:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            status_codes = set(executor.map(attack_order, data_set))
        STATUSES = STATUSES.union(status_codes)
        if FAILURES.size() > 0:
            data_set = FAILURES.copy_to_set()
            FAILURES.clear()
        else:
            break

    print("Unique status codes: {}".format(STATUSES))
    print(
        "\nFinished HTTP parallel attack sequence with {} attack orders executed".format(
            GLOBAL_COUNTER.get()
        )
    )
    print("Found the following values resulting hits {}".format(hit_list))
    return hit_list


def get_attack_order(req_template, req_gen, predicate, hit_list):
    def attack_order(value):
        global GLOBAL_COUNTER, FAILURES
        attack_req = req_gen(req_template, value)
        try:
            resp = http.send_one(attack_req)
        except Exception:
            FAILURES.add(value)
            return 600

        if predicate(resp):
            print("HTTP attack hit on value {}".format(value))
            hit_list.append(value)
        else:
            pass

        count = GLOBAL_COUNTER.increment_and_get()
        if count % LOG_STEP == 0:
            print("Processed {} attack orders".format(count))

        return resp.get_status_code()

    return attack_order
