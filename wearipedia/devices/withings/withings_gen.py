import hashlib
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm

__all__ = ["create_synthetic_sleeps_df", "create_syn_hr", "create_syn_bodyplus"]

#############
# ScanWatch #
#############


def create_synthetic_sleeps_df(start_date, end_date):
    """Create a synthetic dataframe of sleep data. This is for
    the ScanWatch.

    :param start_date: the start date of the synthetic data as a string formatted as YYYY-MM-DD
    :type start_date: str
    :param end_date: the end date of the synthetic data as a string formatted as YYYY-MM-DD
    :type end_date: str
    :return: the synthetic dataframe containing sleep data
    :rtype: pd.DataFrame
    """

    start_day = datetime.strptime(start_date, "%Y-%m-%d")
    end_day = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end_day - start_day).days

    syn_sleeps = pd.DataFrame()

    syn_sleeps["id"] = np.random.randint(0, 100000000, size=(num_days,))
    syn_sleeps["timezone"] = "America/Los_Angeles"
    syn_sleeps["model"] = 16
    syn_sleeps["model_id"] = 93
    syn_sleeps[
        "hash_deviceid"
    ] = "d41d8cd98f00b204e9800998ecf8427e"  # randomly generated
    syn_sleeps["date"] = [
        datetime.fromtimestamp(
            datetime.strptime(start_date, "%Y-%m-%d").timestamp() + i * 24 * 3600
        ).strftime("%Y-%m-%d")
        for i in range(num_days)
    ]

    startdates = []
    enddates = []

    for date in syn_sleeps["date"]:
        sleep_start = np.random.randint(20, 27)
        sleep_time = np.random.randint(4, 9)

        startdate = datetime.strptime(date, "%Y-%m-%d") + timedelta(
            hours=sleep_start + 7
        )

        enddate = startdate + timedelta(hours=sleep_time)

        startdate, enddate = int(startdate.timestamp()), int(enddate.timestamp())

        startdates.append(startdate)
        enddates.append(enddate)

    all_data = []

    for _ in range(num_days):

        data = {
            "wakeupduration": np.random.randint(0, 3000),
            "wakeupcount": np.random.poisson(1),
            "durationtosleep": np.random.randint(120, 180),
            "durationtowakeup": np.random.randint(0, 700),
            "total_timeinbed": np.random.randint(10000, 50000),
            "total_sleep_time": np.random.randint(10000, 50000),
            "sleep_efficiency": np.random.rand() * 0.1 + 0.9,
            "sleep_latency": np.random.randint(120, 130),
            "wakeup_latency": np.random.randint(0, 800),
            "waso": np.random.randint(0, 4000),
            "nb_rem_episodes": 0,
            "out_of_bed_count": 0,
            "lightsleepduration": np.random.randint(6000, 35000),
            "deepsleepduration": np.random.randint(3000, 17000),
            "hr_average": np.random.randint(55, 65),
            "hr_min": np.random.randint(40, 60),
            "hr_max": np.random.randint(70, 120),
            "sleep_score": np.random.randint(30, 80),
        }

        all_data.append(data)

    syn_sleeps["startdate"] = startdates
    syn_sleeps["enddate"] = enddates

    syn_sleeps["data"] = all_data

    syn_sleeps["created"] = enddates
    syn_sleeps["modified"] = enddates

    return syn_sleeps


