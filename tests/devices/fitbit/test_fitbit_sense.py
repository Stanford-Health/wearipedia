from datetime import datetime, timedelta

import pytest
from dateutil import parser

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_fitbit_sense(real):
    start_dates = [datetime(2009, 11, 30), datetime(2021, 4, 4), datetime(2022, 6, 10)]
    end_dates = [datetime(2009, 12, 1), datetime(2021, 4, 5), datetime(2022, 6, 11)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "fitbit/fitbit_sense",
            synthetic_start_date=datetime.strftime(start_date, "%Y-%m-%d"),
            synthetic_end_date=datetime.strftime(end_date, "%Y-%m-%d"),
        )
        """
        if real:
            wearipedia._authenticate_device("fitbit/fitbit_sense", device)
        """
        helper_test(device, start_date, end_date, real)


def helper_test(device, start_synthetic, end_synthetic, real):
    sleep = device.get_data(
        "sleep",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )

    steps = device.get_data(
        "steps",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    minutesVeryActive = device.get_data(
        "minutesVeryActive",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    minutesLightlyActive = device.get_data(
        "minutesLightlyActive",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    minutesFairlyActive = device.get_data(
        "minutesFairlyActive",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    distance = device.get_data(
        "distance",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    minutesSedentary = device.get_data(
        "minutesSedentary",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    minutesAsleep = []
    for datapoint in sleep[0]["sleep"]:
        minutesAsleep.append(datapoint["minutesAsleep"])
    assert len(minutesAsleep) >= 1, "Number of sleep data points should be at least 1"
    assert (
        sum(minutesAsleep) / len(minutesAsleep) < 800
    ), f"Average minutes asleep should be less than 800 but was {sum(minutesAsleep) / len(minutesAsleep)}"

    steps_arr = []
    for datapoint in steps[0]["activities-steps"]:
        steps_arr.append(datapoint["value"])
    assert len(steps_arr) >= 1, "Number of steps data points should be at least 1"
    assert (
        sum(steps_arr) / len(steps_arr) < 20000
    ), f"Average steps should be less than 20000 but was {sum(steps_arr) / len(steps_arr)}"

    light = []
    for datapoint in minutesLightlyActive[0]["activities-minutesLightlyActive"]:
        light.append(datapoint["value"])
        assert (
            datapoint["value"] < 1440
        ), f"Value should be less than 1440 but was {datapoint['value']}"
    assert len(light) >= 1, "Number of light activity data points should be at least 1"

    fair = []
    for datapoint in minutesFairlyActive[0]["activities-minutesFairlyActive"]:
        fair.append(datapoint["value"])
        assert (
            datapoint["value"] < 1440
        ), f"Value should be less than 1440 but was {datapoint['value']}"
    assert (
        len(fair) >= 1
    ), "Number of fairly active minutes data points should be at least 1"

    very = []
    for datapoint in minutesVeryActive[0]["activities-minutesVeryActive"]:
        very.append(datapoint["value"])
        assert (
            datapoint["value"] < 1440
        ), f"Value should be less than 1440 but was {datapoint['value']}"
    assert (
        len(very) >= 1
    ), "Number of very active minutes data points should be at least 1"

    sedentary = []
    for datapoint in minutesSedentary[0]["activities-minutesSedentary"]:
        sedentary.append(datapoint["value"])
        assert (
            datapoint["value"] < 1440
        ), f"Value should be less than 1440 but was {datapoint['value']}"
    assert (
        len(sedentary) >= 1
    ), "Number of sedentary minutes data points should be at least 1"

    distance_arr = []
    for datapoint in distance[0]["activities-distance"]:
        distance_arr.append(datapoint["value"])
    assert (
        sum(distance_arr) / len(distance_arr) < 30
    ), f"Average distance should be less than 30 but was {sum(distance_arr) / len(distance_arr)}"
    assert len(distance_arr) >= 1, "Number of distance data points should be at least 1"
