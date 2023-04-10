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

        if real:
            wearipedia._authenticate_device("cronometer/cronometer", device)

        dailySummary = device.get_data("dailySummary", params=params)
        servings = device.get_data("servings", params=params)
        exercises = device.get_data("exercises", params=params)
        biometrics = device.get_data("biometrics", params=params)

        daily_summary_helper(dailySummary)
        servings_helper(servings)
        exercises_helper(exercises)
        biometrics_helper(biometrics)


def nutriton_checker(d):
    if not math.isnan(d["Energy (kcal)"]):
        assert d["Energy (kcal)"] >= 0
        assert d["Energy (kcal)"] < 7500
    if not math.isnan(d["Alcohol (g)"]):
        assert d["Alcohol (g)"] >= 0
        assert d["Alcohol (g)"] < 100
    if not math.isnan(d["Caffeine (mg)"]):
        assert d["Caffeine (mg)"] >= 0
        assert d["Caffeine (mg)"] < 1000
    if not math.isnan(d["Water (g)"]):
        assert d["Water (g)"] >= 0
        assert d["Water (g)"] < 10000
    if not math.isnan(d["B1 (Thiamine) (mg)"]):
        assert d["B1 (Thiamine) (mg)"] >= 0
        assert d["B1 (Thiamine) (mg)"] < 100
    if not math.isnan(d["B2 (Riboflavin) (mg)"]):
        assert d["B2 (Riboflavin) (mg)"] >= 0
        assert d["B2 (Riboflavin) (mg)"] < 100
    if not math.isnan(d["B3 (Niacin) (mg)"]):
        assert d["B3 (Niacin) (mg)"] >= 0
        assert d["B3 (Niacin) (mg)"] < 100
    if not math.isnan(d["B5 (Pantothenic Acid) (mg)"]):
        assert d["B5 (Pantothenic Acid) (mg)"] >= 0
        assert d["B5 (Pantothenic Acid) (mg)"] < 100
    if not math.isnan(d["B6 (Pyridoxine) (mg)"]):
        assert d["B6 (Pyridoxine) (mg)"] >= 0
        assert d["B6 (Pyridoxine) (mg)"] < 100
    if not math.isnan(d["B12 (Cobalamin) (µg)"]):
        assert d["B12 (Cobalamin) (µg)"] >= 0
        assert d["B12 (Cobalamin) (µg)"] < 100
    if not math.isnan(d["Folate (µg)"]):
        assert d["Folate (µg)"] >= 0
        assert d["Folate (µg)"] < 1000
    if not math.isnan(d["Vitamin A (µg)"]):
        assert d["Vitamin A (µg)"] >= 0
        assert d["Vitamin A (µg)"] < 10000
    if not math.isnan(d["Vitamin C (mg)"]):
        assert d["Vitamin C (mg)"] >= 0
        assert d["Vitamin C (mg)"] < 1000
    if not math.isnan(d["Vitamin D (IU)"]):
        assert d["Vitamin D (IU)"] >= 0
        assert d["Vitamin D (IU)"] < 10000
    if not math.isnan(d["Vitamin E (mg)"]):
        assert d["Vitamin E (mg)"] >= 0
        assert d["Vitamin E (mg)"] < 100
    if not math.isnan(d["Vitamin K (µg)"]):
        assert d["Vitamin K (µg)"] >= 0
        assert d["Vitamin K (µg)"] < 1000
    if not math.isnan(d["Calcium (mg)"]):
        assert d["Calcium (mg)"] >= 0
        assert d["Calcium (mg)"] < 10000
    if not math.isnan(d["Copper (mg)"]):
        assert d["Copper (mg)"] >= 0
        assert d["Copper (mg)"] < 100
    if not math.isnan(d["Iron (mg)"]):
        assert d["Iron (mg)"] >= 0
        assert d["Iron (mg)"] < 100
    if not math.isnan(d["Magnesium (mg)"]):
        assert d["Magnesium (mg)"] >= 0
        assert d["Magnesium (mg)"] < 1000
    if not math.isnan(d["Manganese (mg)"]):
        assert d["Manganese (mg)"] >= 0
        assert d["Manganese (mg)"] < 100
    if not math.isnan(d["Phosphorus (mg)"]):
        assert d["Phosphorus (mg)"] >= 0
        assert d["Phosphorus (mg)"] < 10000
    if not math.isnan(d["Potassium (mg)"]):
        assert d["Potassium (mg)"] >= 0
        assert d["Potassium (mg)"] < 10000
    if not math.isnan(d["Selenium (µg)"]):
        assert d["Selenium (µg)"] >= 0
        assert d["Selenium (µg)"] < 100
    if not math.isnan(d["Sodium (mg)"]):
        assert d["Sodium (mg)"] >= 0
        assert d["Sodium (mg)"] < 10000
    if not math.isnan(d["Zinc (mg)"]):
        assert d["Zinc (mg)"] >= 0
        assert d["Zinc (mg)"] < 100
    if not math.isnan(d["Carbs (g)"]):
        assert d["Carbs (g)"] >= 0
        assert d["Carbs (g)"] < 1000
    if not math.isnan(d["Fiber (g)"]):
        assert d["Fiber (g)"] >= 0
        assert d["Fiber (g)"] < 100
    if not math.isnan(d["Starch (g)"]):
        assert d["Starch (g)"] >= 0
        assert d["Starch (g)"] < 1000
    if not math.isnan(d["Sugars (g)"]):
        assert d["Sugars (g)"] >= 0
        assert d["Sugars (g)"] < 1000
    if not math.isnan(d["Net Carbs (g)"]):
        assert d["Net Carbs (g)"] >= 0
        assert d["Net Carbs (g)"] < 1000
    if not math.isnan(d["Fat (g)"]):
        assert d["Fat (g)"] >= 0
        assert d["Fat (g)"] < 1000
    if not math.isnan(d["Cholesterol (mg)"]):
        assert d["Cholesterol (mg)"] >= 0
        assert d["Cholesterol (mg)"] < 1000
    if not math.isnan(d["Monounsaturated (g)"]):
        assert d["Monounsaturated (g)"] >= 0
        assert d["Monounsaturated (g)"] < 1000
    if not math.isnan(d["Polyunsaturated (g)"]):
        assert d["Polyunsaturated (g)"] >= 0
        assert d["Polyunsaturated (g)"] < 1000
    if not math.isnan(d["Saturated (g)"]):
        assert d["Saturated (g)"] >= 0
        assert d["Saturated (g)"] < 1000
    if not math.isnan(d["Trans-Fats (g)"]):
        assert d["Trans-Fats (g)"] >= 0
        assert d["Trans-Fats (g)"] < 1000
    if not math.isnan(d["Omega-3 (g)"]):
        assert d["Omega-3 (g)"] >= 0
        assert d["Omega-3 (g)"] < 1000
    if not math.isnan(d["Omega-6 (g)"]):
        assert d["Omega-6 (g)"] >= 0
        assert d["Omega-6 (g)"] < 1000
    if not math.isnan(d["Cystine (g)"]):
        assert d["Cystine (g)"] >= 0
        assert d["Cystine (g)"] < 1000
    if not math.isnan(d["Histidine (g)"]):
        assert d["Histidine (g)"] >= 0
        assert d["Histidine (g)"] < 1000
    if not math.isnan(d["Isoleucine (g)"]):
        assert d["Isoleucine (g)"] >= 0
        assert d["Isoleucine (g)"] < 1000
    if not math.isnan(d["Leucine (g)"]):
        assert d["Leucine (g)"] >= 0
        assert d["Leucine (g)"] < 1000
    if not math.isnan(d["Lysine (g)"]):
        assert d["Lysine (g)"] >= 0
        assert d["Lysine (g)"] < 1000
    if not math.isnan(d["Methionine (g)"]):
        assert d["Methionine (g)"] >= 0
        assert d["Methionine (g)"] < 10000
    if not math.isnan(d["Phenylalanine (g)"]):
        assert d["Phenylalanine (g)"] >= 0
        assert d["Phenylalanine (g)"] < 1000
    if not math.isnan(d["Threonine (g)"]):
        assert d["Threonine (g)"] >= 0
        assert d["Threonine (g)"] < 1000
    if not math.isnan(d["Tryptophan (g)"]):
        assert d["Tryptophan (g)"] >= 0
        assert d["Tryptophan (g)"] < 1000
    if not math.isnan(d["Tyrosine (g)"]):
        assert d["Tyrosine (g)"] >= 0
        assert d["Tyrosine (g)"] < 1000
    if not math.isnan(d["Valine (g)"]):
        assert d["Valine (g)"] >= 0
        assert d["Valine (g)"] < 1000


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
        assert isinstance(d["Amount"], float | int)
        assert d["Amount"] >= 0
