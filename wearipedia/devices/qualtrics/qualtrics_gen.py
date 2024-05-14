import math
import random
from datetime import datetime, timedelta

import numpy as np


def create_syn_data(start_date, end_date):
    """
    Generates synthetic data collected by Biostrap between a given start and end date.

    :param start_date: Start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: End date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str

    :return: A tuple consisting of:
        - activities: Dictionary containing details of a random synthetic activity
        - bpm: Dictionary representing beats per minute for every 10 seconds throughout the range
        - brpm: Dictionary representing breaths per minute based on bpm values for every minute throughout the range
        - hrv: Dictionary representing heart rate variability for every 10 seconds throughout the range
        - spo2: Dictionary representing blood oxygen saturation for every 10 seconds
        - rest_cals: Dictionary representing resting calories burned each day
        - work_cals: Dictionary representing workout calories burned each day
        - active_cals: Dictionary representing active calories burned each day
        - step_cals: Dictionary representing calories burned from steps each day
        - total_cals: Dictionary representing total calories burned each day
        - sleep_session: Dictionary representing moments of movement during typical sleeping hours
        - sleep_detail: Dictionary representing details of a synthetic sleep session
        - steps: Dictionary representing steps taken every minute throughout the range
        - distance: Dictionary representing distance covered (based on steps) every minute throughout the range

    :rtype: Tuple[Dict, Dict, Dict, Dict, Dict, Dict, Dict, Dict, Dict, Dict, Dict, Dict, Dict, Dict]
    """

    # Convert the provided strings to datetime objects
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    TZ_OFFSET = -420

    # Adjusted Gaussian noise functions for each biometric with more realistic standard deviations
    def gaussian_noise_bpm():
        return np.random.normal(0, 2)  # Reduced standard deviation for less noise

    def gaussian_noise_brpm():
        return np.random.normal(0, 0.5)  # Reduced standard deviation for less noise

    def gaussian_noise_hrv():
        return np.random.normal(0, 1)  # Reduced standard deviation for less noise

    def gaussian_noise_spo2():
        return np.random.normal(0, 0.05)  # Reduced standard deviation for minimal noise

    def synthetic_biometrics(start_date_obj, end_date_obj):
        bpm = {}
        brpm = {}
        hrv = {}
        spo2 = {}

        curr_date_obj = start_date_obj
        time_index = 0

        # Initial values for random walk
        bpm_current = 45
        brpm_current = 16
        hrv_current = 40
        spo2_current = 98

        # Target means and bounds
        target_mean_bpm = 70
        target_mean_brpm = 16
        target_mean_hrv = 50
        target_mean_spo2 = 98

        bpm_lower_bound, bpm_upper_bound = 40, 120
        brpm_lower_bound, brpm_upper_bound = 12, 20
        hrv_lower_bound, hrv_upper_bound = 20, 100
        spo2_lower_bound, spo2_upper_bound = 95, 100

        # Store the last minute's average bpm to calculate brpm
        last_minute_bpm = []

        while curr_date_obj <= end_date_obj:
            curr_time = curr_date_obj
            while curr_time < curr_date_obj + timedelta(days=1):
                key = (curr_time.strftime("%Y-%m-%d %H:%M:%S"), TZ_OFFSET)

                # Update bpm, hrv, and spo2 every 10 seconds
                bpm_mean_reversion = (
                    target_mean_bpm - bpm_current
                ) * 0.01  # Changed from 0.1
                bpm_current += bpm_mean_reversion + gaussian_noise_bpm()
                bpm_current = max(bpm_lower_bound, min(bpm_upper_bound, bpm_current))
                bpm[key] = int(bpm_current)

                hrv_mean_reversion = (target_mean_hrv - hrv_current) * 0.1
                hrv_current += hrv_mean_reversion + gaussian_noise_hrv()
                hrv_current = max(hrv_lower_bound, min(hrv_upper_bound, hrv_current))
                hrv[key] = int(hrv_current)

                spo2_mean_reversion = (target_mean_spo2 - spo2_current) * 0.1
                spo2_current += spo2_mean_reversion + gaussian_noise_spo2()
                spo2_current = max(
                    spo2_lower_bound, min(spo2_upper_bound, spo2_current)
                )
                spo2[key] = int(spo2_current)

                # Update brpm every minute
                if time_index % 60 == 0:
                    brpm_mean_reversion = (target_mean_brpm - brpm_current) * 0.1
                    brpm_current += brpm_mean_reversion + gaussian_noise_brpm()
                    brpm_current = max(
                        brpm_lower_bound, min(brpm_upper_bound, brpm_current)
                    )
                    brpm[key] = int(brpm_current)

                # Increment time and index
                curr_time += timedelta(seconds=10)
                time_index += 10

            curr_date_obj += timedelta(days=1)

        return bpm, brpm, hrv, spo2

    def synthetic_steps_distance_per_minute(bpm_dict):
        steps_dict = {}
        distance_dict = {}

        # For each minute, we'll check the BPM to determine steps
        for key, bpm_value in bpm_dict.items():
            dt, _ = key

            # Extracting hour to check for sleeping hours
            curr_hour = int(dt.split(" ")[1].split(":")[0])

            if dt.endswith("00"):  # Checking if it's on a per-minute mark
                if 23 <= curr_hour or curr_hour < 6:  # typical sleeping hours
                    steps = random.choice(
                        [0, 0, 0, 0, 1, 2]
                    )  # Mostly zero, but sometimes a small number indicating tossing/turning in sleep
                elif bpm_value < 60:
                    steps = random.randint(0, 20)  # Relatively calm/resting
                elif bpm_value < 80:
                    steps = random.randint(20, 40)  # Maybe just light walking
                else:
                    steps = random.randint(40, 120)  # Active movement or jogging

                distance = steps * random.uniform(0.7, 0.8)
                date_str = dt.split()[0]
                time_str = dt.split()[1]

                steps_dict[f"{date_str} {time_str}"] = steps
                distance_dict[f"{date_str} {time_str}"] = distance

        return steps_dict, distance_dict

    def synthetic_daily_calories(bpm_dict, steps_dict):
        rest_cals_dict = {}
        work_cals_dict = {}
        active_cals_dict = {}
        step_cals_dict = {}
        total_cals_dict = {}

        daily_bpm_averages = {}

        # Precompute average BPM per day
        for (dt, _), v in bpm_dict.items():
            date_str = dt.split(" ")[0]
            daily_bpm_averages.setdefault(date_str, []).append(v)

        # Compute average BPM for each day
        for date_str, bpm_vals in daily_bpm_averages.items():
            avg_bpm = sum(bpm_vals) / len(bpm_vals)
            daily_bpm_averages[date_str] = avg_bpm

        # Calculate calories based on the precomputed average BPMs
        for date_str, avg_bpm in daily_bpm_averages.items():
            if avg_bpm < 60:
                active_cals = random.randint(50, 100)  # relatively inactive
            elif avg_bpm < 80:
                active_cals = random.randint(100, 200)  # moderately active
            else:
                active_cals = random.randint(200, 300)  # very active

            steps_val = sum(
                [val for dt, val in steps_dict.items() if dt.startswith(date_str)]
            )

            rest_cals_dict[date_str] = random.randint(1000, 1300)
            work_cals_dict[date_str] = random.randint(300, 600)
            step_cals_dict[date_str] = steps_val * 0.05
            active_cals_dict[date_str] = active_cals
            total_cals_dict[date_str] = (
                rest_cals_dict[date_str]
                + work_cals_dict[date_str]
                + step_cals_dict[date_str]
                + active_cals_dict[date_str]
            )

        return (
            rest_cals_dict,
            work_cals_dict,
            active_cals_dict,
            step_cals_dict,
            total_cals_dict,
        )

    def synthetic_activity():
        # A sample workout
        activity_date = (start_date_obj + (end_date_obj - start_date_obj) / 2).strftime(
            "%Y-%m-%d"
        )  # choose a day in the middle of the range

        return {
            "activity_date": activity_date,
            "type": "Running",
            "duration": timedelta(minutes=random.randint(20, 60)),
            "distance": random.uniform(3, 10),
            "calories_burned": random.randint(200, 500),
            "avg_bpm": random.randint(80, 150),
            "peak_bpm": random.randint(150, 180),
            "steps_taken": random.randint(3000, 10000),
            "intensity": random.choice(["light", "moderate", "high"]),
        }

    def synthetic_sleep_session(bpm_dict):
        # Extracting nighttime bpm readings
        night_movements = {
            k: v
            for k, v in bpm_dict.items()
            if 23 <= int(k[0].split(" ")[1].split(":")[0])
            or int(k[0].split(" ")[1].split(":")[0]) < 6
        }
        # Filter out readings where bpm indicates deep sleep (low bpm)
        night_movements = {k: v for k, v in night_movements.items() if v > 65}
        return night_movements

    def synthetic_sleep_detail():
        sleep_date = (start_date_obj + (end_date_obj - start_date_obj) / 2).strftime(
            "%Y-%m-%d"
        )
        total_sleep_duration = 8  # Assuming 8 hours sleep

        light_sleep = random.uniform(0.4, 0.6) * total_sleep_duration
        deep_sleep = random.uniform(0.2, 0.3) * total_sleep_duration
        rem_sleep = total_sleep_duration - (light_sleep + deep_sleep)

        return {
            "sleep_date": sleep_date,
            "light_sleep": light_sleep,
            "deep_sleep": deep_sleep,
            "rem_sleep": rem_sleep,
            "awake_time": random.uniform(0.1, 0.3),
            "times_awoken": random.randint(1, 5),
        }

    # Generate biometric, steps, and distance data
    bpm, brpm, hrv, spo2 = synthetic_biometrics(start_date_obj, end_date_obj)
    steps, distance = synthetic_steps_distance_per_minute(bpm)

    # Generate daily calories based on steps and bpm
    rest_cals, work_cals, active_cals, step_cals, total_cals = synthetic_daily_calories(
        bpm, steps
    )

    # Generate activity data
    activities = synthetic_activity()

    # Generate sleep session data
    sleep_session = synthetic_sleep_session(bpm)

    # Generate sleep detail data
    sleep_detail = synthetic_sleep_detail()

    return (
        activities,
        bpm,
        brpm,
        hrv,
        spo2,
        rest_cals,
        work_cals,
        active_cals,
        step_cals,
        total_cals,
        sleep_session,
        sleep_detail,
        steps,
        distance,
    )
