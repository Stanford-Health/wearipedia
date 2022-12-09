# utils for generating synthetic data

import datetime

import dateutil
import numpy as np
import pandas as pd
from tqdm import tqdm

__all__ = [
    "create_fake_cycles_df",
    "create_fake_metrics_df",
    "create_fake_hr_df",
    "create_fake_sleeps_df",
]


def create_fake_cycles_df(start_date, end_date):
    """Create fake cycles dataframe. Each "cycle" is essentially a day.

    :param start_date: the start date of the synthetic data as a string formatted as YYYY-MM-DD
    :type start_date: str
    :param end_date: the end date of the synthetic data as a string formatted as YYYY-MM-DD
    :type end_date: str
    :return: cycles dataframe
    :rtype: pd.DataFrame
    """

    cycles_df_syn = pd.DataFrame(
        columns=[
            "id",
            "day",
            "rMSSD",
            "resting_hr",
            "recovery_score",
            "n_naps",
            "sleep_need_baseline",
            "sleep_debt",
            "sleep_need_strain",
            "sleep_need_total",
            "sleep_quality_duration",
            "avg_hr",
            "kilojoules",
            "max_hr",
            "strain_score",
        ]
    )

    start_day = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_day = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    num_sleeps = (end_day - start_day).days

    cycles_df_syn.id = np.random.choice(range(1000), size=(num_sleeps,), replace=False)

    cycles_df_syn.day = pd.date_range(start_day, end_day - datetime.timedelta(days=1), freq="D")

    cycles_df_syn.recovery_score = np.clip(
        50 + 10 * np.random.randn(num_sleeps), 0, 100
    ).astype("int")

    cycles_df_syn.n_naps = np.random.poisson(0.5, size=num_sleeps)

    ms_hour_normal = lambda loc, scale: np.clip(
        (
            3600 * 1000 * np.random.normal(loc=loc, scale=scale, size=(num_sleeps,))
        ).astype("int"),
        0,
        None,
    )

    cycles_df_syn.sleep_need_baseline = ms_hour_normal(8, 1)
    cycles_df_syn.sleep_debt = ms_hour_normal(1, 0.2)
    cycles_df_syn.sleep_need_strain = ms_hour_normal(0.1, 0.1)
    cycles_df_syn.sleep_need_total = ms_hour_normal(8, 1)
    cycles_df_syn.sleep_quality_duration = ms_hour_normal(6, 1)

    cycles_df_syn.resting_hr = np.clip(
        np.random.normal(loc=60, scale=5, size=(num_sleeps,)).astype("int"), 0, None
    )
    cycles_df_syn.avg_hr = np.clip(
        np.random.normal(loc=70, scale=5, size=(num_sleeps,)).astype("int"), 0, None
    )
    cycles_df_syn.kilojoules = np.clip(
        np.random.normal(loc=9000, scale=1000, size=(num_sleeps,)), 0, None
    )
    cycles_df_syn.max_hr = np.clip(
        np.random.normal(loc=150, scale=10, size=(num_sleeps,)).astype("int"),
        0,
        200,
    )
    cycles_df_syn.strain_score = np.clip(
        np.random.normal(loc=12, scale=2, size=(num_sleeps,)), 0, 21
    )
    cycles_df_syn.rMSSD = np.clip(
        np.random.normal(loc=0.07, scale=0.01, size=(num_sleeps,)), 0, None
    )

    return cycles_df_syn


