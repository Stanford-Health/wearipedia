from datetime import datetime

import numpy as np

import wearipedia


def test_verity_sense_synthetic():
    start_dates = [
        np.datetime64("2009-11-15"),
        np.datetime64("2021-04-01"),
        np.datetime64("2022-06-10"),
    ]
    end_dates = [
        np.datetime64("2010-02-01"),
        np.datetime64("2021-06-20"),
        np.datetime64("2022-08-25"),
    ]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "polar/verity_sense",
            start_date=np.datetime_as_string(start_date, unit="D"),
            end_date=np.datetime_as_string(end_date, unit="D"),
        )

        data = device.get_data("sessions")

        # run tests for device
        helper(data, start_date, end_date)


def helper(data, start_synthetic, end_synthetic):
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
    for key in data.keys():
        assert (
            len(data[key]["heart_rates"]) == data[key]["minutes"] * 60
        ), f"Expected {data[key]['minutes']*60} heart rates, got {len(data[key]['heart_rates'])}"
    # assert the calorie counts are reasonable
    for key in data.keys():
        assert (
            data[key]["calories"] >= 0 and data[key]["calories"] <= 1000
        ), f"Calories burned should be between 0 and 1000, but received {data[key]['calories']}"
    # assert the heart rate values are reasonable
    for key in data.keys():
        for hr in data[key]["heart_rates"]:
            assert (
                hr >= 40 and hr <= 200
            ), f"Heart rate should be between 40 and 200, but received {hr}"
