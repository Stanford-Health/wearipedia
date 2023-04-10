import os

import numpy as np
import pandas as pd


def create_syn_data(start_date, end_date):

    # create a list of dates between start and end date
    dates = pd.date_range(start_date, end_date)

    # creating returned list for each data type
    biometrics = []
    dailySummary = []
    servings = []
    exercises = []

    # Functions to generate random data
    def energy(x):
        return np.round(np.random.uniform(1500, 3500), 2)

    def alcohol(x):
        return np.round(np.random.uniform(0, 10), 2)

    def caffeine(x):
        return np.round(np.random.uniform(0, 500), 2)

    def water(x):
        return np.round(np.random.uniform(1000, 5000), 2)

    syn_weight = np.random.randint(50, 100)

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "servings.csv"))

    # extracted 55 popular food items on random from cronometer
    servings_data = pd.read_csv(path)

    # create random id
    for d in dates:

        # create random biometrics
        biometrics.append(
            {
                "Day": d.strftime("%Y-%m-%d"),
                "Metric": "Weight",
                "Unit": "kg",
                "Amount": syn_weight + np.random.uniform(-2, 2),
            }
        )
        biometrics.append(
            {
                "Day": d.strftime("%Y-%m-%d"),
                "Metric": "Heart Rate (Apple Health)",
                "Unit": "bpm",
                "Amount": np.random.randint(100, 130),
            }
        )

        minutes1 = np.random.uniform(30, 90)
        minutes2 = np.random.uniform(30, 90)

        calories1 = minutes1 * np.random.randint(4, 6)
        calories2 = minutes2 * np.random.randint(4, 6)

        # create random exercises
        exercises.append(
            {
                "Day": d.strftime("%Y-%m-%d"),
                "Exercise": np.random.choice(
                    [
                        "Running",
                        "Traditional Strength Training",
                        "High Intensity Interval Training",
                        "Walking",
                        "Swimming",
                        "Boxing",
                        "Golf",
                        "Elliptical",
                        "Hiking",
                        "Cycling",
                        "Rower",
                        "Yoga",
                        "Dance",
                        "Pilates",
                        "Tai Chi",
                        "Martial Arts",
                        "Climbing",
                        "Skiing",
                        "Snowboarding",
                        "Squash",
                        "Tennis",
                        "Volleyball",
                        "Basketball",
                        "Football",
                        "Rugby",
                        "Baseball",
                        "Softball",
                        "Cricket",
                        "Hockey",
                        "Badminton",
                        "Table Tennis",
                        "Lacrosse",
                        "Handball",
                        "Water Polo",
                        "Fencing",
                        "Gymnastics",
                        "Skateboarding",
                        "Surfing",
                        "Wrestling",
                        "Soccer",
                        "American Football",
                        "Australian Football",
                        "Racquetball",
                        "Field Hockey",
                        "Ice Hockey",
                        "Netball",
                    ]
                ),
                "Minutes": minutes1,
                "Calories Burned": -calories1,
            }
        )
        exercises.append(
            {
                "Day": d.strftime("%Y-%m-%d"),
                "Exercise": "Active Energy Balance (Apple Health)",
                "Minutes": minutes2,
                "Calories Burned": -calories2,
            }
        )

        serving = list(servings_data.sample(1).to_dict("index").values())[0]

        # remove index
        del serving["Unnamed: 0"]

        # create random servings
        serving["Day"] = d.strftime("%Y-%m-%d")

        # add to list
        servings.append(serving)

        # create random exercises
        dailySummary.append(
            {
                "Day": d.strftime("%Y-%m-%d"),
                "Energy (kcal)": energy("x"),
                "Alcohol (g)": alcohol("x"),
                "Caffeine (mg)": caffeine("x"),
                "Water (g)": water("x"),
                "B1 (Thiamine) (mg)": np.round(np.random.normal(1.2, 0.05), 2),
                "B2 (Riboflavin) (mg)": np.round(np.random.normal(1.3, 0.05), 2),
                "B3 (Niacin) (mg)": np.round(np.random.normal(16, 2), 2),
                "B5 (Pantothenic Acid) (mg)": np.round(np.random.normal(5, 1), 2),
                "B6 (Pyridoxine) (mg)": np.round(np.random.normal(1.7, 0.05), 2),
                "B12 (Cobalamin) (µg)": np.round(np.random.normal(4, 0.5), 2),
                "Folate (µg)": np.round(np.random.normal(400, 50), 2),
                "Vitamin A (µg)": np.round(np.random.normal(900, 150), 2),
                "Vitamin C (mg)": np.round(np.random.normal(90, 20), 2),
                "Vitamin D (IU)": np.round(np.random.uniform(300, 900), 2),
                "Vitamin E (mg)": np.round(np.random.normal(15, 2), 2),
                "Vitamin K (µg)": np.round(np.random.normal(100, 20), 2),
                "Calcium (mg)": np.round(np.random.normal(1000, 100), 2),
                "Copper (mg)": np.round(np.random.normal(0.9, 0.05), 2),
                "Iron (mg)": np.round(np.random.normal(8, 2), 2),
                "Magnesium (mg)": np.round(np.random.normal(400, 50), 2),
                "Manganese (mg)": np.round(np.random.normal(2.3, 0.05), 2),
                "Phosphorus (mg)": np.round(np.random.normal(700, 100), 2),
                "Potassium (mg)": np.round(np.random.normal(4700, 200), 2),
                "Selenium (µg)": np.round(np.random.normal(55, 10), 2),
                "Sodium (mg)": np.round(np.random.normal(1500, 200), 2),
                "Zinc (mg)": np.round(np.random.normal(15, 2), 2),
                "Carbs (g)": np.round(np.random.normal(275, 50), 2),
                "Fiber (g)": np.round(np.random.normal(25, 2), 2),
                "Starch (g)": np.round(np.random.normal(225, 50), 2),
                "Sugars (g)": np.round(np.random.normal(36, 10), 2),
                "Net Carbs (g)": np.round(np.random.uniform(40, 120), 2),
                "Fat (g)": np.round(np.random.normal(100, 20), 2),
                "Cholesterol (mg)": np.round(np.random.normal(200, 40), 2),
                "Monounsaturated (g)": np.round(np.random.normal(69, 10), 2),
                "Polyunsaturated (g)": np.round(np.random.normal(17, 2), 2),
                "Saturated (g)": np.round(np.random.normal(22, 5), 2),
                "Trans-Fats (g)": np.round(np.random.normal(2, 0.05), 2),
                "Omega-3 (g)": np.round(np.random.normal(2, 0.05), 2),
                "Omega-6 (g)": np.round(np.random.normal(1.5, 0.05), 2),
                "Cystine (g)": np.round(np.random.normal(25, 5), 2),
                "Histidine (g)": np.round(np.random.normal(2.25, 0.05), 2),
                "Isoleucine (g)": np.round(np.random.normal(19, 2), 2),
                "Leucine (g)": np.round(np.random.normal(2.5, 0.05), 2),
                "Lysine (g)": np.round(np.random.normal(78, 5), 2),
                "Methionine (g)": np.round(np.random.normal(1000), 2),
                "Phenylalanine (g)": np.round(np.random.normal(55, 5), 2),
                "Protein (g)": np.round(np.random.uniform(50, 125), 2),
                "Threonine (g)": np.round(np.random.normal(41.2, 5), 2),
                "Tryptophan (g)": np.round(np.random.normal(20, 3), 2),
                "Tyrosine (g)": np.round(np.random.normal(500, 20), 2),
                "Valine (g)": np.round(np.random.normal(50, 5), 2),
                "Completed": bool(np.random.choice([True, False])),
            }
        )

    return dailySummary, servings, exercises, biometrics
