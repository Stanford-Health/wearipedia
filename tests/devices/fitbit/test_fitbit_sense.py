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

        if real:
            wearipedia._authenticate_device("fitbit/fitbit_sense", device)

        helper_test(device, start_date, end_date, real)


def helper_test(device, start_synthetic, end_synthetic, real):
    sleep = device.get_data(
        "sleep",
        params={
            "start": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    steps = device.get_data(
        "steps",
        params={
            "start": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end": datetime.strftime(end_synthetic, "%Y-%m-%d"),
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

    rem = []
    for datapoint in sleep[0]["sleep"]:
        steps_arr.append(datapoint["value"])
        if "rem" in datapoint["levels"]["summary"]:
            rem.append(datapoint["levels"]["summary"]["rem"]["minutes"])
    assert (len(rem)) >= 1

    steps_arr = []
    for datapoint in steps[0]["activities-steps"]:
        steps_arr.append(datapoint["value"])
    assert (len(steps_arr)) >= 1

    light = []
    for datapoint in minutesLightlyActive[0]["activities-minutesLightlyActive"]:
        steps_arr.append(datapoint["value"])
    assert (len(light)) >= 1

    fair = []
    for datapoint in minutesFairlyActive[0]["activities-minutesFairlyActive"]:
        steps_arr.append(datapoint["value"])
    assert (len(fair)) >= 1

    very = []
    for datapoint in minutesVeryActive[0]["activities-minutesVeryActive"]:
        steps_arr.append(datapoint["value"])
    assert (len(very)) >= 1

    sedentary = []
    for datapoint in minutesSedentary[0]["activities-minutesSedentary"]:
        steps_arr.append(datapoint["value"])
    assert (len(sedentary)) >= 1

    distance_arr = []
    for datapoint in distance[0]["activities-distance"]:
        steps_arr.append(datapoint["value"])
    assert (len(distance_arr)) >= 1
