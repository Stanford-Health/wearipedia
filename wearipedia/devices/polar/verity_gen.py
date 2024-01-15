import copy
import datetime
from collections import defaultdict
from threading import Thread

import numpy as np
import pandas as pd
from tqdm import tqdm


def gen_data(seed, start_date, end_date):
    """Main function for creating synthetic heart rate data for the Verity Sense.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: a dictionary with keys the training session dates and values a dictionary with keys heart_rates, calories, and minutes
    :rtype: Dict[str: Dict[str: list, str: int, str: int]]
    """
    sessions = np.datetime64(end_date) - np.datetime64(start_date)
    durations = (45, 60)  # minutes

    def gen_session(result, index):
        local_rng = np.random.RandomState(seed + index)

        # simulate skip day
        if local_rng.uniform(low=0, high=1, size=(1,))[0] > 0.8:
            return

        # day that you workout
        day = np.datetime64(start_date) + np.timedelta64(index, "D")
        duration = int(
            local_rng.uniform(low=durations[0], high=durations[1], size=(1,))[0]
        )
        hrate = []
        start_rate = local_rng.uniform(low=70, high=110, size=(1,))[0]

        for _ in range(duration * 60):
            hrate.append(start_rate)
            added = local_rng.normal(scale=1) + 0.01 * (160 / start_rate)
            if start_rate < 50:
                added = abs(added)
            elif start_rate > 190:
                added = -1 * abs(added)
            start_rate += added

        result[pd.to_datetime(day).strftime("%Y-%m-%d")]["heart_rates"] = copy.deepcopy(
            hrate
        )
        result[pd.to_datetime(day).strftime("%Y-%m-%d")]["calories"] = int(
            local_rng.uniform(low=200, high=500, size=(1,))[0]
        )
        result[pd.to_datetime(day).strftime("%Y-%m-%d")]["minutes"] = duration

    threads = []
    result = defaultdict(dict)
    for i in tqdm(range(int(sessions / np.timedelta64(1, "D")))):
        new_thread = Thread(target=gen_session, args=(result, i))

        threads.append(new_thread)

    # start threads
    for thread in threads:
        thread.start()

    # wait for all threads to terminate
    for thread in tqdm(threads):
        thread.join()

    return result
