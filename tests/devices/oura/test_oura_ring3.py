from datetime import datetime, timedelta

import pytest
from dateutil import parser

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_oura_ring3_synthetic(real):
    start_dates = [datetime(2009, 11, 30), datetime(2021, 4, 4), datetime(2022, 6, 10)]
    end_dates = [datetime(2009, 12, 1), datetime(2021, 4, 5), datetime(2022, 6, 11)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "oura/oura_ring3",
            synthetic_start_date=datetime.strftime(start_date, "%Y-%m-%d"),
            synthetic_end_date=datetime.strftime(end_date, "%Y-%m-%d"),
        )

        if real:
            wearipedia._authenticate_device("oura/oura_ring3", device)

        helper_test(device, start_date, end_date, real)


def helper_test(device, start_synthetic, end_synthetic, real):
    sleep = device.get_data(
        "sleep",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )

    daily_activity = device.get_data(
        "daily_activity",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    activity = device.get_data(
        "activity",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    ideal_bedtime = device.get_data(
        "ideal_bedtime",
        params={
            "start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )
    readiness = device.get_data(
        "readiness",
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

    deep = []
    light = []
    rem = []
    awake = []
    dates = []
    for elem in sleep:
        deep_hours = elem["deep"] / 60 / 60
        deep.append(deep_hours)  # sec -> min -> hour

        assert (
            deep_hours < 8
        ), f"Deep sleep hours should be less than 8 but was {deep_hours}"
        assert (
            deep_hours > 0
        ), f"Deep sleep hours should be greater than 0 but was {deep_hours}"

        light_hours = elem["light"] / 60 / 60
        light.append(light_hours)
        rem_hours = elem["rem"] / 60 / 60
        rem.append(rem_hours)
        awake_hours = elem["awake"] / 60 / 60
        awake.append(awake_hours)
        dates.append(elem["summary_date"])

    assert len(deep) != 0, "Number of deep sleep data points should be greater than 0"
    assert len(rem) != 0, "Number of REM sleep data points should be greater than 0"
    assert len(light) != 0, "Number of light sleep data points should be greater than 0"
    assert len(awake) != 0, "Number of awake sleep data points should be greater than 0"
    assert len(dates) != 0, "Number of dates should be greater than 0"

    bpm = []
    for elem in heart_rate:
        bpm_value = elem["bpm"]
        bpm.append(bpm_value)
        assert (
            bpm_value < 200
        ), f"Heart rate should be less than 200 but was {bpm_value}"

    daily_activiy_score = []
    for elem in daily_activity:
        score = elem["score"]
        daily_activiy_score.append(score)
        assert (
            score < 100
        ), f"Daily activity score should be less than 100 but was {score}"

    cal_total = []
    for elem in activity:
        cal_total_value = elem["cal_total"]
        cal_total.append(cal_total_value)
        assert (
            cal_total_value < 5000
        ), f"Calories total should be less than 5000 but was {cal_total_value}"

    score_temperature = []
    for elem in readiness:
        temperature_score = elem["score_temperature"]
        score_temperature.append(temperature_score)
        assert (
            temperature_score < 100
        ), f"Temperature score should be less than 100 but was {temperature_score}"

    assert (
        len(ideal_bedtime[0]["status"]) > 0
    ), "Ideal bedtime status should not be empty"