def create_fake_metrics_df(start_date, end_date):
    """Create fake metrics dataframe. Each row in the dataframe is a single
    day.

    :param start_date: the start date of the synthetic data as a string formatted as YYYY-MM-DD
    :type start_date: str
    :param end_date: the end date of the synthetic data as a string formatted as YYYY-MM-DD
    :type end_date: str
    :return: metrics dataframe
    :rtype: pd.DataFrame
    """

    start_day = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_day = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    n_rows = (end_day - start_day).days

    metrics_df_syn = pd.DataFrame(
        columns=[
            "id",
            "day",
            "RESPIRATORY_RATE.current_value",
            "RESPIRATORY_RATE.current_deviation",
            "BLOOD_OXYGEN.current_value",
            "BLOOD_OXYGEN.current_deviation",
            "RHR.current_value",
            "RHR.current_deviation",
            "HRV.current_value",
            "HRV.current_deviation",
            "SKIN_TEMPERATURE_CELSIUS.current_value",
            "SKIN_TEMPERATURE_CELSIUS.current_deviation",
            "SKIN_TEMPERATURE_FAHRENHEIT.current_value",
            "SKIN_TEMPERATURE_FAHRENHEIT.current_deviation",
        ]
    )

    metrics_df_syn.id = np.random.choice(range(1000), size=(n_rows,), replace=False)

    metrics_df_syn.day = pd.date_range(start_day, end_day - datetime.timedelta(days=1), freq="D")

    metrics_df_syn["RESPIRATORY_RATE.current_value"] = np.clip(
        np.random.normal(loc=15, scale=1, size=(n_rows,)), 0, None
    )

    metrics_df_syn["RESPIRATORY_RATE.current_deviation"] = np.random.normal(
        loc=0, scale=0.5, size=(n_rows,)
    )
    metrics_df_syn["BLOOD_OXYGEN.current_value"] = np.clip(
        np.round(np.random.normal(loc=96, scale=1, size=(n_rows,))), 0, 100
    )
    metrics_df_syn["BLOOD_OXYGEN.current_deviation"] = np.clip(
        np.round(np.random.normal(loc=0, scale=0.8, size=(n_rows,))), -3, 3
    )
    metrics_df_syn["RHR.current_value"] = np.clip(
        np.round(np.random.normal(loc=60, scale=3, size=(n_rows,))), 0, None
    )
    metrics_df_syn["RHR.current_deviation"] = np.clip(
        np.round(np.random.normal(loc=0, scale=0.8, size=(n_rows,))), -3, 3
    )
    metrics_df_syn["HRV.current_value"] = np.clip(
        np.round(np.random.normal(loc=70, scale=3, size=(n_rows,))), 0, None
    )
    metrics_df_syn["HRV.current_deviation"] = np.clip(
        np.round(np.random.normal(loc=0, scale=4, size=(n_rows,))), -3, 3
    )
    metrics_df_syn["SKIN_TEMPERATURE_CELSIUS.current_value"] = np.clip(
        np.random.normal(loc=33, scale=1.0, size=(n_rows,)), 0, None
    )
    metrics_df_syn["SKIN_TEMPERATURE_CELSIUS.current_deviation"] = np.clip(
        np.random.normal(loc=0, scale=0.5, size=(n_rows,)), -3, 3
    )
    metrics_df_syn["SKIN_TEMPERATURE_FAHRENHEIT.current_value"] = (
        9 / 5 * metrics_df_syn["SKIN_TEMPERATURE_CELSIUS.current_value"] + 32
    )
    metrics_df_syn["SKIN_TEMPERATURE_FAHRENHEIT.current_deviation"] = (
        9 / 5 * metrics_df_syn["SKIN_TEMPERATURE_CELSIUS.current_deviation"]
    )

    return metrics_df_syn


