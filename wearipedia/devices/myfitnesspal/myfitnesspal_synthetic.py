import json
import os

import numpy as np
import pandas as pd


def create_syn_data(start_date, end_date):

    # Create a list of dates between start_date and end_date
    dates = pd.date_range(start_date, end_date, freq="D")

    # Create empty lists to store data
    goals = []
    daily_summary = []
    strength_exercises = []
    cardio_exercises = []
    breakfast = []
    lunch = []
    dinner = []
    snacks = []

    # Functions to generate synthetic data
    def syn_calories(x):
        return np.round(np.random.normal(2500, 200), 1)

    def syn_carbs(x):
        return np.round(np.random.normal(250, 75), 1)

    def syn_fat(x):
        return np.round(np.random.normal(75, 25), 1)

    def syn_protein(x):
        return np.round(max(0.0, np.random.normal(100, 33)), 1)

    def syn_sodium(x):
        return np.round(np.random.normal(2300, 500), 1)

    def syn_sugar(x):
        return np.round(np.random.normal(75, 25), 1)

    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "myfitnesspal_syn_data.json")
    )

    # Loading data from our json file
    data = json.load(open(path, "r"))

    # wearipedia/devices/myfitnesspal/myfitnesspal_syn_data.json

    # Scraped a list of all exercises from MyFitnessPal and used GPT3 to seperate them into strength and cardio exercises
    exercises_cardio = data["exercises_cardio"]
    # List of exercises that are strength exercises scraped from myfitnesspal.com
    exercises_strength = data["exercises_strength"]

    # List of top 15 breakfast foods from the USDA
    breakfast_foods = data["breakfast_foods"]

    # List of top 15 lunch foods from the USDA
    lunch_foods = data["lunch_foods"]
    # List of top 15 dinner foods from the USDA
    dinner_foods = data["dinner_foods"]
    # List of top 15 snack foods from the USDA
    snack_foods = data["snack_foods"]

    def create_food_item(item_name, food_item):
        return [
            {"day": pd.Timestamp(day)},
            {
                "name": item_name,
                "nutrition_information": {
                    "calories": float(food_item["calories"]),
                    "carbohydrates": float(food_item["carbohydrates"]),
                    "fat": float(food_item["fat"]),
                    "protein": float(food_item["protein"]),
                    "sodium": float(food_item["sodium"]),
                    "sugar": float(food_item["sugar"]),
                },
                "totals": {
                    "calories": float(food_item["calories"]),
                    "carbohydrates": float(food_item["carbohydrates"]),
                    "fat": float(food_item["fat"]),
                    "protein": float(food_item["protein"]),
                    "sodium": float(food_item["sodium"]),
                    "sugar": float(food_item["sugar"]),
                },
            },
        ]

    for day in dates:

        # Creating a randomly generated summary of the day's food goal
        goals.append(
            {
                "calories": syn_calories(day),
                "carbohydrates": syn_carbs(day),
                "fat": syn_fat(day),
                "protein": syn_protein(day),
                "sodium": syn_sodium(day),
                "sugar": syn_sugar(day),
                "date": pd.Timestamp(day),
            }
        )

        # Creating a randomly generated summary of the day's food intake
        daily_summary.append(
            {
                "calories": syn_calories(day),
                "carbohydrates": syn_carbs(day),
                "fat": syn_fat(day),
                "protein": syn_protein(day),
                "sodium": syn_sodium(day),
                "sugar": syn_sugar(day),
                "date": pd.Timestamp(day),
            }
        )

        # Creating a randomly generated list of cardio exercises for the day
        cardio = [{"day": pd.Timestamp(day)}]

        # We will randomly select between 1 and 3 cardio exercises
        cardio_count = np.random.randint(1, 3)

        # We will randomly select between 1 and 3 cardio exercises
        random_exercises = np.random.choice(
            exercises_cardio, cardio_count, replace=False
        )

        # Adding each exercise to the list of cardio exercises for that day
        for exercise in random_exercises:
            minutes = np.random.randint(10, 60)
            syn_exercise = {
                "name": exercise,
                "nutrition_information": {
                    "minutes": minutes,
                    "calories burned": minutes * max(2, np.random.uniform(3, 5)),
                },
            }

            # Adding the exercise to the list of cardio exercises for that day
            cardio.append(syn_exercise)

        # Adding the list of cardio exercises for that day to the list of all cardio exercises
        cardio_exercises.append(cardio)

        # Creating a randomly generated list of strength exercises for the day
        strength = []

        # Adding the date to the list of strength exercises for that day
        strength.append({"date": pd.Timestamp(day)})

        # We will randomly select between 1 and 10 strength exercises
        exercise_count = np.random.randint(1, 10)

        # We will randomly select between 1 and 10 strength exercises
        random_exercises = np.random.choice(
            exercises_strength, exercise_count, replace=False
        )

        # Adding each exercise to the list of strength exercises for that day
        for exercise in random_exercises:
            syn_exercise = {
                "name": exercise,
                "nutrition_information": {
                    "sets": float(np.random.randint(2, 5)),
                    "reps/set": float(np.round(np.random.uniform(10, 2))),
                    "weight/set": float(np.random.randint(5, 100)),
                },
            }
            strength.append(syn_exercise)
        strength_exercises.append(strength)

        # Creating a randomly generated list of breakfast foods for the day
        breakfast_item_name = np.random.choice(list(breakfast_foods.keys()))
        breakfast_item = breakfast_foods[breakfast_item_name]

        # Adding the breakfast food to the list of breakfast foods for that day
        breakfast.append(create_food_item(breakfast_item_name, breakfast_item))

        # Creating a randomly generated list of lunch foods for the day
        lunch_item_name = np.random.choice(list(lunch_foods.keys()))
        lunch_item = lunch_foods[lunch_item_name]

        # Adding the lunch food to the list of lunch foods for that day
        lunch.append(create_food_item(lunch_item_name, lunch_item))

        # Creating a randomly generated list of dinner foods for the day
        dinner_item_name = np.random.choice(list(dinner_foods.keys()))
        dinner_item = dinner_foods[dinner_item_name]

        # Adding the dinner food to the list of dinner foods for that day
        dinner.append(create_food_item(dinner_item_name, dinner_item))

        # Creating a randomly generated list of snack foods for the day
        snack_item_name = np.random.choice(list(snack_foods.keys()))
        snack_item = snack_foods[snack_item_name]

        # Adding the snack food to the list of snack foods for that day
        snacks.append(create_food_item(snack_item_name, snack_item))

    return (
        goals,
        daily_summary,
        cardio_exercises,
        strength_exercises,
        breakfast,
        lunch,
        dinner,
        snacks,
    )
