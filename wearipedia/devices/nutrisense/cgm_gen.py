from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from fbm import fbm
from numpy.random import randint
from scipy.stats import tstd


def gen_data(start_date, end_date):
    """Main function for generating synthetic data for nutrisense cgm.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: the data generated according to the inputs
    :rtype: tuple(dict, list[dict], dict, dict)
    """

    scores = gen_scores()
    continuous, Y = gen_continuous(start_date, end_date)
    summary = gen_summary(Y)
    stat = {
        "today": gen_stats(Y),
        "average": gen_stats(Y, weekly=True),
    }
    return (scores, continuous, summary, stat)


def gen_continuous(start_date, end_date):
    """Generate the continuous data. Other data generating functions depend on results
    from this function.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: the data generated according to the inputs
    :rtype: tuple(list[dict], list[float])
    """

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    dToStr = lambda x: datetime.strftime(x, "%Y-%m-%dT%H:%M:%S") + "-08:00"

    n = (end - start).days + 1

    datelist = pd.date_range(start, periods=n).tolist()

    continuous = []

    fbm_sample = fbm(n=n * 96, hurst=0.40, length=0.5, method="daviesharte")
    fbm_sample = (abs(fbm_sample * 70) + 70).round(1)

    X = []
    Y = []

    for j in range(len(datelist)):
        t = datelist[j]
        for i in range(96):  # 15 minute segments in a day
            x = t + i * timedelta(minutes=15)
            y = fbm_sample[j * 96 + i]
            item = {
                "x": dToStr(x),
                "y": y,
                "interpolated": True,
                "__typename": "TimePair",
            }
            continuous.append(item)
            X.append(x)
            Y.append(y)

    return (continuous, Y)


def gen_summary(Y):
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
    if weekly:
        low = randint(70, 110)
        high = randint(low, 140)
        median = randint(low, high)
        std = randint(0, 10)
        q1 = randint(low, median)
        q3 = randint(median, high)
        timeWithinRange = randint(0, 100)
        avg = randint(low, high)
    else:
        low, high = min(Y), max(Y)
        median = np.median(Y)
        std = tstd(Y)
        q1, q3 = (np.quantile(Y, [0.25, 0.75])).round(1)
        greater = 70.0 < np.array(Y)
        less = np.array(Y) < 140.0
        condition = greater & less
        timeWithinRange = float(len(np.extract(condition, Y)))
        avg = np.average(Y)

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
