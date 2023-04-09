from datetime import datetime

import numpy as np
import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_myfitnesspal(real):

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
            "myfitnesspal/myfitnesspal",
            start_date=np.datetime_as_string(start_date, unit="D"),
            end_date=np.datetime_as_string(end_date, unit="D"),
        )

        # This training id is only valid for arjo@stanford.edu
        params = {
            "start_date": str(start_date),
            "end_date": str(end_date),
            "training_id": "7472390363",
        }

        if real:
            wearipedia._authenticate_device("myfitnesspal/myfitnesspal", device)

        goals = device.get_data("goals", params=params)

#         goal_helper(goals)

# def goal_helper(data):

