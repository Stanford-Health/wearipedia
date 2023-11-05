import uuid

import numpy as np
import pandas as pd


def create_syn_data(start_date, end_date):

    # create a list of dates between start and end date
    dates = pd.date_range(start_date, end_date)
    # create random id
    def random_id(x):
        return np.random.randint(1000000000, 9999999999, dtype=np.int64)

    # create random duration in milliseconds between 15 and 120 minutes
    def random_duration(x):
        return np.random.randint(900000, 7200000, dtype=np.int64)

    # create random distance
    def random_distance(d):
        return d / 6000 * 5

    # create random hr_avg
    def random_hr_avg(d):
        return np.random.randint(60, 180, dtype=np.int64)

    # create random calories with the assumption that 1
    def random_calories(dur):
        return dur / 6000 * 5 * 0.1

    # create random maxHr
    def max_syn_hrs(x):
        return np.round(np.random.normal(120, 20), 14)

    # create random minHr
    def min_syn_hrs(x):
        return np.round(np.random.normal(80, 20), 14)

    # create random vo2Max
    def random_vo2Max(x):
        return np.random.randint(40, 60)

    # create random recoveryTime
    def random_recovery_time(dur):
        return dur - np.random.randint(0, dur, dtype=np.int64)

    # generating the name for the the syntehtic user
    randomName = "John Doe"

    # create random periodDataUuid
    random_periodDataUuid = str(uuid.uuid4())

    # Random sleep time generator function
    def sleep_time():
        return f"T{np.random.randint(20, 24)}:{np.random.randint(0, 60):02d}:{np.random.randint(0, 60):02d}.{np.random.randint(0, 1000):03d}-{np.random.randint(0, 24):02d}:{np.random.randint(0, 60):02d}"

    def wake_time():
        return f"T{np.random.randint(5, 10):02d}:{np.random.randint(0, 60):02d}:{np.random.randint(0, 60):02d}.{np.random.randint(0, 1000):03d}-{np.random.randint(4, 8):02d}:{np.random.randint(0, 60):02d}"

    def activity_time(d):
        return f"{d.strftime('%Y-%m-%d')}T{np.random.randint(5, 22):02d}:{np.random.randint(0, 60):02d}:{np.random.randint(0, 60):02d}.{np.random.randint(0, 1000):03d}-{np.random.randint(4, 8):02d}:{np.random.randint(0, 60):02d}"

    # Continutity of sleep
    def continuity(x):
        return np.round(np.random.rand() * 2, 1)

    # List to store all the synthetically generated sleeps
    sleeps = []

    # List to store all the synthetically generated training sessions
    trainings = []

    # List to store all the synthetically generated training sessions by id
    training_by_ids = []

    for d in dates:

        # Create a a dictionary sleep on the current date
        current_sleep = {
            "date": d.strftime("%Y-%m-%d"),
            "sleepStartTime": d.strftime("%Y-%m-%d") + sleep_time(),
            "sleepEndTime": (d + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
            + wake_time(),
            "sleepStartOffset": 0,
            "sleepEndOffset": 0,
            "sleepRating": None,
            "continuityIndex": continuity(0),
            "continuityClass": 1,
            "sleepCycles": np.random.randint(4, 7),
            "sleepScore": np.round(np.random.rand() * 100, 5),
            "sleepWakeStates": [],
        }

        # Calculate total sleep time
        total_sleep_time = pd.to_datetime(
            current_sleep["sleepEndTime"][:19]
        ) - pd.to_datetime(current_sleep["sleepStartTime"][:19])

        # Create random sleep wake states
        for i in range(total_sleep_time.seconds // 300):
            current_sleep["sleepWakeStates"].append(
                {
                    "sleepWakeState": int(
                        np.random.choice([0] * 35 + [1] * 15 + [2] * 40 + [3] * 10)
                    ),
                    "offsetFromStart": i * 300,
                    "longInterruption": bool(np.random.choice([True] + [False] * 9)),
                }
            )

        # Append the current sleep to the list of sleeps
        sleeps.append(current_sleep)

        # Generating a random duration for the training session
        duration = random_duration("")

        # Generating a random distance for the training session
        distance = int(random_distance(duration))

        # Creating a dictionary to store images for activities
        activity_images = {
            "Running": "https://platform.cdn.polar.com/ecosystem/sport/icon/808d0882e97375e68844ec6c5417ea33-2015-10-20_13_46_22",
            "Cycling": "https://platform.cdn.polar.com/ecosystem/sport/icon/561a80f6d7eef7cc328aa07fe992af8e-2015-10-20_13_46_03",
            "Strength_Training": "https://platform.cdn.polar.com/ecosystem/sport/icon/d1ce94078aec226be28f6c602e6803e1-2015-10-20_13_45_19",
            "Swimming": "https://platform.cdn.polar.com/ecosystem/sport/icon/f4197b0c1a4d65962b9e45226c77d4d5-2015-10-20_13_45_26",
        }

        # Randomly generating a selected activity
        selected_activity = np.random.choice(
            ["Running", "Cycling", "Strength_Training", "Swimming"]
        )

        # Create a a dictionary for the activity on the current date
        activity = {
            "id": random_id(""),
            "duration": duration,
            "distance": distance,
            "hrAvg": random_hr_avg(""),
            "calories": int(random_calories(duration)),
            "note": " ",
            "sportName": selected_activity,
            "sportId": int(np.random.choice([1, 2, 15, 16])),
            "startDate": f"{d.strftime('%Y-%m-%d')} {str(pd.to_datetime(activity_time(d)[:19])).split(' ')[1]}.{str(np.random.randint(0, 1000)).zfill(3)}",
            "recoveryTime": random_recovery_time(duration),
            "iconUrl": activity_images[selected_activity],
            "trainingLoadHtml": "",
            "hasTrainingTarget": False,
            "swimmingSport": False,
            "swimmingPoolUnits": "METERS",
            "trainingLoadProHtml": "000000",
            "periodDataUuid": random_periodDataUuid,
            "isTest": False,
        }

        # If the activity is swimming, add the swimmingSport key
        if activity["sportId"] == 16:
            activity["swimmingSport"] = True

        # Append the current activity to the list of activities
        trainings.append(activity)

        # if time is after 12pm, change the suffix to PM
        suffix = "AM"
        if pd.to_datetime(activity["startDate"][:19]).hour > 12:
            suffix = "PM"

        # Convert distance to miles
        distance = activity["distance"] / 1609.344

        # Create a a dictionary for the training session by id on the current date
        curr_id_traning = [
            {
                "Name": randomName,
                "Sport": activity["sportName"].upper(),
                "Date": d.strftime("%d-%m-%Y"),
                "Start time": f"{str(pd.to_datetime(activity['startDate'][:19])).split(' ')[1]} {suffix}",
                "Duration": str(int(duration / 3600000)).zfill(2)
                + ":"
                + str(int(duration / 60000)).zfill(2)
                + ":"
                + str(int(duration % 1000))[:2].zfill(2),
                "Total distance (mi)": np.round(distance, 2)
                if activity["sportId"] != 15
                else None,
                "Average heart rate (bpm)": activity["hrAvg"],
                "Average speed (mi/h)": np.round(
                    distance / (activity["duration"] / 3600000), 1
                )
                if activity["sportId"] != 15
                else None,
                "Max speed (mi/h)": np.round(
                    distance / (activity["duration"] / 3600000)
                )
                if activity["sportId"] != 15
                else None,
                "Average pace (min/mi)": (duration / 60000) / activity["distance"]
                if activity["sportId"] != 5
                else None,
                "Max pace (min/mi)": (duration / 60000) / activity["distance"]
                + np.random.randint(0, 10)
                if activity["sportId"] != 15
                else None,
                "Calories": activity["calories"],
                "Fat percentage of calories(%)": 55,
                "Carbohydrate percentage of calories(%)": 45,
                "Protein percentage of calories(%)": 0,
                "Average cadence (rpm)": 0,
                "Average stride length (in)": 0,
                "Running index": 0,
                "Training load": 0,
                "Ascent (ft)": 0,
                "Descent (ft)": 0,
                "Average power (W)": 0,
                "Max power (W)": 0,
                "Notes": " ",
                "Height (ft in)": "5 11",
                "Weight (lbs)": 119.0,
                "HR max": int(max_syn_hrs("")),
                "HR sit": int(min_syn_hrs("")),
                "VO2max": int(random_vo2Max("")),
                "Unnamed: 29": None,
            }
        ]

        # Create a a dictionary for the training session by id on the current date
        temp = np.random.randint(50, 90)

        # Our sample time is 1 second, so we need to loop through the duration of the activity
        for i in range(duration // 1000):
            curr_id_traning.append(
                {
                    "Sample rate": 1,
                    "Time": f"{str(i // 3600).zfill(2)}:{str(i // 60).zfill(2)}:{str(i % 60).zfill(2)}",
                    "HR (bpm)": int(random_hr_avg("")),
                    "Speed (mi/h)": np.round(
                        distance / (activity["duration"] / 3600000), 1
                    )
                    if activity["sportId"] not in [15, 16]
                    else None,
                    "Pace (min/mi)": distance / (activity["distance"] / 3600000)
                    if activity["sportId"] not in [15, 16]
                    else None,
                    "Cadence": 0,
                    "Altitude (ft)": 0,
                    "Stride length (in)": 0,
                    "Distances (ft)": 0,
                    "Temperatures (F)": temp,
                    "Power (W)": 0,
                    "Unnamed: 11": None,
                }
            )

        # Append the current activity to the list of activities
        training_by_ids.append(curr_id_traning)

    # Return the list of sleeps, activities, and training by id
    return trainings, sleeps, training_by_ids[0]
