import numpy as np
from scipy.ndimage.filters import uniform_filter1d


def generate_synthetic_heart_rate_data(
    size=np.random.randint(60, 1800), min_hr=60, max_hr=160, window_size=10
):
    """
    This function generates synthetic heart rate data.

    :param size: The number of data points to generate.
    :type size: int
    :param min_hr: The minimum heart rate value to generate.
    :type min_hr: int
    :param max_hr: The maximum heart rate value to generate.
    :type max_hr: int
    :param window_size: The size of the window to use for smoothing.
    :type window_size: int
    :return: A list of dictionaries containing the generated data.
    :rtype: list
    """
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
    """
    This function returns synthetic data streams.

    :param data_type: The type of data to generate.
    :type data_type: str
    :return: The generated data streams.
    :rtype: list
    """
    if data_type == "heartrate":
        return generate_synthetic_heart_rate_data()
