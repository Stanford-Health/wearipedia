from datetime import datetime

import numpy as np
import pandas as pd
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
            "underarmour/myfitnesspal",
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
            wearipedia._authenticate_device("underarmour/myfitnesspal", device)

        goals = device.get_data("goals", params=params)
        daily_summary = device.get_data("daily_summary", params=params)
        exercises_cardio = device.get_data("exercises_cardio", params=params)
        excerises_strength = device.get_data("exercises_strength", params=params)
        lunch = device.get_data("lunch", params=params)
        breakfast = device.get_data("breakfast", params=params)
        dinner = device.get_data("dinner", params=params)
        snacks = device.get_data("snacks", params=params)

        vitals_helper(goals)
        vitals_helper(daily_summary)
        cardio_exercise_helper(exercises_cardio)
        strength_exercise_helper(excerises_strength)
        meal_helper(lunch)
        meal_helper(breakfast)
        meal_helper(dinner)
        meal_helper(snacks)


def vitals_helper(data):
    for d in data:
        # Check keys are present
        assert list(d.keys()) == [
            "calories",
            "carbohydrates",
            "fat",
            "protein",
            "sodium",
            "sugar",
            "date",
        ]

        # Check data types and value ranges
        assert isinstance(d["calories"], float)
        assert d["calories"] >= 0.0 and d["calories"] <= 10000.0

        assert isinstance(d["carbohydrates"], float)
        assert d["carbohydrates"] >= 0.0 and d["carbohydrates"] <= 1000.0

        assert isinstance(d["fat"], float)
        assert d["fat"] >= 0.0 and d["fat"] <= 1000.0

        assert isinstance(d["protein"], float)
        assert d["protein"] >= 0.0 and d["protein"] <= 1000.0

        assert isinstance(d["sodium"], float)
        assert d["sodium"] >= 0.0 and d["sodium"] <= 10000.0

        assert isinstance(d["sugar"], float)
        assert d["sugar"] >= 0.0 and d["sugar"] <= 1000.0

        assert isinstance(d["date"], pd.Timestamp)


def cardio_exercise_helper(data):
    for d in data:
        # Check keys are present=
        assert list(d[0].keys()) == ["day"]
        assert list(d[1].keys()) == ["name", "nutrition_information"]
        assert list(d[1]["nutrition_information"].keys()) == [
            "minutes",
            "calories burned",
        ]

        # Check data types and value ranges
        assert isinstance(d[0]["day"], pd.Timestamp)

        assert isinstance(d[1]["name"], str)

        assert isinstance(d[1]["nutrition_information"]["minutes"], int)
        assert (
            d[1]["nutrition_information"]["minutes"] >= 0
            and d[1]["nutrition_information"]["minutes"] <= 1440
        )

        assert isinstance(d[1]["nutrition_information"]["calories burned"], float)
        assert (
            d[1]["nutrition_information"]["calories burned"] >= 0.0
            and d[1]["nutrition_information"]["calories burned"] <= 1000.0
        )


def strength_exercise_helper(data):
    for d in data:
        # Check keys are present
        assert list(d[0].keys()) == ["date"]
        assert all(
            ["name" in entry and "nutrition_information" in entry for entry in d[1:]]
        )
        assert all(
            [
                "sets" in entry["nutrition_information"]
                and "reps/set" in entry["nutrition_information"]
                and "weight/set" in entry["nutrition_information"]
                for entry in d[1:]
            ]
        )

        # Check data types and value ranges
        assert isinstance(d[0]["date"], pd.Timestamp)

        for entry in d[1:]:
            assert isinstance(entry["name"], str)
            assert isinstance(entry["nutrition_information"]["sets"], float)
            assert entry["nutrition_information"]["sets"] >= 0.0
            assert isinstance(entry["nutrition_information"]["reps/set"], float)
            assert entry["nutrition_information"]["reps/set"] >= 0.0
            assert isinstance(entry["nutrition_information"]["weight/set"], float)
            assert entry["nutrition_information"]["weight/set"] >= 0.0


def meal_nutritions(data):
    assert isinstance(data["calories"], float)
    assert data["calories"] >= 0

    assert isinstance(data["carbohydrates"], float)
    assert data["carbohydrates"] >= 0

    assert isinstance(data["fat"], float)
    assert data["fat"] >= 0

    assert isinstance(data["protein"], float)
    assert data["protein"] >= 0

    assert isinstance(data["sodium"], float)
    assert data["sodium"] >= 0

    assert isinstance(data["sugar"], float)
    assert data["sugar"] >= 0


def meal_helper(data):
    for d in data:
        d1 = d[0]
        print(d1)
        assert list(d1.keys()) == ["day"]
        assert isinstance(d1["day"], pd.Timestamp)

        d2 = d[1]
        assert list(d2.keys()) == ["name", "nutrition_information", "totals"]
        assert isinstance(d2["name"], str)

        nutrition_data = d2["nutrition_information"]
        assert list(nutrition_data.keys()) == [
            "calories",
            "carbohydrates",
            "fat",
            "protein",
            "sodium",
            "sugar",
        ]

        meal_nutritions(nutrition_data)

        totals_data = d2["totals"]

        meal_nutritions(totals_data)
