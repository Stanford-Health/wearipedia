import os
from datetime import datetime, timedelta
from threading import Lock, Thread

import requests
from tqdm import tqdm

__all__ = ["fetch_real_data"]


def fetch_day_data(date, array, api_func, lock):
    date_str = datetime.strftime(date, "%Y-%m-%d")

    elem = api_func(date_str)
    # steps_data = api.get_steps_data(date_str)
    # hr_data = api.get_heart_rates(date_str)
    # brpm_data = api.get_respiration_data(date_str)

    # critical section, ensuring each index in each array
    # matches up
    with lock:
        array.append(elem)


def fetch_real_data(start_date, end_date, data_type, api):
    num_days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days

    lock = Lock()

    if data_type == "steps":
        api_func = api.get_steps_data
    elif data_type == "hrs":
        api_func = api.get_heart_rates
    elif data_type == "brpms":
        api_func = api.get_respiration_data
    elif data_type == "dates":
        # no API interaction here
        return [
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            for i in tqdm(range(num_days))
        ]

    arr = []

    # configure threads to add to the list
    print("configuring threads...")
    threads = []

    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)

        new_thread = Thread(target=fetch_day_data, args=(new_date, arr, api_func, lock))

        threads.append(new_thread)

    # start threads
    for thread in threads:
        thread.start()

    # wait for all threads to terminate
    print("Main thread waiting for child threads...")
    for thread in tqdm(threads):
        thread.join()

    # report the number of items in the list
    print("\ndone")

    return arr
