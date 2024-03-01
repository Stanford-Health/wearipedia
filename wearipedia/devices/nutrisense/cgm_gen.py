from collections import defaultdict
from datetime import datetime, timedelta
from threading import Thread

import numpy as np
import pandas as pd
from numpy.random import randint
from scipy.stats import tstd
from tqdm import tqdm


def gen_data(start_date, end_date, seed=0):
    """Main function for generating synthetic data for nutrisense cgm.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param seed: the seed for the random number generator, defaults to 0
    :type seed: int, optional
    :return: the data generated according to the inputs
    :rtype: tuple(dict, list[dict], dict, dict)
    """

    scores = gen_scores()
    continuous, Y = gen_continuous(start_date, end_date, seed)
    summary = gen_summary(Y)
    stat = {
        "today": gen_stats(Y),
        "average": gen_stats(Y, weekly=True),
    }
    return (scores, continuous, summary, stat)


def gen_continuous(start_date, end_date, seed=0):
    """Generate the continuous data. Other data generating functions depend on results
    from this function.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param seed: the seed for the random number generator, defaults to 0
    :type seed: int, optional
    :return: the data generated according to the inputs
    :rtype: tuple(list[dict], list[float])
    """

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dToStr = lambda x: f"{datetime.strftime(x, '%Y-%m-%dT%H:%M:%S')}-08:00"

    n = (end - start).days + 1

    datelist = pd.date_range(start, periods=n).tolist()

    X = []
    Y = []

    def gen_glucose(t, index, seed=0):
        local_rng = np.random.RandomState(seed + index)
        cdata = []

        y = local_rng.uniform(low=110, high=150, size=(1,))[0]

        for i in range(96):  # 15 minute segments in a day
            # simulate lack of adherence
            interpolated = False
            if local_rng.uniform(low=0, high=1, size=(1,))[0] > 0.95:
                interpolated = True

            x = t + i * timedelta(minutes=15)
            item = {
                "x": dToStr(x),
                "y": y,
                "interpolated": interpolated,
                "__typename": "TimePair",
            }
            cdata.append(item)
            X.append(x)
            Y.append(y)

            added = sorted([-1.1, local_rng.normal(scale=1), 1.1])[1] * 10 + 0.01 * (
                160 / y
            )
            if y < 75:
                added = abs(added)
            elif y > 135:
                added = -1 * abs(added)
            y += added

        result[index] = cdata

    threads = []
    result = defaultdict(dict)
    for j in tqdm(range(len(datelist))):
        t = datelist[j]
        new_thread = Thread(target=gen_glucose, args=(t, j, seed))
        threads.append(new_thread)

    # start threads
    for thread in threads:
        thread.start()

    # wait for all threads to terminate
    for thread in tqdm(threads):
        thread.join()

    continuous = []
    for k in sorted(result.keys()):
        continuous += result[k]

    return (continuous, Y)


def gen_summary(Y):
    """Generate a summary of data.

    :param Y: the synthetic sensor data
    :type Y: list[float]
    :return: a short dictionary of the summary statistics
    :rtype: dict
    """

    summary = {
        "min": min(Y),
        "max": max(Y),
        "goal": None,
        "goalMin": 70.0,
        "goalMax": 140.0,
        "__typename": "ChartRange",
    }
    return summary


def gen_scores():
    """Generate random scores for the daily statistics

    :return: a short dictionary of the random scores
    :rtype: dict
    """

    score = {
        "scoreTimeOutsideRange": randint(0, 11),
        "scorePeak": randint(0, 11),
        "scoreMean": randint(0, 11),
        "scoreStdDev": randint(0, 11),
        "score": randint(0, 11),
        "__typename": "DailyScore",
    }
    return score


def gen_stats(Y, weekly=False):
    """Generate random scores for the daily statistics

    :param Y: the synthetic sensor data
    :type Y: list[float]
    :param weekly: whether statistics are weekly, defaults to False
    :type weekly: bool, optional
    :return: a short dictionary of the random scores
    :rtype: dict
    """

    if weekly:
        low, high = min(Y), max(Y)
        median = np.median(Y)
        std = tstd(Y)
        q1, q3 = (np.quantile(Y, [0.25, 0.75])).round(1)
        greater = 70.0 < np.array(Y)
        less = np.array(Y) < 140.0
        condition = greater & less
        timeWithinRange = float(len(np.extract(condition, Y)))
        avg = np.average(Y)
    else:
        low = randint(min(Y), 110)
        high = randint(low, max(Y))
        median = randint(low, high)
        std = randint(0, 10)
        q1 = randint(low, median)
        q3 = randint(median, high)
        timeWithinRange = randint(0, 100)
        avg = randint(low, high)

    first = {"min": 70.0, "max": 140.0, "__typename": "Range"}
    second = {"min": low, "max": high, "__typename": "Range"}

    stat = {
        "healthyRange": first,
        "range": second,
        "timeWithinRange": timeWithinRange,
        "min": low,
        "max": high,
        "mean": avg,
        "median": median,
        "standardDeviation": std,
        "q1": q1,
        "q3": q3,
        "score": 0.0,
        "__typename": "Stat",
    }

    return stat
