import copy
import datetime
from collections import defaultdict
from threading import Thread

import numpy as np
import pandas as pd
from tqdm import tqdm


def gen_data(seed, start_date, end_date):
    """Main function for creating synthetic heart rate data for the H10.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: a tuple of dictionary with keys the training session dates and values a dictionary with keys RR< heart_rates, calories, and minutes
    :rtype: tuple(Dict[str: list, str: list], Dict[str: Dict[str: list, str: int, str: int]])
    """
    sessions = np.datetime64(end_date) - np.datetime64(start_date)
    durations = (45, 60)  # minutes

    def gen_all(rr_result, hr_result, index):
        local_rng = np.random.RandomState(seed + index)

        # simulate skip day
        if local_rng.uniform(low=0, high=1, size=(1,))[0] > 0.8:
            return

        # day that you workout
        day = np.datetime64(start_date) + np.timedelta64(index, "D")
        duration = int(
            local_rng.uniform(low=durations[0], high=durations[1], size=(1,))[0]
        )

        # RR data
        rr_list = []
        c_rr = local_rng.uniform(low=400, high=2000, size=(1,))[0]

        # heart rate data
        hrate = []
        start_rate = local_rng.uniform(low=70, high=110, size=(1,))[0]

        for _ in range(duration * 60):

            # heart rate data
            hrate.append(start_rate)
            added = local_rng.normal(scale=1) + 0.01 * (160 / start_rate)
            if start_rate < 50:
                added = abs(added)
            elif start_rate > 190:
                added = -1 * abs(added)
            start_rate += added

            # RR data
            rr_list.append(c_rr)
            added = local_rng.normal(scale=1) + 0.01 * (1000 / c_rr)
            if c_rr < 400:
                added = abs(added)
            elif c_rr > 2000:
                added = -1 * abs(added)
            c_rr += added

        # save heart rate data
        hr_result[pd.to_datetime(day).strftime("%Y-%m-%d")]["heart_rates"] = hrate
        hr_result[pd.to_datetime(day).strftime("%Y-%m-%d")]["calories"] = int(
            local_rng.uniform(low=200, high=500, size=(1,))[0]
        )
        hr_result[pd.to_datetime(day).strftime("%Y-%m-%d")]["minutes"] = duration

        # save RR data
        # create a list of timestamps
        cur_time = datetime.datetime.strptime("00:00:00.0", "%H:%M:%S.%f")
        date_list = []

        for interval in rr_list:
            date_list.append(cur_time)
            cur_time = cur_time + datetime.timedelta(milliseconds=interval)

        rr_result[pd.to_datetime(day).strftime("%Y-%m-%d")]["rr"] = rr_list
        rr_result[pd.to_datetime(day).strftime("%Y-%m-%d")]["time"] = date_list

    threads = []
    hr_result = defaultdict(dict)
    rr_result = defaultdict(dict)
    for i in tqdm(range(int(sessions / np.timedelta64(1, "D")))):
        new_thread = Thread(target=gen_all, args=(rr_result, hr_result, i))
        threads.append(new_thread)

    # start threads
    for thread in threads:
        thread.start()

    # wait for all threads to terminate
    for thread in tqdm(threads):
        thread.join()

    return rr_result, hr_result
