from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter
from tqdm import tqdm

__all__ = ["create_synth"]


def lerp(x1, x2, t):
    return t * x2 + (1 - t) * x1


base_keypoints = [100] * 4 + [120] * 4 + [130] * 8 + [120] * 4 + [100] * 4


def create_synth(start_day_str, end_day_str):
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

    egvs = []
    glucoses = gaussian_filter(glucoses, 2, mode="constant")

    for dt_obj, glucose in zip(datetimes[::-1], glucoses[::-1]):
        egvs.append(
            {
                "systemTime": dt_obj.strftime("%Y-%m-%dT%H:%M:%S"),
                # this is supposed to be timezone shift
                "displayTime": dt_obj.strftime("%Y-%m-%dT%H:%M:%S"),
                "value": glucose,
                "realtimeValue": glucose,
                "smoothedValue": None,
                "status": None,
                "trend": "flat",
                "trendRate": np.round(np.random.normal(), 2),
            }
        )

    out = {"unit": "mg/dL", "rateUnit": "mg/dL/min", "egvs": egvs}

    return out
