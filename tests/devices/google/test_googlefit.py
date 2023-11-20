from datetime import datetime

import numpy as np
import pandas as pd
import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_googlefit(real):

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
            "google/googlefit",
            start_date=np.datetime_as_string(start_date, unit="D"),
            end_date=np.datetime_as_string(end_date, unit="D"),
        )

        params = {"start_date": str(start_date), "end_date": str(end_date)}

        if real:
            wearipedia._authenticate_device("google/googlefit", device)

        steps = device.get_data("steps", params=params)
        heart_rate = device.get_data("heart_rate", params=params)
        sleep = device.get_data("sleep", params=params)
        heart_minutes = device.get_data("heart_minutes", params=params)
        blood_pressure = device.get_data("blood_pressure", params=params)
        blood_glucose = device.get_data("blood_glucose", params=params)
        body_temperature = device.get_data("body_temperature", params=params)
        calories_expended = device.get_data("calories_expended", params=params)
        activity_minutes = device.get_data("activity_minutes", params=params)
        height = device.get_data("height", params=params)
        oxygen_saturation = device.get_data("oxygen_saturation", params=params)
        menstruation = device.get_data("menstruation", params=params)
        speed = device.get_data("speed", params=params)
        weight = device.get_data("weight", params=params)
        distance = device.get_data("distance", params=params)

        steps_helper(steps)
        heart_rate_helper(heart_rate)
        sleep_helper(sleep)
        heart_minutes_helper(heart_minutes)
        blood_pressure_helper(blood_pressure)
        blood_glucose_helper(blood_glucose)
        body_temperature_helper(body_temperature)
        calories_expended_helper(calories_expended)
        activity_minutes_helper(activity_minutes)
        height_helper(height)
        oxygen_saturation_helper(oxygen_saturation)
        menstruation_helper(menstruation)
        speed_helper(speed)
        weight_helper(weight)
        distance_helper(distance)


def base_info(data):
    assert list(data[0].keys()) == [
        "startTimeMillis",
        "endTimeMillis",
        "dataset",
    ]
    assert isinstance(
        datetime.fromtimestamp(data[0]["startTimeMillis"] / 1000), datetime
    )
    assert isinstance(datetime.fromtimestamp(data[0]["endTimeMillis"] / 1000), datetime)
    assert isinstance(data[0]["dataset"][0]["dataSourceId"], str)


def point_base(data):
    assert isinstance(data[0]["dataset"][0]["point"][0]["startTimeNanos"], str)
    assert isinstance(data[0]["dataset"][0]["point"][0]["endTimeNanos"], str)
    assert isinstance(data[0]["dataset"][0]["point"][0]["dataTypeName"], str)
    assert isinstance(data[0]["dataset"][0]["point"][0]["originDataSourceId"], str)


def steps_helper(steps):
    for data in steps:
        base_info(data)
        if data[0]["dataset"][0]["point"] == []:
            continue
        point_base(data)
        if data[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][0]["intVal"], int
            )


def heart_rate_helper(heart_rate):
    for data in heart_rate:
        base_info(data)
        if data[0]["dataset"][0]["point"] == []:
            continue
        point_base(data)
        if data[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"], float
            )
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] > 0
            assert data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] > 0
            assert data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] > 0


def sleep_helper(sleep):
    for data in sleep:
        base_info(data)
        if data[0]["dataset"][0]["point"] == []:
            continue
        point_base(data)
        if data[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 24
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0


def heart_minutes_helper(heart_minutes):
    for data in heart_minutes:
        base_info(data)
        if data[0]["dataset"][0]["point"] == []:
            continue
        point_base(data)
        if data[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 1000
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0
            assert data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] <= 1000
            assert data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] >= 0


def blood_pressure_helper(blood_pressure):
    for data in blood_pressure:
        base_info(data)
        if data[0]["dataset"][0]["point"] == []:
            continue
        point_base(data)
        if data[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] > 0
            assert data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] > 0
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"], float
            )
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][3]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][3]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] > 0
            assert data[0]["dataset"][0]["point"][0]["value"][3]["fpVal"] > 0
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][4]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][4]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][4]["fpVal"] > 0
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][5]["intVal"], int
            )
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][6]["intVal"], int
            )


def blood_glucose_helper(blood_glucose):
    for data in blood_glucose:
        base_info(data)
        if data[0]["dataset"][0]["point"] == []:
            continue
        point_base(data)
        if data[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] >= 0
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] <= 300
            assert data[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] >= 0


def body_temperature_helper(data):
    for d in data:
        base_info(d)
        if d[0]["dataset"][0]["point"] == []:
            continue
        point_base(d)
        if d[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 100
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] <= 100
            assert d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] >= 0
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] <= 100
            assert d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] >= 0


def calories_expended_helper(cals):
    for data in cals:
        base_info(data)
        if data[0]["dataset"][0]["point"] == []:
            continue
        point_base(data)
        if data[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 100000
            assert data[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0


def activity_minutes_helper(data):
    for d in data:
        base_info(d)
        if d[0]["dataset"][0]["point"] == []:
            continue
        point_base(d)
        if d[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 1000
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0


def height_helper(data):
    for d in data:
        base_info(d)
        if d[0]["dataset"][0]["point"] == []:
            continue
        point_base(d)
        if d[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 300
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] <= 300
            assert d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] >= 0
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] <= 300
            assert d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] >= 0


def oxygen_saturation_helper(data):
    for d in data:
        base_info(d)
        if d[0]["dataset"][0]["point"] == []:
            continue
        point_base(d)
        if d[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 150
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] <= 150
            assert d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] >= 0
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] <= 150
            assert d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] >= 0


def menstruation_helper(data):
    for d in data:
        base_info(d)
        if d[0]["dataset"][0]["point"] == []:
            continue
        point_base(d)
        if d[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(d[0]["dataset"][0]["point"][0]["value"][0]["intVal"], int)
            assert d[0]["dataset"][0]["point"][0]["value"][0]["intVal"] <= 4
            assert d[0]["dataset"][0]["point"][0]["value"][0]["intVal"] > 0


def speed_helper(data):
    for d in data:
        base_info(d)
        if d[0]["dataset"][0]["point"] == []:
            continue
        point_base(d)
        if d[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 100
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] <= 100
            assert d[0]["dataset"][0]["point"][0]["value"][1]["fpVal"] >= 0
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] <= 100
            assert d[0]["dataset"][0]["point"][0]["value"][2]["fpVal"] >= 0


def weight_helper(data):
    for d in data:
        base_info(d)
        if d[0]["dataset"][0]["point"] == []:
            continue
        point_base(d)
        if d[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 1000
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0


def distance_helper(data):
    for d in data:
        base_info(d)
        if d[0]["dataset"][0]["point"] == []:
            continue
        point_base(d)
        if d[0]["dataset"][0]["point"][0]["value"] != []:
            assert isinstance(
                d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"], float
            )
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] <= 100000
            assert d[0]["dataset"][0]["point"][0]["value"][0]["fpVal"] >= 0
