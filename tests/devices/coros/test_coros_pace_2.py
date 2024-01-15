from datetime import datetime, timedelta

import pytest
from dateutil import parser

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_coros_pace_2_synthetic(real):
    start_dates = [datetime(2009, 11, 30), datetime(2021, 4, 4), datetime(2022, 6, 10)]
    end_dates = [datetime(2009, 12, 1), datetime(2021, 4, 5), datetime(2022, 6, 11)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "coros/coros_pace_2",
            synthetic_start_date=datetime.strftime(start_date, "%Y-%m-%d"),
            synthetic_end_date=datetime.strftime(end_date, "%Y-%m-%d"),
        )

        if real:
            wearipedia._authenticate_device("coros/coros_pace_2", device)

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
    exercise_time = device.get_data(
        "exercise_time",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    heart_rate = device.get_data(
        "heart_rate",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    sports = device.get_data(
        "sports",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    active_energy = device.get_data(
        "active_energy",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )

    sleep_arr = []
    for ele in sleep:
        sleep_time = ele["data"]["statisticData"]["dayDataList"][0]["sleepData"][
            "totalSleepTime"
        ]
        assert (
            sleep_time < 1440
        ), f"Sleep time should be less than 1440 minutes but was {sleep_time}"
        sleep_arr.append(sleep_time)
    assert len(sleep_arr) > 0, "No sleep data found"

    steps_arr = []
    for ele in steps:
        step_count = ele["data"]["statisticData"]["dayDataList"][0]["step"]
        assert (
            step_count < 100000
        ), f"Step count should be less than 100000 but was {step_count}"
        steps_arr.append(step_count)
    assert len(steps_arr) > 0, "No step data found"

    exercise_time_arr = []
    for ele in exercise_time:
        exercise_duration = ele["data"]["statisticData"]["dayDataList"][0]["motionTime"]
        assert (
            exercise_duration < 1440
        ), f"Exercise duration should be less than 1440 minutes but was {exercise_duration}"
        exercise_time_arr.append(exercise_duration)
    assert len(exercise_time_arr) > 0, "No exercise time data found"

    heart_rate_arr = []
    for ele in heart_rate:
        avg_heart_rate = ele["data"]["statisticData"]["dayDataList"][0][
            "heartRateData"
        ]["avgHeartRate"]
        assert (
            avg_heart_rate < 121
        ), f"Avg. heart rate should be less than 121 but was {avg_heart_rate}"
        heart_rate_arr.append(avg_heart_rate)
    assert len(heart_rate_arr) > 0, "No heart rate data found"

    sports_arr = []
    for ele in sports:
        duration = ele["data"][0]["duration"]
        assert (
            duration < 1440
        ), f"Sports duration should be less than 1440 minutes but was {duration}"
        sports_arr.append(duration)
    assert len(sports_arr) > 0, "No sports data found"

    active_energy_arr = []
    for ele in active_energy:
        calorie_count = ele["data"]["statisticData"]["dayDataList"][0]["calorie"]
        assert (
            calorie_count < 10000
        ), f"Calorie count should be less than 10000 but was {calorie_count}"
        active_energy_arr.append(calorie_count)
    assert len(active_energy_arr) > 0, "No active energy data found"
