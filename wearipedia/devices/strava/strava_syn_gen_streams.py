import numpy as np
from scipy.ndimage.filters import uniform_filter1d


def generate_synthetic_heart_rate_data(
    size=np.random.randint(60, 1800), min_hr=60, max_hr=160, window_size=10
):
    heart_rate_data = {
        "heartrate": {
            "data": [],
            "series_type": "time",
            "original_size": size,
            "resolution": "high",
        },
        "time": {
            "data": list(range(size)),
            "series_type": "time",
            "original_size": size,
            "resolution": "high",
        },
    }

    raw_data = np.random.randint(min_hr, max_hr, size)
    smoothed_data = uniform_filter1d(raw_data, size=window_size)

    for hr in smoothed_data:
        heart_rate_data["heartrate"]["data"].append(hr)

    return [heart_rate_data]


def return_streams_syn(data_type):
    if data_type == "heartrate":
        return generate_synthetic_heart_rate_data()
