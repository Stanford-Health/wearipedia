import os
from datetime import datetime, timedelta
from threading import Lock, Thread

from tqdm import tqdm

__all__ = ["fetch_real_data"]


def fetch_day_data(date, array, api_func, lock):
    date_str = datetime.strftime(date, "%Y-%m-%d")

    # this does not need to be in a critical section, since
    # requests don't really share state
    elem = api_func(date_str)

    # critical section, ensuring each index in each array
    # matches up. with the "lock" context manager,
    # we ensure that only one thread can access the
    # critical section (e.g. adding an element to the array)
    # at a time
    with lock:
        array.append(elem)


def fetch_real_data(start_date, end_date, data_type, api):
    """Main function for fetching real data from the Garmin Connect API.
    We parallelize this since making requests to the API is day-by-day,
    and API requests are I/O bound.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param data_type: the type of data to fetch, one of "dates", "steps", "hrs", "brpms"
    :type data_type: str
    :param api: the Garmin Connect API object
    :type api: Garmin
    :return: the data fetched from the API according to the inputs
    :rtype: List
    """

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

    # create a thread per each day, and assign it
    # to fetch the data for that day
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