def create_syn_hr(start_date, end_date, syn_sleeps):
    """Create a synthetic dataframe of heart rate data. This is for
    the ScanWatch.

    :param syn_sleeps: the synthetic sleep dataframe
    :type syn_sleeps: pd.DataFrame
    :return: the synthetic dataframe containing heart rate data
    :rtype: pd.DataFrame
    """
    start_day = datetime.strptime(start_date, "%Y-%m-%d")
    end_day = datetime.strptime(end_date, "%Y-%m-%d")

    num_days = (end_day - start_day).days

    hour_usage = [0.8] * 3 + [0.9] * 7 + [1.0] * 10 + [0.9] * 4

    datetimes = []

    for day_offset in tqdm(range(num_days)):
        for hour_offset in range(24):
            for minute_offset in range(0, 60, 10):
                day = start_day + timedelta(days=day_offset)
                hour = day + timedelta(hours=hour_offset)
                minute = hour + timedelta(minutes=minute_offset)

                if np.random.uniform(0, 1) < hour_usage[hour_offset]:
                    datetimes.append(minute)

    hr_measurements = (np.random.randn(len(datetimes)) * 5 + 90).astype("int")

    timestamps = np.array([dt.timestamp() for dt in datetimes])

    for i, (startdate, enddate) in tqdm(
        enumerate(zip(syn_sleeps.startdate, syn_sleeps.enddate))
    ):
        idxes = np.where(np.logical_and(timestamps > startdate, timestamps < enddate))[
            0
        ]
        duration = (enddate - startdate) / 3600
        avg_hr = -5 / 7 * duration + 64.1428571429

        hr_measurements[idxes] = (np.random.randn(idxes.shape[0]) + avg_hr).astype(
            "int"
        )

    syn_hr = pd.DataFrame()
    syn_hr["datetime"] = datetimes
    syn_hr["heart_rate"] = hr_measurements

    syn_hr["model"] = "ScanWatch"
    syn_hr["model_id"] = 93
    syn_hr["deviceid"] = hashlib.md5().hexdigest()

    num_garbage = 1000

    timestamps_garbage = np.random.uniform(
        (start_day - timedelta(days=100)).timestamp(),
        start_day.timestamp(),
        size=num_garbage,
    )

    garbage_df = pd.DataFrame()
    garbage_df["datetime"] = [
        datetime.fromtimestamp(int(ts)) for ts in timestamps_garbage
    ]
    garbage_df["heart_rate"] = (np.random.randn(num_garbage) * 5 + 90).astype("int")

    garbage_df["model"] = None
    garbage_df["model_id"] = 1059
    garbage_df["deviceid"] = None

    syn_hr = pd.concat((garbage_df, syn_hr), ignore_index=True)

    return syn_hr


#########
# Body+ #
#########


def create_syn_bodyplus(start_date):
    """Create a synthetic dataframe of body+ data. This is for
    the Body+ scale. The reason why we don't have an end date is
    because we wish to generate 2.5 years' worth of data to portray
    a fictional scenario where the user has been using the scale
    for a year and we see the impact of a fictional medication.

    :param start_date: the start date as a string formatted as YYYY-MM-DD
    :type start_date: str
    :return: the synthetic dataframe containing body+ data
    :rtype: pd.DataFrame
    """

    # captures before/after meal weight discrepancies, offset from mean weight
    offsets = [0] * 7 + [
        -1,
        -1,
        -0.5,
        -0.5,
        0.5,
        0.5,
        0.2,
        0,
        -0.2,
        -0.5,
        -0.1,
        0.7,
        0.8,
        0.7,
        0.6,
        0.6,
    ]

    total_duration = 75168000  # 2.5 years in seconds
    start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())

    # generate times by the day, sample from 8am to 11:59pm
    random_times = []
    for dt in range(start_ts, start_ts + total_duration, 24 * 3600):
        random_times += list(
            np.random.uniform(
                dt + 8 * 3600, dt + 24 * 3600, size=np.random.randint(0, 5)
            )
        )

    # delete so we have 1400 elements in the end
    to_delete = np.random.choice(
        len(random_times), size=len(random_times) - 1400, replace=False
    )
    random_times = np.delete(random_times, to_delete)

    weights = np.random.normal(60, 1, len(random_times)) + np.concatenate(
        (np.linspace(8, 10, 200), np.linspace(10, 0, 1200))
    )

    random_times_hour = np.array(
        [int(datetime.fromtimestamp(t).strftime("%H")) for t in random_times]
    )

    # now actually offset the weights
    for i, offset in zip(range(24), offsets):
        special_idxes = np.where(random_times_hour == i)[0]
        weights[special_idxes] = weights[special_idxes] + np.random.normal(
            offset, 1, len(special_idxes)
        )

    fat_percent = np.random.normal(3, 1, len(random_times)) + np.concatenate(
        (np.linspace(25, 30, 200), np.linspace(30, 13, 1200))
    )

    df = pd.DataFrame(columns=["date", "Weight (kg)", "Fat Ratio (%)"])

    df.date = [datetime.fromtimestamp(t) for t in random_times]
    df["Weight (kg)"] = weights
    df["Fat Ratio (%)"] = fat_percent

    # user left out some data, went on vacation, etc.
    df.drop(index=df.index[300:310], axis=0, inplace=True)

    df.drop(index=df.index[400:410], axis=0, inplace=True)

    return df
