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
        deep.append(elem["deep"] / 60 / 60)  # sec -> min -> hour

        assert elem["deep"] / 60 / 60 < 8
        assert elem["deep"] / 60 / 60 > 0

        light.append(elem["light"] / 60 / 60)
        rem.append(elem["rem"] / 60 / 60)
        awake.append(elem["awake"] / 60 / 60)
        dates.append(elem["summary_date"])

    assert len(deep) != 0
    assert len(rem) != 0
    assert len(light) != 0
    assert len(awake) != 0
    assert len(dates) != 0

    bpm = []
    for elem in heart_rate:
        bpm.append(elem["bpm"])
        assert elem["bpm"] < 200

    daily_activiy_score = []
    for elem in daily_activity:
        daily_activiy_score.append(elem["score"])
        assert elem["score"] < 100

    cal_total = []
    for elem in activity:
        cal_total.append(elem["cal_total"])
        assert elem["cal_total"] < 5000

    score_temperature = []
    for elem in readiness:
        score_temperature.append(elem["score_temperature"])
        assert elem["score_temperature"] < 100

    assert len(ideal_bedtime[0]["status"]) > 0
