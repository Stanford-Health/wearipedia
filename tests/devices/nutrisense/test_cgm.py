from datetime import datetime, timedelta

import numpy as np
import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_nutrisense(real):
    start_dates = [
        np.datetime64("2009-11-15"),
        np.datetime64("2021-04-01"),
        np.datetime64("2022-06-10"),
    ]
    end_dates = [
        np.datetime64("2010-02-01"),
        np.datetime64("2021-06-20"),
        np.datetime64("2022-12-10"),
    ]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "nutrisense/cgm",
            synthetic_start_date=np.datetime_as_string(start_date, unit="D"),
            synthetic_end_date=np.datetime_as_string(end_date, unit="D"),
        )

        if real:
            wearipedia._authenticate_device("nutrisense/cgm", device)

        summary = device.get_data("summary")
        scores = device.get_data("scores")
        statistics = device.get_data("statistics")
        data = device.get_data("continuous")

        bound = end_date + np.timedelta64(3, "D")
        # run tests for device
        helper(data, start_date, bound, real)


def helper(data, start_synthetic, end_synthetic, real):
    for e in data:
        assert (
            start_synthetic <= np.datetime64(e["x"]) <= end_synthetic
        ), f"expected all data to be between start and end, but got {np.datetime64(e['x'])}, which is not between {start_synthetic} and {end_synthetic}"
