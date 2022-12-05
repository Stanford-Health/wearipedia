from datetime import datetime

import numpy as np

import wearipedia


def test_verity_sense_synthetic():
    # we test with default params

    start_synthetic = np.datetime64("2022-03-01")
    end_synthetic = np.datetime64("2022-06-17")

    device = wearipedia.get_device(
        "polar/verity_sense",
        params={
            "synthetic_start_date": "2022-03-01",
            "synthetic_end_date": "2022-06-17",
        },
    )

    data = device.get_data("sessions")

    # assert we have the right range of sessions
    assert (
        int(
            (np.datetime64(list(data.keys())[0]) - start_synthetic)
            / np.timedelta64(1, "D")
        )
        >= 0
    ), f"Expected first entry to be after 2022-03-01, but got {list(data.keys())[0]}"
    assert (
        int(
            (np.datetime64(list(data.keys())[-1]) - end_synthetic)
            / np.timedelta64(1, "D")
        )
        <= 0
    ), f"Expected last entry to be before 2022-06-17, but got {list(data.keys())[-1]}"
    # assert we have the right amount of heart rate points for duration
    for key in data.keys():
        assert (
            len(data[key]["heart_rates"]) == data[key]["minutes"] * 60
        ), f"Expected {data[key]['minutes']*60} heart rates, got {len(data[key]['heart_rates'])}"
