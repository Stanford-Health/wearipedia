import math
from datetime import datetime

import numpy as np
import pandas as pd
import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_cronometer(real):

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
            "cronometer/cronometer",
            start_date=np.datetime_as_string(start_date, unit="D"),
            end_date=np.datetime_as_string(end_date, unit="D"),
        )

        params = {"start_date": str(start_date), "end_date": str(end_date)}
        """
        if real:
            wearipedia._authenticate_device("cronometer/cronometer", device)
        """
        dailySummary = device.get_data("dailySummary", params=params)
        servings = device.get_data("servings", params=params)
        exercises = device.get_data("exercises", params=params)
        biometrics = device.get_data("biometrics", params=params)

        daily_summary_helper(dailySummary)
        servings_helper(servings)
        exercises_helper(exercises)
        biometrics_helper(biometrics)


valid_bounds = {
    "Energy (kcal)": (0, 7500),
    "Alcohol (g)": (0, 100),
    "Caffeine (mg)": (0, 1000),
    "Water (g)": (0, 10000),
    "B1 (Thiamine) (mg)": (0, 100),
    "B2 (Riboflavin) (mg)": (0, 100),
    "B3 (Niacin) (mg)": (0, 100),
    "B5 (Pantothenic Acid) (mg)": (0, 100),
    "B6 (Pyridoxine) (mg)": (0, 100),
    "B12 (Cobalamin) (µg)": (0, 10000),
    "Folate (µg)": (0, 1000),
    "Vitamin A (µg)": (0, 10000),
    "Vitamin C (mg)": (0, 10000),
    "Vitamin D (IU)": (0, 10000),
    "Vitamin E (mg)": (0, 100),
    "Vitamin K (µg)": (0, 1000),
    "Calcium (mg)": (0, 10000),
    "Copper (mg)": (0, 100),
    "Iron (mg)": (0, 100),
    "Magnesium (mg)": (0, 1000),
    "Manganese (mg)": (0, 100),
    "Phosphorus (mg)": (0, 10000),
    "Potassium (mg)": (0, 10000),
    "Selenium (µg)": (0, 100),
    "Sodium (mg)": (0, 10000),
    "Zinc (mg)": (0, 100),
    "Carbs (g)": (0, 1000),
    "Fiber (g)": (0, 100),
    "Starch (g)": (0, 1000),
    "Sugars (g)": (0, 1000),
    "Net Carbs (g)": (0, 1000),
    "Fat (g)": (0, 1000),
    "Cholesterol (mg)": (0, 1000),
    "Monounsaturated (g)": (0, 1000),
    "Polyunsaturated (g)": (0, 1000),
    "Saturated (g)": (0, 1000),
    "Trans-Fats (g)": (0, 1000),
    "Omega-3 (g)": (0, 1000),
    "Omega-6 (g)": (0, 1000),
    "Cystine (g)": (0, 1000),
    "Histidine (g)": (0, 1000),
    "Isoleucine (g)": (0, 1000),
    "Leucine (g)": (0, 1000),
    "Lysine (g)": (0, 1000),
    "Methionine (g)": (0, 1000),
    "Phenylalanine (g)": (0, 1000),
    "Threonine (g)": (0, 1000),
    "Tryptophan (g)": (0, 1000),
    "Tyrosine (g)": (0, 1000),
    "Valine (g)": (0, 1000),
}


def nutriton_checker(d):
    for key, bounds in valid_bounds.items():
        if not math.isnan(d[key]):
            assert d[key] >= bounds[0]
            assert d[key] < bounds[1]


def daily_summary_helper(data):
    for d in data:
        assert isinstance(d["Day"], str)
        nutriton_checker(d)
        assert isinstance(d["Completed"], bool)


def servings_helper(data):
    for d in data:
        assert isinstance(d["Day"], str)
        nutriton_checker(d)


def exercises_helper(data):
    for d in data:
        assert isinstance(d["Day"], str)
        assert isinstance(d["Exercise"], str)
        assert isinstance(d["Minutes"], float)
        assert isinstance(d["Calories Burned"], float)
        assert d["Minutes"] >= 0
        assert d["Calories Burned"] <= 0


def biometrics_helper(data):
    for d in data:
        assert isinstance(d["Day"], str)
        assert isinstance(d["Metric"], str)
        assert isinstance(d["Unit"], str)
        assert isinstance(d["Amount"], (float, int))
        assert d["Amount"] >= 0