def create_fake_hr_df(start_date, end_date, sleeps_syn):
    """Create a fake heart rate dataframe. This is a dataframe with
    a row for every seven seconds of the day. Though the heart rate is
    "recorded" throughout the entire day, this function depends on the
    sleeps_syn dataframe to determine when the user is asleep and when
    they are awake. The heart rate is set based on whether the user
    is asleep in a nap, asleep at night, or awake.

    :param start_date: The start date of the synthetic data as a string formatted as YYYY-MM-DD
    :type start_date: str
    :param end_date: The end date of the synthetic data as a string formatted as YYYY-MM-DD
    :type end_date: str
    :param sleeps_syn: A dataframe with a row for every sleep event
    :type sleeps_syn: pd.DataFrame
    :return: A dataframe of heart rates with a row for every seven seconds
        of the day
    :rtype: pd.DataFrame
    """

    start_day_orig = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_day = start_day_orig.replace(tzinfo=dateutil.tz.gettz("US/Pacific"))
    end_day_orig = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    end_day = end_day_orig.replace(tzinfo=dateutil.tz.gettz("US/Pacific"))
    start_ts = start_day.timestamp()

    N = int((end_day - start_day).days * 24 * 60 * 60 / 7)

    hr_df_syn = pd.DataFrame(
        np.empty((N, 2)) * np.nan, columns=["heart_rate", "timestamp"]
    )

    heart_rate = np.random.normal(loc=80, scale=20, size=(N,)).astype("int")
    hr_df_syn.heart_rate = heart_rate

    hr_df_syn.timestamp = pd.date_range(
        start_day_orig, end_day_orig, freq="7S"
    )[:-1]

    hr_df_syn.timestamp = hr_df_syn.timestamp.dt.tz_localize(
        "US/Pacific", nonexistent="shift_forward"
    )

    for lower, upper, is_nap in tqdm(
        zip(
            sleeps_syn.time_lower_bound,
            sleeps_syn.time_upper_bound,
            sleeps_syn.is_nap,
        )
    ):
        lower_idx = int((lower.timestamp() - start_ts) // 7)
        upper_idx = int((upper.timestamp() - start_ts) // 7)

        decrement_val = 20 if is_nap else 40

        hr_df_syn.loc[lower_idx:upper_idx, ["heart_rate"]] -= decrement_val

    return hr_df_syn


def create_fake_sleeps_df(start_date, end_date):
    """Create a fake sleeps dataframe. This is a dataframe with a row
    for every sleep event (nap or night sleep).

    :param start_date: The start date of the synthetic data as a string formatted as YYYY-MM-DD
    :type start_date: str
    :param end_date: The end date of the synthetic data as a string formatted as YYYY-MM-DD
    :type end_date: str
    :return: A dataframe of sleep events
    :rtype: pd.DataFrame
    """

    columns = [
        "cycle_id",
        "sleep_id",
        "cycles_count",
        "disturbance_count",
        "time_upper_bound",
        "time_lower_bound",
        "is_nap",
        "in_bed_duration",
        "light_sleep_duration",
        "latency_duration",
        "no_data_duration",
        "rem_sleep_duration",
        "respiratory_rate",
        "sleep_score",
        "sleep_efficiency",
        "sleep_consistency",
        "sws_duration",
        "wake_duration",
        "quality_duration",
    ]
    sleeps_syn = pd.DataFrame(columns=columns)
    start_day = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_day = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    num_sleeps = (end_day - start_day).days

    sleeps_syn.cycle_id = np.random.choice(
        range(1000), size=(num_sleeps,), replace=False
    )
    sleeps_syn.sleep_id = np.random.choice(
        range(1000), size=(num_sleeps,), replace=False
    )

    sleeps_syn.cycles_count = np.random.poisson(1, size=(num_sleeps,))
    sleeps_syn.disturbance_count = np.random.poisson(12, size=(num_sleeps,))
    sleeps_syn.is_nap = ([False, True] * num_sleeps)[:num_sleeps]

    dur = []
    for i in range(num_sleeps):
        dur.append(np.clip(np.random.normal(loc=8.0), 0, 14))
        dur.append(np.clip(np.random.normal(loc=1.0, scale=0.5), 0.2, 6))

    sleeps_syn.in_bed_duration = dur[:num_sleeps]
    sleeps_syn.light_sleep_duration = sleeps_syn.in_bed_duration * 0.5
    sleeps_syn.latency_duration = 0
    sleeps_syn.no_data_duration = 0
    sleeps_syn.rem_sleep_duration = sleeps_syn.in_bed_duration * 0.1
    sleeps_syn.sws_duration = sleeps_syn.in_bed_duration * 0.3
    sleeps_syn.wake_duration = sleeps_syn.in_bed_duration * 0.1
    sleeps_syn.quality_duration = sleeps_syn.in_bed_duration * 0.9
    sleeps_syn.respiratory_rate = np.random.normal(loc=15, size=(num_sleeps,))
    sleeps_syn.sleep_score = np.random.randint(0, 100, size=(num_sleeps,))
    sleeps_syn.sleep_efficiency = 0.90
    sleeps_syn.sleep_consistency = np.random.uniform(0, 1, size=(num_sleeps,))

    # create start/end times
    cur_timestamp = start_day.timestamp()

    sleep_starts = []
    sleep_ends = []

    # make sleep start/end correspond with duration
    for i in range(sleeps_syn.shape[0]):
        try:
            offset = int(sleeps_syn.iloc[i * 2].in_bed_duration * 3600)
            sleep_starts.append(cur_timestamp)
            sleep_ends.append(cur_timestamp + offset)

            offset = int(sleeps_syn.iloc[i * 2 + 1].in_bed_duration * 3600)
            sleep_starts.append(cur_timestamp + 14 * 3600)
            sleep_ends.append(cur_timestamp + 14 * 3600 + offset)
            cur_timestamp += 24 * 3600
        except:
            pass  # index error

    sleep_starts = [
        datetime.datetime.fromtimestamp(ts, tz=dateutil.tz.gettz("US/Pacific"))
        for ts in sleep_starts
    ]
    sleep_ends = [
        datetime.datetime.fromtimestamp(ts, tz=dateutil.tz.gettz("US/Pacific"))
        for ts in sleep_ends
    ]
    sleeps_syn.time_lower_bound = sleep_starts[:num_sleeps]
    sleeps_syn.time_upper_bound = sleep_ends[:num_sleeps]

    return sleeps_syn
