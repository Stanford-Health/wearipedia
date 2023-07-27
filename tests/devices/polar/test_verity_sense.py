from datetime import datetime

import numpy as np
import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_verity_sense(real):
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
            "polar/verity_sense",
            start_date=np.datetime_as_string(start_date, unit="D"),
            end_date=np.datetime_as_string(end_date, unit="D"),
        )

        if real:
            wearipedia._authenticate_device("polar/verity_sense", device)

        data = device.get_data("sessions")

        # run tests for device
        helper(data, start_date, end_date, real)


def helper(data, start_synthetic, end_synthetic, real):
    if real:
        for key in data.keys():
            assert (
                start_synthetic < np.datetime64(key) < end_synthetic
            ), f"expected all data to be between start and end, but got {key}, which is not between {start_synthetic} and {end_synthetic}"

    else:
        # assert we have the right range of sessions
        assert (
            int(
                (np.datetime64(list(data.keys())[0]) - start_synthetic)
                / np.timedelta64(1, "D")
            )
            >= 0
        ), f"Expected first entry to be after {start_synthetic}, but got {list(data.keys())[0]}"
        assert (
            int(
                (np.datetime64(list(data.keys())[-1]) - end_synthetic)
                / np.timedelta64(1, "D")
            )
            <= 0
        ), f"Expected last entry to be before {end_synthetic} but got {list(data.keys())[-1]}"

    # assert we have the right amount of heart rate points for duration
    # NOTE: we allow for a tolerance of 20 measurements
    for key in data.keys():
        assert (
            abs(len(data[key]["heart_rates"]) - data[key]["minutes"] * 60) < 20
        ), f"Expected {data[key]['minutes']*60} heart rates, got {len(data[key]['heart_rates'])}"

    # assert the calorie counts are reasonable
    for key in data.keys():
        assert (
            0 <= data[key]["calories"] <= 1000
        ), f"Calories burned should be between 0 and 1000, but received {data[key]['calories']}"

    # assert the heart rate values are reasonable
    for key in data.keys():
        for hr in data[key]["heart_rates"]:
            assert (
                40 <= hr <= 200
            ), f"Heart rate should be between 40 and 200, but received {hr}"
