from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter
from tqdm import tqdm

__all__ = ["create_synth_df"]


def lerp(x1, x2, t):
    return t * x2 + (1 - t) * x1


base_keypoints = [100] * 4 + [120] * 4 + [130] * 8 + [120] * 4 + [100] * 4


def create_synth_df(start_day_str, end_day_str):
    """Create a synthetic dataframe of CGM data.

    :param start_day_str: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_day_str: str
    :param end_day_str: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_day_str: str
    :return: the synthetic dataframe
    :rtype: pd.DataFrame
    """

    start_day = datetime.strptime(start_day_str, "%Y-%m-%d")
    end_day = datetime.strptime(end_day_str, "%Y-%m-%d")

    num_days = (end_day - start_day).days

    datetimes = []
    glucoses = []

    for day_offset in tqdm(range(num_days)):
        if day_offset != 0:
            overlap = keypoints[-1]
        keypoints = list(np.random.randn(24) * 10 + np.array(base_keypoints))
        if day_offset != 0:
            keypoints[0] = overlap

        keypoints = keypoints + [keypoints[0]]

        for minute_offset in range(0, 24 * 60, 5):
            minute = (
                start_day
                + timedelta(days=day_offset)
                + timedelta(minutes=minute_offset)
            )

            scaled_offset = minute_offset / 60

            k1 = keypoints[np.floor(scaled_offset).astype("int")]
            k2 = keypoints[np.ceil(scaled_offset).astype("int")]

            value = lerp(k1, k2, scaled_offset % 1)
            if value > 130:
                scaling = 30
            else:
                scaling = 15
            value += np.random.randn() * scaling

            datetimes.append(minute)
            glucoses.append(value)

    synth_df = pd.DataFrame()

    synth_df["datetime"] = datetimes
    synth_df["glucose_level"] = gaussian_filter(glucoses, 2, mode="constant")

    # unnecessary, included for some reason
    # synth_df['Time of Day'] = ['Day' if dt.hour in range(8, 20) else 'Night' for dt in datetimes]
    # synth_df['Rates of change'] = np.random.randn(synth_df.shape[0])
    # synth_df['Rates of change'].iloc[np.where(synth_df['Time of Day'] == 'Day')[0]] *= 3

    # take out some rows to create missing values

    missing_start = datetime.strptime("2022-04-06", "%Y-%m-%d") + timedelta(hours=14)
    missing_end = missing_start + timedelta(minutes=70)

    synth_df = synth_df.drop(
        np.where(
            np.logical_and(
                synth_df.datetime > missing_start, synth_df.datetime < missing_end
            )
        )[0]
    )

    return synth_df
