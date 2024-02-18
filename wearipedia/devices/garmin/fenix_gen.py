import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm

__all__ = ["create_syn_data"]


################
# some helpers #
################


def get_hrv_data(start_date, num_days):
    """
    Generate synthetic Heart Rate Variability (HRV) data for a specified date range.

    This function creates synthetic HRV data for a given number of days starting from a specified date.
    It includes various HRV metrics such as last night's average, last night's 5-minute high, baseline values,
    status, feedback phrases, and associated timestamps.

    :param start_date: The start date for the HRV data generation in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_days: The number of days to generate HRV data for, starting from the start_date.
    :type num_days: int
    :return: A list of dictionaries, each containing HRV data for a specific day. This includes HRV summary,
        readings, timestamps, and sleep-related timestamps.
    :rtype: List[Dict]
    """

    hrv_data = []
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        date = start_date_obj + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        start_timestamp_gmt = f"{date_str}T06:00:00.0"
        end_timestamp_gmt = (
            f"{date_str}T13:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.0"
        )
        start_timestamp_local = f"{(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')}T23:00:00.0"
        end_timestamp_local = (
            f"{date_str}T06:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.0"
        )

        last_night_avg = random.randint(15, 30)
        last_night_5min_high = random.randint(30, 60)
        baseline = {
            "lowUpper": random.randint(15, 20),
            "balancedLow": random.randint(20, 25),
            "balancedUpper": random.randint(25, 35),
            "markerValue": round(random.uniform(0.3, 0.6), 8),
        }
        status = random.choice(["BALANCED", "ELEVATED", "LOW"])
        feedback_phrase = f"HRV_{status}_RANDOM"

        hrv_entry = {
            "userProfilePk": random.randint(10000000, 99999999),
            "hrvSummary": {
                "calendarDate": date_str,
                "weeklyAvg": None,
                "lastNightAvg": last_night_avg,
                "lastNight5MinHigh": last_night_5min_high,
                "baseline": baseline,
                "status": status,
                "feedbackPhrase": feedback_phrase,
                "createTimeStamp": date.strftime("%Y-%m-%dT%H:%M:%S.000"),
            },
            "hrvReadings": [],
            "startTimestampGMT": start_timestamp_gmt,
            "endTimestampGMT": end_timestamp_gmt,
            "startTimestampLocal": start_timestamp_local,
            "endTimestampLocal": end_timestamp_local,
            "sleepStartTimestampGMT": None,
            "sleepEndTimestampGMT": None,
            "sleepStartTimestampLocal": None,
            "sleepEndTimestampLocal": None,
        }

        hrv_data.append(hrv_entry)

    return hrv_data


def get_steps_data(start_date, num_days):
    """
    Generate synthetic step data for a specified date range.

    This function creates synthetic step data for each 15-minute interval within a specified date range.
    It includes the number of steps taken, activity level, and a boolean indicating if the activity level is constant.

    :param start_date: The start date for generating step data in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_days: The number of days to generate step data for, starting from the start_date.
    :type num_days: int
    :return: A list of lists, where each inner list contains dictionaries of step data for each 15-minute
        interval in a day. Each dictionary includes the start and end times for the interval, steps taken,
        activity level, and a constant activity level indicator.
    :rtype: List[List[Dict]]
    """
    steps_data = []

    for _ in range(num_days):
        calendar_date = (
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)
        ).strftime("%Y-%m-%d")
        start_timestamp_gmt = f"{calendar_date}T06:00:00.0"

        steps_day = []
        for i in range(96):  # 24 hours * 60 minutes / 15 minutes
            interval_start = datetime.strptime(
                start_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0"
            ) + timedelta(minutes=15 * i)
            interval_end = interval_start + timedelta(minutes=15)
            steps_entry = {
                "startGMT": interval_start.strftime("%Y-%m-%dT%H:%M:%S.0"),
                "endGMT": interval_end.strftime("%Y-%m-%dT%H:%M:%S.0"),
                "steps": random.randint(0, 200),
                "pushes": 0,
                "primaryActivityLevel": random.choice(
                    ["active", "sedentary", "sleeping", "none"]
                ),
                "activityLevelConstant": random.choice([True, False]),
            }
            steps_day.append(steps_entry)
        steps_data.append(steps_day)

    return steps_data


def get_daily_steps_data(start_date, num_days):
    """
    Generate synthetic daily steps data for a specified date range.

    This function creates synthetic data representing daily step counts, total distance covered, and a step goal
    for each day within a given date range. The step counts and distances are randomly generated within a specified range.

    :param start_date: The start date for generating daily step data in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_days: The number of days for which to generate daily step data, starting from the start_date.
    :type num_days: int
    :return: A list where each item is a list of dictionary containing the date, total steps taken, total distance covered,
        and the step goal for that day.
    :rtype: List[List[Dict]]
    """
    daily_steps_data = []
    for day in range(num_days):
        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day)
        calendar_date = date.strftime("%Y-%m-%d")

        daily_steps_entry = [
            {
                "calendarDate": calendar_date,
                "totalSteps": random.randint(5000, 20000),
                "totalDistance": random.randint(5000, 20000) * random.uniform(0.5, 0.7),
                "stepGoal": 278,
            },
        ]
        daily_steps_data.append(daily_steps_entry)

    return daily_steps_data


def get_stats_data(start_date, num_days):
    """
    Generate synthetic statistics data for a specified date range.

    This function creates synthetic data for daily statistics over a given date range. It includes metrics such as total
    and active kilocalories, steps, distance covered, heart rate statistics, stress levels, sleep duration, and body
    battery values. Each data point is generated with a mix of random and specified values to simulate realistic stats.

    :param start_date: The starting date for generating statistics data in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_days: The number of days for which to generate statistics data.
    :type num_days: int
    :return: A list of dictionaries, each containing a set of statistics for each day within the specified date range.
    :rtype: List[Dict]
    """
    stats_data = []

    for day in range(num_days):
        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day)
        calendar_date = date.strftime("%Y-%m-%d")
        next_day = date + timedelta(days=1)

        stats_entry = {
            "userProfileId": random.randint(10000000, 99999999),
            "totalKilocalories": random.uniform(1500, 3500),
            "activeKilocalories": random.uniform(300, 1000),
            "bmrKilocalories": random.uniform(1200, 2000),
            "wellnessKilocalories": random.uniform(1500, 3500),
            "burnedKilocalories": None,
            "consumedKilocalories": None,
            "remainingKilocalories": random.uniform(500, 2000),
            "totalSteps": random.randint(2000, 15000),
            "netCalorieGoal": None,
            "totalDistanceMeters": random.uniform(1000, 10000),
            "wellnessDistanceMeters": random.uniform(1000, 10000),
            "wellnessActiveKilocalories": random.uniform(300, 1000),
            "netRemainingKilocalories": random.uniform(500, 2000),
            "userDailySummaryId": random.randint(10000000, 99999999),
            "calendarDate": calendar_date,
            "rule": {"typeId": 3, "typeKey": "subscribers"},
            "uuid": "8de4eb77ec554b3daf024adf862971d1",
            "dailyStepGoal": random.randint(3000, 10000),
            "wellnessStartTimeGmt": f"{calendar_date}T07:00:00.0",
            "wellnessStartTimeLocal": f"{calendar_date}T00:00:00.0",
            "wellnessEndTimeGmt": f"{next_day.strftime('%Y-%m-%d')}T07:00:00.0",
            "wellnessEndTimeLocal": f"{next_day.strftime('%Y-%m-%d')}T00:00:00.0",
            "durationInMilliseconds": 86400000,
            "wellnessDescription": None,
            "highlyActiveSeconds": random.randint(500, 3000),
            "activeSeconds": random.randint(1000, 7000),
            "sedentarySeconds": random.randint(20000, 60000),
            "sleepingSeconds": random.randint(18000, 36000),
            "includesWellnessData": True,
            "includesActivityData": False,
            "includesCalorieConsumedData": False,
            "privacyProtected": False,
            "moderateIntensityMinutes": random.randint(10, 60),
            "vigorousIntensityMinutes": random.randint(5, 30),
            "floorsAscendedInMeters": random.uniform(0, 20),
            "floorsDescendedInMeters": random.uniform(0, 15),
            "floorsAscended": random.uniform(0, 8),
            "floorsDescended": random.uniform(0, 5),
            "intensityMinutesGoal": random.randint(30, 120),
            "userFloorsAscendedGoal": random.randint(5, 15),
            "minHeartRate": random.randint(50, 70),
            "maxHeartRate": random.randint(110, 150),
            "restingHeartRate": random.randint(55, 75),
            "lastSevenDaysAvgRestingHeartRate": random.randint(55, 75),
            "source": "GARMIN",
            "averageStressLevel": random.randint(10, 50),
            "maxStressLevel": random.randint(50, 100),
            "stressDuration": random.randint(10000, 40000),
            "restStressDuration": random.randint(5000, 30000),
            "activityStressDuration": random.randint(2000, 10000),
            "uncategorizedStressDuration": random.randint(1000, 5000),
            "totalStressDuration": random.randint(20000, 80000),
            "lowStressDuration": random.randint(10000, 30000),
            "mediumStressDuration": random.randint(5000, 20000),
            "highStressDuration": random.randint(1000, 5000),
            "stressPercentage": random.uniform(10, 60),
            "restStressPercentage": random.uniform(10, 50),
            "activityStressPercentage": random.uniform(5, 25),
            "uncategorizedStressPercentage": random.uniform(1, 10),
            "lowStressPercentage": random.uniform(10, 50),
            "mediumStressPercentage": random.uniform(5, 30),
            "highStressPercentage": random.uniform(1, 15),
            "stressQualifier": "CALM_AWAKE",
            "measurableAwakeDuration": random.randint(10000, 70000),
            "measurableAsleepDuration": random.randint(10000, 30000),
            "lastSyncTimestampGMT": None,
            "minAvgHeartRate": random.randint(50, 70),
            "maxAvgHeartRate": random.randint(110, 150),
            "bodyBatteryChargedValue": random.randint(20, 80),
            "bodyBatteryDrainedValue": random.randint(10, 60),
            "bodyBatteryHighestValue": random.randint(30, 100),
            "bodyBatteryLowestValue": random.randint(5, 30),
            "bodyBatteryMostRecentValue": random.randint(10, 60),
            "bodyBatteryDuringSleep": None,
            "bodyBatteryVersion": 2.0,
            "abnormalHeartRateAlertsCount": None,
            "averageSpo2": None,
            "lowestSpo2": None,
            "latestSpo2": None,
            "latestSpo2ReadingTimeGmt": None,
            "latestSpo2ReadingTimeLocal": None,
            "averageMonitoringEnvironmentAltitude": random.uniform(200, 2000),
            "restingCaloriesFromActivity": None,
            "avgWakingRespirationValue": random.uniform(12, 20),
            "highestRespirationValue": random.uniform(15, 25),
            "lowestRespirationValue": random.uniform(8, 15),
            "latestRespirationValue": random.uniform(12, 22),
            "latestRespirationTimeGMT": f"{calendar_date}T07:00:00.0",
        }
        stats_data.append(stats_entry)

    return stats_data


def get_body_composition_data(start_date, num_days):
    """
    Generate synthetic body composition data for a specified date range.

    This function generates synthetic body composition data for a given date range, including weight, BMI, body fat percentage,
    body water percentage, bone mass, muscle mass, physique rating, visceral fat level, and metabolic age. The data is structured
    as a dictionary containing daily weight entries and a total average over the specified date range.

    :param start_date: The starting date for generating body composition data in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_days: The number of days for which to generate body composition data.
    :type num_days: int
    :return: A dictionary containing body composition data for the specified date range.
    :rtype: Dict
    """

    body_composition_data = {
        "startDate": start_date,
        "endDate": (
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=num_days - 1)
        ).strftime("%Y-%m-%d"),
        "dateWeightList": [],
        "totalAverage": {
            "from": datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000,
            "until": (
                datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=num_days)
            ).timestamp()
            * 1000,
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
        },
    }

    return body_composition_data


def get_body_composition_aggregated_data(start_date, num_days):
    """
    Generate synthetic aggregated body composition data for a specified date range.

    This function generates synthetic aggregated body composition data for a given date range. It provides daily aggregated data
    for each day in the specified range, including weight, BMI, body fat percentage, body water percentage, bone mass, muscle mass,
    physique rating, visceral fat level, and metabolic age. The data is structured as a list of dictionaries, each containing
    aggregated data for a single day.

    :param start_date: The starting date for generating aggregated body composition data in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_days: The number of days for which to generate aggregated body composition data.
    :type num_days: int
    :return: A list of dictionaries containing aggregated body composition data for each day in the specified date range.
    :rtype: List[Dict]
    """

    body_composition_aggregated_data = []

    for day in range(num_days):
        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day)
        calendar_date = date.strftime("%Y-%m-%d")
        body_composition_aggregated_entry = {
            "startDate": calendar_date,
            "endDate": calendar_date,
            "dateWeightList": [],
            "totalAverage": {
                "from": datetime.strptime(calendar_date, "%Y-%m-%d").timestamp() * 1000,
                "until": (
                    datetime.strptime(calendar_date, "%Y-%m-%d") + timedelta(days=1)
                ).timestamp()
                * 1000,
                "weight": None,
                "bmi": None,
                "bodyFat": None,
                "bodyWater": None,
                "boneMass": None,
                "muscleMass": None,
                "physiqueRating": None,
                "visceralFat": None,
                "metabolicAge": None,
            },
        }
        body_composition_aggregated_data.append(body_composition_aggregated_entry)

    return body_composition_aggregated_data


def get_stats_and_body_aggregated_data(start_date, num_days):
    """
    Generate synthetic aggregated statistics and body composition data for a specified date range.

    This function generates synthetic aggregated statistics and body composition data for a given date range. It provides daily
    aggregated statistics data (e.g., calories burned, step count) and body composition data (e.g., weight, BMI) for each day in
    the specified range. The data is structured as a list of dictionaries, each containing both statistics and body composition data
    for a single day.

    :param start_date: The starting date for generating aggregated data in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_days: The number of days for which to generate aggregated data.
    :type num_days: int
    :return: A list of dictionaries containing aggregated statistics and body composition data for each day in the specified date range.
    :rtype: List[Dict]
    """

    stats_and_body_aggregated_data = []

    for day in range(num_days):
        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day)
        calendar_date = date.strftime("%Y-%m-%d")
        stats_and_body_aggregated_entry = {
            "stats": {
                "userProfileId": random.randint(10000000, 99999999),
                "totalKilocalories": random.uniform(2000, 3000),
                "activeKilocalories": random.uniform(500, 800),
                "bmrKilocalories": random.uniform(1400, 1700),
                "wellnessKilocalories": random.uniform(2000, 3000),
                "burnedKilocalories": None,
                "consumedKilocalories": None,
                "remainingKilocalories": random.uniform(2000, 3000),
                "totalSteps": random.randint(5000, 10000),
                "netCalorieGoal": None,
                "totalDistanceMeters": random.uniform(3000, 7000),
                "wellnessDistanceMeters": random.uniform(3000, 7000),
                "wellnessActiveKilocalories": random.uniform(500, 800),
                "netRemainingKilocalories": random.uniform(500, 800),
                "userDailySummaryId": random.randint(85000000, 86000000),
                "calendarDate": calendar_date,
                "rule": {"typeId": 3, "typeKey": "subscribers"},
                "uuid": "random-uuid",
                "dailyStepGoal": random.randint(200, 500),
                "wellnessStartTimeGmt": f"{calendar_date}T07:00:00.0",
                "wellnessStartTimeLocal": f"{calendar_date}T00:00:00.0",
                "wellnessEndTimeGmt": (date + timedelta(days=1)).strftime("%Y-%m-%d")
                + "T07:00:00.0",
                "wellnessEndTimeLocal": (date + timedelta(days=1)).strftime("%Y-%m-%d")
                + "T00:00:00.0",
                "durationInMilliseconds": 86400000,
                "wellnessDescription": None,
                "highlyActiveSeconds": random.randint(2000, 3000),
                "activeSeconds": random.randint(7000, 8000),
                "sedentarySeconds": random.randint(70000, 80000),
                "sleepingSeconds": 0,
                "includesWellnessData": True,
                "includesActivityData": False,
                "includesCalorieConsumedData": False,
                "privacyProtected": False,
                "moderateIntensityMinutes": random.randint(15, 30),
                "vigorousIntensityMinutes": random.randint(20, 40),
                "floorsAscendedInMeters": random.uniform(5, 15),
                "floorsDescendedInMeters": random.uniform(5, 15),
                "floorsAscended": random.uniform(2, 5),
                "floorsDescended": random.uniform(2, 5),
                "intensityMinutesGoal": 150,
                "userFloorsAscendedGoal": random.randint(8, 12),
                "minHeartRate": random.randint(50, 60),
                "maxHeartRate": random.randint(110, 120),
                "restingHeartRate": random.randint(60, 70),
                "lastSevenDaysAvgRestingHeartRate": random.randint(60, 70),
                "source": "GARMIN",
                "averageStressLevel": random.randint(30, 50),
                "maxStressLevel": random.randint(90, 100),
                "stressDuration": random.randint(40000, 45000),
                "restStressDuration": random.randint(25000, 30000),
                "activityStressDuration": random.randint(12000, 13000),
                "uncategorizedStressDuration": random.randint(1000, 2000),
                "totalStressDuration": random.randint(80000, 90000),
                "lowStressDuration": random.randint(25000, 30000),
                "mediumStressDuration": random.randint(13000, 14000),
                "highStressDuration": random.randint(3000, 4000),
                "stressPercentage": random.uniform(30, 60),
                "restStressPercentage": random.uniform(20, 40),
                "activityStressPercentage": random.uniform(10, 20),
                "uncategorizedStressPercentage": random.uniform(1, 5),
                "lowStressPercentage": random.uniform(20, 40),
                "mediumStressPercentage": random.uniform(10, 20),
                "highStressPercentage": random.uniform(2, 6),
                "stressQualifier": "CALM_AWAKE",
                "measurableAwakeDuration": random.randint(80000, 84000),
                "measurableAsleepDuration": 0,
                "lastSyncTimestampGMT": None,
                "minAvgHeartRate": random.randint(50, 60),
                "maxAvgHeartRate": random.randint(110, 120),
                "bodyBatteryChargedValue": random.randint(20, 30),
                "bodyBatteryDrainedValue": random.randint(20, 30),
                "bodyBatteryHighestValue": random.randint(30, 40),
                "bodyBatteryLowestValue": random.randint(0, 10),
                "bodyBatteryMostRecentValue": random.randint(0, 10),
                "bodyBatteryDuringSleep": None,
                "bodyBatteryVersion": 2.0,
                "abnormalHeartRateAlertsCount": None,
                "averageSpo2": None,
                "lowestSpo2": None,
                "latestSpo2": None,
                "latestSpo2ReadingTimeGmt": None,
                "latestSpo2ReadingTimeLocal": None,
                "averageMonitoringEnvironmentAltitude": random.uniform(700, 900),
                "restingCaloriesFromActivity": None,
                "avgWakingRespirationValue": random.uniform(15, 20),
                "highestRespirationValue": random.uniform(20, 25),
                "lowestRespirationValue": random.uniform(8, 12),
                "latestRespirationValue": random.uniform(18, 22),
                "latestRespirationTimeGMT": f"{calendar_date}T07:00:00.0",
            },
            "body_composition": {
                "startDate": calendar_date,
                "endDate": calendar_date,
                "dateWeightList": [],
                "totalAverage": {
                    "from": int(date.timestamp() * 1000),
                    "until": int((date + timedelta(days=1)).timestamp() * 1000),
                    "weight": None,
                    "bmi": None,
                    "bodyFat": None,
                    "bodyWater": None,
                    "boneMass": None,
                    "muscleMass": None,
                    "physiqueRating": None,
                    "visceralFat": None,
                    "metabolicAge": None,
                },
            },
        }

        stats_and_body_aggregated_data.append(stats_and_body_aggregated_entry)

    return stats_and_body_aggregated_data


def get_heart_rate_data(start_date, num_days, steps_data):
    """Generate synthetic heart rate data for a specified date range.

    This function generates synthetic heart rate data for a given date range, including various heart rate metrics
    such as resting heart rate, maximum heart rate, minimum heart rate, and additional descriptors and values.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate heart rate data.
    :type num_days: int
    :return: A list of dictionaries, each containing heart rate data for a specific day, including resting heart rate,
        maximum and minimum heart rate, and additional heart rate descriptors and values.
    :rtype: List[Dict]
    """
    heart_rate_data = []

    for _ in range(num_days):
        calendar_date = (
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)
        ).strftime("%Y-%m-%d")
        start_timestamp_gmt = f"{calendar_date}T07:00:00.0"
        end_timestamp_gmt = (
            datetime.strptime(start_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0")
            + timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M:%S.0")
        start_timestamp_local = f"{calendar_date}T00:00:00.0"
        end_timestamp_local = (
            datetime.strptime(start_timestamp_local, "%Y-%m-%dT%H:%M:%S.0")
            + timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M:%S.0")
        resting_heart_rate = random.randint(50, 90)
        max_heart_rate = random.randint(resting_heart_rate + 5, 120)
        min_heart_rate = random.randint(resting_heart_rate + 2, max_heart_rate - 1)

        last_seven_days_avg = random.randint(
            resting_heart_rate - 2, resting_heart_rate + 2
        )

        heart_rate_values = []
        start_datetime = datetime.strptime(start_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0")
        end_datetime = datetime.strptime(end_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0")
        while start_datetime < end_datetime:
            steps_arrdict_day = steps_data[_]
            step_timestamps = np.array(
                [
                    datetime.strptime(x["startGMT"], "%Y-%m-%dT%H:%M:%S.0").timestamp()
                    for x in steps_arrdict_day
                ]
            )
            step_idx = np.where(
                np.logical_and(
                    datetime.strptime(calendar_date, "%Y-%m-%d").timestamp()
                    + 6 * 60 * 60
                    >= step_timestamps,
                    datetime.strptime(calendar_date, "%Y-%m-%d").timestamp()
                    <= step_timestamps + 15 * 60,
                )
            )[0][0]
            step_val_avg = steps_arrdict_day[step_idx]["steps"]
            heart_rate = int(step_val_avg * 0.03 + 80 + np.random.randn() * 5)
            timestamp = int(
                start_datetime.timestamp() * 1000
            )  # Convert to milliseconds
            heart_rate_values.append([timestamp, heart_rate])
            start_datetime += timedelta(minutes=60)

        heart_rate_entry = {
            "userProfilePK": random.randint(10000000, 99999999),
            "calendarDate": calendar_date,
            "startTimestampGMT": start_timestamp_gmt,
            "endTimestampGMT": end_timestamp_gmt,
            "startTimestampLocal": start_timestamp_local,
            "endTimestampLocal": end_timestamp_local,
            "maxHeartRate": max_heart_rate,
            "minHeartRate": min_heart_rate,
            "restingHeartRate": resting_heart_rate,
            "lastSevenDaysAvgRestingHeartRate": last_seven_days_avg,
            "heartRateValueDescriptors": [
                {"key": "timestamp", "index": 0},
                {"key": "heartrate", "index": 1},
            ],
            "heartRateValues": heart_rate_values,
        }

        heart_rate_data.append(heart_rate_entry)

    return heart_rate_data


def get_body_battery_data(start_date, num_days):
    """
    Generate synthetic body battery data for a specified number of days.

    This function creates synthetic data representing the body battery level for each day within the given date range.
    The data includes the starting and ending timestamps, charged and drained values, and an array of body battery levels
    at different times throughout the day. The body battery levels and their corresponding timestamps are randomly generated.

    :param start_date: The start date for generating body battery data in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_days: The number of days for which to generate body battery data, starting from the start_date.
    :type num_days: int
    :return: A list where each item is a list of dictionary containing the date, charged and drained values, timestamps,
        and an array of body battery levels for each time interval within the day.
    :rtype: List[List[Dict]]
    """

    body_battery_data = []

    for day in range(num_days):
        calendar_date = (
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day)
        ).strftime("%Y-%m-%d")
        start_timestamp_gmt = f"{calendar_date}T23:00:00.0"
        end_timestamp_gmt = (
            datetime.strptime(start_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0")
            + timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M:%S.0")
        start_timestamp_local = f"{calendar_date}T00:00:00.0"
        end_timestamp_local = (
            datetime.strptime(start_timestamp_local, "%Y-%m-%dT%H:%M:%S.0")
            + timedelta(days=1)
        ).strftime("%Y-%m-%dT%H:%M:%S.0")

        charged = random.randint(0, 100)
        drained = random.randint(0, 100)

        body_battery_values_array = []
        start_datetime = datetime.strptime(start_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0")
        end_datetime = datetime.strptime(end_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0")
        while start_datetime < end_datetime:
            timestamp = int(
                start_datetime.timestamp() * 1000
            )  # Convert to milliseconds
            body_battery_level = random.randint(0, 100)  # Random body battery level
            body_battery_values_array.append([timestamp, body_battery_level])
            # Assuming 15-minute intervals
            start_datetime += timedelta(minutes=15)

        body_battery_entry = [
            {
                "date": calendar_date,
                "charged": charged,
                "drained": drained,
                "startTimestampGMT": start_timestamp_gmt,
                "endTimestampGMT": end_timestamp_gmt,
                "startTimestampLocal": start_timestamp_local,
                "endTimestampLocal": end_timestamp_local,
                "bodyBatteryValuesArray": body_battery_values_array,
                "bodyBatteryValueDescriptorDTOList": [
                    {
                        "bodyBatteryValueDescriptorIndex": 0,
                        "bodyBatteryValueDescriptorKey": "timestamp",
                    },
                    {
                        "bodyBatteryValueDescriptorIndex": 1,
                        "bodyBatteryValueDescriptorKey": "bodyBatteryLevel",
                    },
                ],
            }
        ]

        body_battery_data.append(body_battery_entry)

    return body_battery_data


def get_training_readiness_data(start_date, num_entries):
    """
    Generate synthetic training readiness data for a specified number of entries.

    This function creates synthetic data representing training readiness metrics, including a variety of factors such as
    sleep score, recovery time, stress history, and heart rate variability (HRV). Each entry is generated for a specific
    calendar date and includes a range of metrics and feedback phrases.

    :param start_date: The start date for generating training readiness data in "YYYY-MM-DD" format.
    :type start_date: str
    :param num_entries: The number of entries for which to generate training readiness data.
    :type num_entries: int
    :return: A list of list of dictionaries, each containing a set of training readiness metrics and feedback for a particular date.
    :rtype: List[List[Dict]]
    """
    training_readiness_data = []

    for _ in range(num_entries):
        user_profile_pk = random.randint(10000000, 99999999)
        calendar_date = (
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)
        ).strftime("%Y-%m-%d")
        timestamp = f"{calendar_date}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.0"
        timestamp_local = (
            datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.0") + timedelta(hours=7)
        ).strftime("%Y-%m-%dT%H:%M:%S.0")
        deviceId = random.randint(1000000000, 9999999999)
        levels = ["LOW", "MODERATE", "HIGH", "VERY_HIGH", "MAXIMUM", "NONE"]
        level = random.choice(levels)
        feedback_long = "UNKNOWN"
        feedback_short = "UNKNOWN"
        score = random.randint(0, 100)  # Random score between 0 and 100
        stress_history_factor_percent = random.randint(0, 100)  # Random percentage
        stress_history_factor_feedback = random.choice(
            ["GOOD", "AVERAGE", "POOR"]
        )  # Random choice of feedback
        sleep_score = random.randint(50, 100)
        sleep_score_factor_percent = random.randint(0, 100)
        sleep_score_factor_feedback = (
            level if sleep_score_factor_percent > 60 else "NONE"
        )
        recovery_time = random.randint(1, 10)
        recovery_time_factor_percent = random.randint(0, 100)
        recovery_time_factor_feedback = (
            level if recovery_time_factor_percent < 40 else "NONE"
        )
        acwr_factor_percent = random.randint(0, 100)
        acwr_factor_feedback = level if acwr_factor_percent > 60 else "NONE"
        hrv_factor_percent = random.randint(0, 100)
        hrv_factor_feedback = level if hrv_factor_percent < 40 else "NONE"
        hrv_weekly_average = random.randint(50, 100)
        sleep_history_factor_percent = random.randint(0, 100)
        sleep_history_factor_feedback = (
            level if sleep_history_factor_percent < 40 else "NONE"
        )

        training_readiness_entry = [
            {
                "userProfilePK": user_profile_pk,
                "calendarDate": calendar_date,
                "timestamp": timestamp,
                "timestampLocal": timestamp_local,
                "deviceId": deviceId,
                "level": level,
                "feedbackLong": feedback_long,
                "feedbackShort": feedback_short,
                "score": score,
                "sleepScore": sleep_score,
                "sleepScoreFactorPercent": sleep_score_factor_percent,
                "sleepScoreFactorFeedback": sleep_score_factor_feedback,
                "recoveryTime": recovery_time,
                "recoveryTimeFactorPercent": recovery_time_factor_percent,
                "recoveryTimeFactorFeedback": recovery_time_factor_feedback,
                "acwrFactorPercent": acwr_factor_percent,
                "acwrFactorFeedback": acwr_factor_feedback,
                "acuteLoad": None,
                "stressHistoryFactorPercent": stress_history_factor_percent,
                "stressHistoryFactorFeedback": stress_history_factor_feedback,
                "hrvFactorPercent": hrv_factor_percent,
                "hrvFactorFeedback": hrv_factor_feedback,
                "hrvWeeklyAverage": hrv_weekly_average,
                "sleepHistoryFactorPercent": sleep_history_factor_percent,
                "sleepHistoryFactorFeedback": sleep_history_factor_feedback,
                "validSleep": True,
                "recoveryTimeChangePhrase": None,
            },
        ]

        training_readiness_data.append(training_readiness_entry)

    return training_readiness_data


def get_blood_pressure_data(start_date, end_date, num_summaries):
    """Generate synthetic blood pressure data summaries for a specified date range.

    This function generates synthetic blood pressure data summaries for a given date range,
    including various blood pressure measurements and category statistics.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date in the format "YYYY-MM-DD".
    :type end_date: str
    :param num_summaries: The number of blood pressure data summaries to generate.
    :type num_summaries: int
    :return: A dictionary containing blood pressure data for the specified date range,
        including measurement summaries and category statistics.
    :rtype: dict
    """

    blood_pressure_data = {
        "from": start_date,
        "until": end_date,
        "measurementSummaries": [],
        "categoryStats": None,
    }

    return blood_pressure_data


def get_floors_data(start_date, num_days):
    """Generate synthetic floors climbed data for a specified date range.

    This function generates synthetic data for the number of floors climbed for each day within the specified date range.
    The data includes descriptors and floor values for each day, and the date range is determined by the start and end dates.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date in the format "YYYY-MM-DD".
    :type end_date: str
    :return: A list of dictionaries, each containing the start and end timestamps, a descriptor, and a floor value
        for each day within the specified date range.
    :rtype: List[Dict]
    """
    floors_data = []

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for day in range(num_days):
        day_date = start_date_obj + timedelta(days=day)
        start_timestamp_gmt = day_date.strftime("%Y-%m-%dT07:00:00.0")
        end_timestamp_gmt = (day_date + timedelta(days=1)).strftime(
            "%Y-%m-%dT07:00:00.0"
        )
        start_timestamp_local = day_date.strftime("%Y-%m-%dT00:00:00.0")
        end_timestamp_local = (day_date + timedelta(days=1)).strftime(
            "%Y-%m-%dT00:00:00.0"
        )

        floors_entry = {
            "startTimestampGMT": start_timestamp_gmt,
            "endTimestampGMT": end_timestamp_gmt,
            "startTimestampLocal": start_timestamp_local,
            "endTimestampLocal": end_timestamp_local,
            "floorsValueDescriptorDTOList": [
                {"key": "startTimeGMT", "index": 0},
                {"key": "endTimeGMT", "index": 1},
                {"key": "floorsAscended", "index": 2},
                {"key": "floorsDescended", "index": 3},
            ],
            "floorValuesArray": [],
        }

        for hour in range(7, 24):
            for minute in range(0, 60, 15):
                time_slot = day_date.replace(hour=hour, minute=minute)
                next_time_slot = time_slot + timedelta(minutes=15)
                # Random number of floors ascended
                floors_ascended = random.randint(0, 10)
                # Random number of floors descended
                floors_descended = random.randint(0, 10)

                floor_value = [
                    time_slot.strftime("%Y-%m-%dT%H:%M:%S.0"),
                    next_time_slot.strftime("%Y-%m-%dT%H:%M:%S.0"),
                    floors_ascended,
                    floors_descended,
                ]
                floors_entry["floorValuesArray"].append(floor_value)

        floors_data.append(floors_entry)

    return floors_data


def get_training_status_data(start_date, num_days):
    """Generate synthetic floors climbed and descended data for a specified date range.

    This function generates synthetic floors climbed and descended data summaries for a given date range,
    including start and end timestamps, floors ascended, and floors descended for each time slot.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate floors data.
    :type num_days: int
    :return: A list of dictionaries, each containing floors data for a specific day, including
        start and end timestamps, floors ascended, and floors descended for each time slot.
    :rtype: List[Dict]
    """
    training_status_data = []

    for _ in range(num_days):
        calendar_date = (
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)
        ).strftime("%Y-%m-%d")
        training_status_entry = {
            "userId": random.randint(10000000, 99999999),
            "mostRecentVO2Max": None,
            "mostRecentTrainingLoadBalance": None,
            "mostRecentTrainingStatus": None,
            "heatAltitudeAcclimationDTO": None,
        }
        training_status_data.append(training_status_entry)

    return training_status_data


def get_resting_hr_data(start_date, num_days):
    """Generate synthetic resting heart rate data for a specified date range.

    This function generates synthetic resting heart rate data summaries for a given date range,
    including resting heart rate values for each day.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate resting heart rate data.
    :type num_days: int
    :return: A dictionary containing resting heart rate data for the specified date range,
        including user profile ID, statistics start and end dates, and a list of daily resting
        heart rate values.
    :rtype: dict
    """

    resting_hr_data = {
        "userProfileId": random.randint(10000000, 99999999),
        "statisticsStartDate": start_date,
        "statisticsEndDate": (
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=num_days - 1)
        ).strftime("%Y-%m-%d"),
        "allMetrics": {
            "metricsMap": {"WELLNESS_RESTING_HEART_RATE": []},
        },
        "groupedMetrics": None,
    }

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for day in range(num_days):
        current_date = start_date_obj + timedelta(days=day)
        # Random resting heart rate between 50 and 100 bpm
        resting_hr_value = random.randint(50, 100)
        resting_hr_entry = {
            "value": resting_hr_value,
            "calendarDate": current_date.strftime("%Y-%m-%d"),
        }

        resting_hr_data["allMetrics"]["metricsMap"][
            "WELLNESS_RESTING_HEART_RATE"
        ].append(resting_hr_entry)

    return resting_hr_data


def get_hydration_data(start_date, num_days):
    """Generate synthetic hydration data for a specified date range.

    This function generates synthetic hydration data summaries for a given date range,
    including user-specific hydration information for each day.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate hydration data.
    :type num_days: int
    :return: A list of dictionaries, each containing hydration data for a specific day, including
        user ID, calendar date, hydration value, hydration goal, daily average, last entry timestamp,
        sweat loss, and activity intake.
    :rtype: List[Dict]
    """
    hydration_data = []

    for _ in range(num_days):
        user_id = random.randint(10000000, 99999999)
        calendar_date = (
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)
        ).strftime("%Y-%m-%d")
        value_in_ml = None
        goal_in_ml = random.uniform(1800.0, 2500.0)
        daily_average_in_ml = None
        last_entry_timestamp_local = None
        sweat_loss_in_ml = None
        activity_intake_in_ml = None

        hydration_entry = {
            "userId": user_id,
            "calendarDate": calendar_date,
            "valueInML": value_in_ml,
            "goalInML": goal_in_ml,
            "dailyAverageinML": daily_average_in_ml,
            "lastEntryTimestampLocal": last_entry_timestamp_local,
            "sweatLossInML": sweat_loss_in_ml,
            "activityIntakeInML": activity_intake_in_ml,
        }

        hydration_data.append(hydration_entry)

    return hydration_data


def get_sleep_data(start_date, num_days):
    """Generate synthetic sleep data for a specified date range.

    This function generates synthetic sleep data summaries for a given date range,
    including various sleep metrics such as sleep time, deep sleep, light sleep, REM sleep,
    awake sleep, respiration values, and sleep quality scores for each day.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate sleep data.
    :type num_days: int
    :return: A list of dictionaries, each containing sleep data for a specific day, including
        sleep time, sleep quality, respiration values, and sleep quality scores.
    :rtype: List[Dict]
    """
    sleep_data = []

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for day in range(num_days):
        current_date = start_date_obj + timedelta(days=day)
        sleep_time_seconds = random.randint(6 * 3600, 9 * 3600)  # Between 6 and 9 hours
        deep_sleep_seconds = random.randint(1 * 3600, 3 * 3600)  # Between 1 and 3 hours
        light_sleep_seconds = random.randint(
            2 * 3600, 4 * 3600
        )  # Between 2 and 4 hours
        rem_sleep_seconds = (
            sleep_time_seconds - deep_sleep_seconds - light_sleep_seconds
        )
        awake_sleep_seconds = random.randint(
            5 * 60, 20 * 60
        )  # Between 5 and 20 minutes
        avg_respiration_value = random.uniform(12.0, 20.0)
        lowest_respiration_value = avg_respiration_value - random.uniform(0.5, 2.0)
        highest_respiration_value = avg_respiration_value + random.uniform(0.5, 2.0)
        awake_count = random.randint(0, 4)

        sleep_start_timestamp_gmt = int(current_date.timestamp() * 1000)
        sleep_end_timestamp_gmt = int(
            (current_date + timedelta(seconds=sleep_time_seconds)).timestamp() * 1000
        )
        sleep_start_timestamp_local = sleep_start_timestamp_gmt
        sleep_end_timestamp_local = sleep_end_timestamp_gmt

        total_duration_score = random.randint(0, 100)
        stress_score = random.randint(0, 100)
        awake_count_score = random.randint(0, 100)
        overall_score = random.randint(0, 100)
        rem_percentage = random.randint(10, 30)
        light_percentage = random.randint(40, 70)
        deep_percentage = random.randint(20, 40)

        sleep_entry = {
            "dailySleepDTO": {
                "id": random.randint(1000000000000, 9999999999999),
                "userProfilePK": random.randint(10000000, 99999999),
                "calendarDate": current_date.strftime("%Y-%m-%d"),
                "sleepTimeSeconds": sleep_time_seconds,
                "napTimeSeconds": 0,
                "sleepWindowConfirmed": True,
                "sleepWindowConfirmationType": "enhanced_confirmed_final",
                "sleepStartTimestampGMT": sleep_start_timestamp_gmt,
                "sleepEndTimestampGMT": sleep_end_timestamp_gmt,
                "sleepStartTimestampLocal": sleep_start_timestamp_local,
                "sleepEndTimestampLocal": sleep_end_timestamp_local,
                "autoSleepStartTimestampGMT": None,
                "autoSleepEndTimestampGMT": None,
                "sleepQualityTypePK": None,
                "sleepResultTypePK": None,
                "unmeasurableSleepSeconds": 0,
                "deepSleepSeconds": deep_sleep_seconds,
                "lightSleepSeconds": light_sleep_seconds,
                "remSleepSeconds": rem_sleep_seconds,
                "awakeSleepSeconds": awake_sleep_seconds,
                "deviceRemCapable": True,
                "retro": False,
                "sleepFromDevice": True,
                "averageRespirationValue": avg_respiration_value,
                "lowestRespirationValue": lowest_respiration_value,
                "highestRespirationValue": highest_respiration_value,
                "awakeCount": awake_count,
                "avgSleepStress": random.uniform(20.0, 30.0),
                "ageGroup": "ADULT",
                "sleepScoreFeedback": "NEGATIVE_LONG_BUT_NOT_ENOUGH_REM",
                "sleepScoreInsight": "NONE",
                "sleepScores": {
                    "totalDuration": {
                        "value": total_duration_score,
                        "qualifierKey": "POOR",
                    },
                    "stress": {"value": stress_score, "qualifierKey": "FAIR"},
                    "awakeCount": {"value": awake_count_score, "qualifierKey": "POOR"},
                    "overall": {"value": overall_score, "qualifierKey": "POOR"},
                    "remPercentage": {"value": rem_percentage, "qualifierKey": "POOR"},
                    "lightPercentage": {
                        "value": light_percentage,
                        "qualifierKey": "GOOD",
                    },
                    "deepPercentage": {
                        "value": deep_percentage,
                        "qualifierKey": "EXCELLENT",
                    },
                },
                "sleepVersion": 2,
            },
            "sleepMovement": None,
            "remSleepData": True,
            "sleepLevels": None,
            "restingHeartRate": random.randint(50, 70),
        }

        sleep_data.append(sleep_entry)

    return sleep_data


def get_earned_badges_data(start_date, num_days):
    """Generate synthetic earned badges data for a specified date range.

    This function generates synthetic earned badges data for a given date range,
    including information about badges earned by users, such as badge names, categories,
    points, and earned dates.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate earned badges data.
    :type num_days: int
    :return: A list of dictionaries, each containing information about badges earned by users,
        including badge ID, name, category, points, and earned date.
    :rtype: List[Dict]
    """
    earned_badges_data = []

    badge_names = ["Badge 1", "Badge 2", "Badge 3"]
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(100):
        badge_earned_date = start_date_obj + timedelta(
            days=random.randint(0, 365)
        )  # Random date within a year
        badge_earned_date_str = badge_earned_date.strftime("%Y-%m-%dT06:59:59.0")

        earned_badge_entry = {
            "badgeId": random.randint(1, 100),
            "badgeKey": "RANDOM",
            "badgeName": random.choice(badge_names),
            "badgeUuid": None,
            "badgeCategoryId": random.randint(1, 10),
            "badgeDifficultyId": random.randint(1, 3),
            "badgePoints": random.randint(1, 5),
            "badgeTypeIds": [random.randint(1, 5)],
            "badgeSeriesId": random.randint(1, 20),
            "badgeStartDate": start_date,
            "badgeEndDate": None,
            "userProfileId": random.randint(10000000, 99999999),
            "fullName": "UNKNOWN",
            "displayName": "UNKNOWN",
            "badgeEarnedDate": badge_earned_date_str,
            "badgeEarnedNumber": random.randint(1, 10),
            "badgeLimitCount": None,
            "badgeIsViewed": True,
            "badgeProgressValue": random.uniform(0.0, 10.0),
            "badgeTargetValue": random.uniform(0.0, 10.0),
            "badgeUnitId": random.randint(1, 5),
            "badgeAssocTypeId": random.randint(1, 5),
            "badgeAssocDataId": None,
            "badgeAssocDataName": None,
            "earnedByMe": True,
            "currentPlayerType": None,
            "userJoined": None,
            "badgeChallengeStatusId": None,
            "badgePromotionCodeTypeList": [None],
            "promotionCodeStatus": None,
            "createDate": badge_earned_date_str,
            "relatedBadges": None,
            "connectionNumber": None,
            "connections": None,
        }

        earned_badges_data.append(earned_badge_entry)

    return earned_badges_data


def get_stress_data(start_date, num_days):
    """Generate synthetic stress data for a specified date range.

    This function generates synthetic stress data summaries for a given date range,
    including stress levels for each day and timestamps for stress level measurements.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate stress data.
    :type num_days: int
    :return: A list of dictionaries, each containing stress data for a specific day, including
        user profile ID, calendar date, stress levels, and timestamps for stress level measurements.
    :rtype: List[Dict]
    """
    stress_data = []

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        date = (start_date_obj + timedelta(days=i)).strftime("%Y-%m-%d")

        stress_entry = {
            "userProfilePK": random.randint(10000000, 99999999),
            "calendarDate": date,
            "startTimestampGMT": f"{date}T07:00:00.0",
            "endTimestampGMT": f"{date}T07:00:00.0",
            "startTimestampLocal": f"{date}T00:00:00.0",
            "endTimestampLocal": f"{date}T00:00:00.0",
            "maxStressLevel": random.randint(70, 100),
            "avgStressLevel": random.randint(20, 50),
            "stressChartValueOffset": 1,
            "stressChartYAxisOrigin": -1,
            "stressValueDescriptorsDTOList": [],
            "stressValuesArray": [],
        }

        for j in range(24 * 4):
            timestamp = int(
                (start_date_obj + timedelta(days=i, minutes=j * 15)).timestamp() * 1000
            )
            stress_level = random.randint(10, 99)
            stress_entry["stressValuesArray"].append([timestamp, stress_level])

        stress_data.append(stress_entry)

    return stress_data


def get_day_stress_aggregated_data(start_date, num_days):
    """Generate synthetic day-wise stress and body battery aggregated data for a specified date range.

    This function generates synthetic day-wise aggregated stress and body battery data summaries
    for a given date range, including stress levels, body battery status, and timestamps.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate aggregated data.
    :type num_days: int
    :return: A list of dictionaries, each containing aggregated stress and body battery data for a specific day, including
        user profile ID, calendar date, maximum and average stress levels, stress level timestamps, body battery status,
        body battery level, and timestamps for body battery measurements.
    :rtype: List[Dict]
    """
    day_stress_aggregated_data = []
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        current_date = start_date_obj + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")

        stress_values = []
        body_battery_values = []
        for j in range(24 * 4):  # Assuming readings every 15 minutes
            timestamp = int(
                (current_date + timedelta(minutes=15 * j)).timestamp() * 1000
            )
            stress_level = random.randint(25, 100)
            body_battery_status = random.choice(["MEASURED", "ESTIMATED"])
            body_battery_level = random.randint(0, 100)
            stress_values.append([timestamp, stress_level])
            body_battery_values.append(
                [timestamp, body_battery_status, body_battery_level, 2.0]
            )

        day_stress_aggregated_entry = {
            "userProfilePK": random.randint(10000000, 99999999),
            "calendarDate": date_str,
            "maxStressLevel": random.randint(90, 100),
            "avgStressLevel": random.randint(30, 50),
            "stressValueDescriptorsDTOList": [
                {"key": "timestamp", "index": 0},
                {"key": "stressLevel", "index": 1},
            ],
            "bodyBatteryValueDescriptorsDTOList": [
                {
                    "bodyBatteryValueDescriptorIndex": 0,
                    "bodyBatteryValueDescriptorKey": "timestamp",
                },
                {
                    "bodyBatteryValueDescriptorIndex": 1,
                    "bodyBatteryValueDescriptorKey": "bodyBatteryStatus",
                },
                {
                    "bodyBatteryValueDescriptorIndex": 2,
                    "bodyBatteryValueDescriptorKey": "bodyBatteryLevel",
                },
                {
                    "bodyBatteryValueDescriptorIndex": 3,
                    "bodyBatteryValueDescriptorKey": "bodyBatteryVersion",
                },
            ],
            "stressValuesArray": stress_values,
            "bodyBatteryValuesArray": body_battery_values,
        }

        day_stress_aggregated_data.append(day_stress_aggregated_entry)

    return day_stress_aggregated_data


def get_respiration_data(start_date, num_days):
    """Generate synthetic respiration data for a specified date range.

    This function generates synthetic respiration data summaries for a given date range,
    including respiration values, timestamps, and sleep-related respiration metrics.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate respiration data.
    :type num_days: int
    :return: A list of dictionaries, each containing respiration data for a specific day, including
        user profile ID, calendar date, respiration values, sleep-related respiration metrics, and timestamps.
    :rtype: List[Dict]
    """
    respiration_data = []

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        current_date = start_date_obj + timedelta(days=i)
        date = current_date.strftime("%Y-%m-%d")

        respiration_entry = {
            "userProfilePK": random.randint(10000000, 99999999),
            "calendarDate": date,
            "startTimestampGMT": f"{date}T07:00:00.0",
            "endTimestampGMT": f"{date}T07:00:00.0",
            "startTimestampLocal": f"{date}T00:00:00.0",
            "endTimestampLocal": f"{date}T00:00:00.0",
            "sleepStartTimestampGMT": f"{date}T05:53:00.0",
            "sleepEndTimestampGMT": f"{date}T13:48:00.0",
            "sleepStartTimestampLocal": f"{date}T22:53:00.0",
            "sleepEndTimestampLocal": f"{date}T06:48:00.0",
            "tomorrowSleepStartTimestampGMT": f"{date}T05:39:00.0",
            "tomorrowSleepEndTimestampGMT": f"{date}T14:16:00.0",
            "tomorrowSleepStartTimestampLocal": f"{date}T22:39:00.0",
            "tomorrowSleepEndTimestampLocal": f"{date}T07:16:00.0",
            "lowestRespirationValue": random.uniform(10.0, 15.0),
            "highestRespirationValue": random.uniform(20.0, 25.0),
            "avgWakingRespirationValue": random.uniform(12.0, 18.0),
            "avgSleepRespirationValue": random.uniform(16.0, 22.0),
            "avgTomorrowSleepRespirationValue": random.uniform(16.0, 22.0),
            "respirationValueDescriptorsDTOList": [],
            "respirationValuesArray": [],
        }

        for j in range(24 * 4):
            timestamp = int(
                (current_date + timedelta(minutes=15 * j)).timestamp() * 1000
            )
            respiration_value = random.uniform(10.0, 25.0)
            respiration_entry["respirationValuesArray"].append(
                [timestamp, respiration_value]
            )

        respiration_data.append(respiration_entry)
    return respiration_data


def get_spo2_data(start_date, num_days):
    """Generate synthetic SpO2 (Blood Oxygen Saturation) data for a specified date range.

    This function generates synthetic SpO2 data summaries for a given date range, including user profile ID,
    calendar date, sleep-related SpO2 metrics, and timestamps.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which to generate SpO2 data.
    :type num_days: int
    :return: A list of dictionaries, each containing SpO2 data for a specific day, including user profile ID, calendar date,
        sleep-related SpO2 metrics, and timestamps.
    :rtype: List[Dict]
    """
    spo2_data = []

    for i in range(num_days):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime(
            "%Y-%m-%d"
        )

        spo2_entry = {
            "userProfilePK": random.randint(10000000, 99999999),
            "calendarDate": date,
            "startTimestampGMT": f"{date}T07:00:00.0",
            "endTimestampGMT": f"{date}T07:00:00.0",
            "startTimestampLocal": f"{date}T00:00:00.0",
            "endTimestampLocal": f"{date}T00:00:00.0",
            "sleepStartTimestampGMT": f"{date}T05:53:00.0",
            "sleepEndTimestampGMT": f"{date}T13:48:00.0",
            "sleepStartTimestampLocal": f"{date}T22:53:00.0",
            "sleepEndTimestampLocal": f"{date}T06:48:00.0",
            "tomorrowSleepStartTimestampGMT": f"{date}T05:39:00.0",
            "tomorrowSleepEndTimestampGMT": f"{date}T14:16:00.0",
            "tomorrowSleepStartTimestampLocal": f"{date}T22:39:00.0",
            "tomorrowSleepEndTimestampLocal": f"{date}T07:16:00.0",
            "averageSpO2": None,
            "lowestSpO2": None,
            "lastSevenDaysAvgSpO2": None,
            "latestSpO2": None,
            "latestSpO2TimestampGMT": None,
            "latestSpO2TimestampLocal": None,
            "avgSleepSpO2": None,
            "avgTomorrowSleepSpO2": None,
            "spO2ValueDescriptorsDTOList": None,
            "spO2SingleValues": None,
            "continuousReadingDTOList": None,
            "spO2HourlyAverages": None,
        }

        spo2_data.append(spo2_entry)

    return spo2_data


def get_metrics_data(start_date, num_days):
    """Generate synthetic "max_metrics" data for a specified number of days.

    This function generates synthetic "max_metrics" data for a specified number of days. It simulates various metrics like
    vo2MaxPreciseValue and vo2MaxValue for users with random values. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which "max_metrics" data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing "max_metrics" data for the specified number of days.
    :rtype: List[Dict]
    """
    max_metrics_data = []

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        date = (start_date_obj + timedelta(days=i)).strftime("%Y-%m-%d")

        max_metrics_entry = [
            {
                "userId": random.randint(10000000, 99999999),
                "generic": {
                    "calendarDate": date,
                    "vo2MaxPreciseValue": random.uniform(30.0, 50.0),
                    "vo2MaxValue": random.randint(30, 50),
                    "fitnessAge": random.randint(20, 50),
                    "fitnessAgeDescription": "MODERATE",
                    "maxMetCategory": random.randint(0, 3),
                },
                "cycling": None,
                "heatAltitudeAcclimation": {
                    "calendarDate": date,
                    "altitudeAcclimationDate": date,
                    "previousAltitudeAcclimationDate": date,
                    "heatAcclimationDate": date,
                    "previousHeatAcclimationDate": date,
                    "altitudeAcclimation": random.randint(0, 100),
                    "previousAltitudeAcclimation": random.randint(0, 100),
                    "heatAcclimationPercentage": random.randint(0, 100),
                    "previousHeatAcclimationPercentage": random.randint(0, 100),
                    "heatTrend": "STABLE",
                    "altitudeTrend": "STABLE",
                    "currentAltitude": random.randint(100, 1000),
                    "previousAltitude": random.randint(100, 1000),
                    "acclimationPercentage": random.randint(0, 100),
                    "previousAcclimationPercentage": random.randint(0, 100),
                    "altitudeAcclimationLocalTimestamp": f"{date}T23:55:52.0",
                },
            }
        ]

        max_metrics_data.append(max_metrics_entry)
    return max_metrics_data


def random_datetime(start_date, end_date):
    """
    Generate a random datetime within a specified date range.

    This function generates a random datetime within the specified start and end dates.

    :param start_date: The start date as a datetime object.
    :type start_date: datetime.datetime
    :param end_date: The end date as a datetime object.
    :type end_date: datetime.datetime
    :return: A random datetime between start_date (inclusive) and end_date (exclusive).
    :rtype: datetime.datetime
    """
    start_timestamp = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
    end_timestamp = datetime.strptime(end_date, "%Y-%m-%d").timestamp()
    random_timestamp = start_timestamp + random.random() * (
        end_timestamp - start_timestamp
    )
    return datetime.fromtimestamp(random_timestamp)


def get_personal_record_data(start_date, end_date, num_entries):
    """Generate synthetic personal record data for a specified date range.

    This function generates synthetic personal record data for a given date range. Each personal record entry contains
    information such as the type of record, activity details, start timestamps (GMT and local), and the recorded value.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date in the format "YYYY-MM-DD".
    :type end_date: str
    :param num_entries: The number of personal record entries to generate.
    :type num_entries: int
    :return: A list of dictionaries, each containing personal record data, including type, activity details, timestamps, and recorded value.
    :rtype: List[Dict]
    """
    personal_record_data = []

    for _ in range(num_entries):
        personal_record_entry = {
            "id": random.randint(1000000000, 9999999999),
            "typeId": random.randint(1, 16),
            "activityId": 0,
            "activityName": None,
            "activityType": None,
            "activityStartDateTimeInGMT": None,
            "actStartDateTimeInGMTFormatted": None,
            "activityStartDateTimeLocal": None,
            "activityStartDateTimeLocalFormatted": None,
            "value": round(random.uniform(10, 1000000), 2),
            "prTypeLabelKey": None,
            "poolLengthUnit": None,
        }

        personal_record_entry["prStartTimeGmt"] = int(
            random_datetime(start_date, end_date).timestamp() * 1000
        )
        personal_record_entry["prStartTimeGmtFormatted"] = datetime.utcfromtimestamp(
            personal_record_entry["prStartTimeGmt"] / 1000
        ).strftime("%Y-%m-%dT%H:%M:%S.0")

        personal_record_entry["prStartTimeLocal"] = int(
            random_datetime(start_date, end_date).timestamp() * 1000
        )
        personal_record_entry["prStartTimeLocalFormatted"] = datetime.fromtimestamp(
            personal_record_entry["prStartTimeLocal"] / 1000
        ).strftime("%Y-%m-%dT%H:%M:%S.0")

        personal_record_data.append(personal_record_entry)

    return personal_record_data


def get_activities_data(start_date, num_days):
    """Generate synthetic activity data for a specified number of days.

    This function generates synthetic activity data for a specified number of days. It simulates activities with random
    start times, durations, distances, elevation gains, and other attributes. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which activity data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic activity data for the specified number of days.
    :rtype: List[Dict]
    """

    activities_data = []
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        activity_start_time = start_date_obj + timedelta(days=i)
        # Between 30 minutes and 3 hours
        activity_duration = random.randint(30 * 60, 3 * 60 * 60)
        distance = random.uniform(0.0, 15.0)  # Up to 15 km
        elevation_gain = random.uniform(0.0, 500.0)  # Up to 500 meters
        elevation_loss = random.uniform(0.0, 500.0)  # Up to 500 meters
        # Average speed in km/h
        avg_speed = distance / (activity_duration / 3600)

        activity_entry = {
            "activityId": random.randint(10000000, 99999999),
            "activityName": "Random Activity",
            "description": None,
            "startTimeLocal": activity_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "startTimeGMT": activity_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "activityType": {
                "typeId": random.randint(1, 20),
                "typeKey": "random_activity",
                "parentTypeId": random.randint(1, 20),
                "isHidden": False,
                "restricted": False,
                "trimmable": True,
            },
            "eventType": {
                "typeId": random.randint(1, 10),
                "typeKey": "uncategorized",
                "sortOrder": 10,
            },
            "comments": None,
            "parentId": None,
            "distance": distance,
            "duration": activity_duration,
            "elapsedDuration": activity_duration,
            "movingDuration": random.randint(20 * 60, activity_duration),
            "elevationGain": elevation_gain,
            "elevationLoss": elevation_loss,
            "averageSpeed": avg_speed,
            "maxSpeed": avg_speed + random.uniform(0.0, 5.0),
            "startLatitude": random.uniform(-90.0, 90.0),
            "startLongitude": random.uniform(-180.0, 180.0),
            "hasPolyline": True,
            "ownerId": random.randint(10000000, 99999999),
            "ownerDisplayName": "Random User",
            "ownerFullName": "Random User",
        }

        activities_data.append(activity_entry)

    return activities_data


def get_devices_data(start_date, num_days):
    """Generate synthetic device data for a specified number of days.

    This function generates synthetic device data for a specified number of days. It simulates various device attributes
    for multiple devices. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which device data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic device data for the specified number of days.
    :rtype: List[Dict]
    """
    devices_data = []

    devices_entry = {
        "userProfilePk": random.randint(10000000, 99999999),
        "unitId": random.randint(1000000000, 9999999999),
        "deviceId": random.randint(1000000000, 9999999999),
        "appSupport": True,
        "applicationKey": "fenix7s",
        "deviceTypePk": 36879,
        "bestInClassVideoLink": None,
        "bluetoothClassicDevice": False,
        "bluetoothLowEnergyDevice": True,
        "deviceCategories": ["FITNESS", "WELLNESS", "GOLF", "OUTDOOR"],
        "deviceEmbedVideoLink": None,
        "deviceSettingsFile": "RealTimeDeviceSettings_RANDOM.json",
        "gcmSettingsFile": "Fenix7S_RANDOM.json",
        "deviceVideoPageLink": None,
        "displayOrder": 0,
        "golfDisplayOrder": 0,
        "hasOpticalHeartRate": True,
        "highlighted": False,
        "hybrid": True,
        "imageUrl": "https://static.garmincdn.com/en/products/010-02539-00/v/cf-sm-2x3-d013b003-7e67-4db4-90c2-7fbd03f40a7c.png",
        "minGCMAndroidVersion": 6411,
        "minGCMWindowsVersion": 99999,
        "minGCMiOSVersion": 10320,
        "minGolfAppiOSVersion": 0,
        "minGolfAppAndroidVersion": 0,
        "partNumber": "006-B3905-00",
        "primary": True,
        "productDisplayName": "fenix 7S",
        "deviceTags": None,
        "productSku": "010-02539-00",
        "wasp": False,
        "weightScale": False,
        "wellness": False,
        "wifi": True,
        "hasPowerButton": True,
        "supportsSecondaryUsers": False,
        "primaryApplication": "UNSPECIFIED",
        "incompatibleApplications": [],
        "abnormalHeartRateAlertCapable": True,
        "activitySummFitFileCapable": True,
        "aerobicTrainingEffectCapable": True,
        "alarmDaysCapable": True,
        "allDayStressCapable": True,
        "anaerobicTrainingEffectCapable": True,
        "atpWorkoutCapable": True,
        "bodyBatteryCapable": True,
        "brickWorkoutCapable": True,
        "cardioCapable": True,
        "cardioOptionCapable": False,
        "cardioSportsCapable": False,
        "cardioWorkoutCapable": True,
        "cellularCapable": False,
        "changeLogCapable": True,
        "contactManagementCapable": True,
        "courseCapable": True,
        "courseFileType": "FIT",
        "coursePromptCapable": False,
        "customIntensityMinutesCapable": True,
        "customWorkoutCapable": True,
        "cyclingSegmentCapable": True,
        "cyclingSportsCapable": False,
        "cyclingWorkoutCapable": True,
        "defaultSettingCapable": True,
        "deviceSettingCapable": True,
        "deviceSettingFileType": None,
        "displayFieldsExtCapable": False,
        "divingCapable": False,
        "ellipticalOptionCapable": False,
        "floorsClimbedGoalCapable": True,
        "ftpCapable": True,
        "gcj02CourseCapable": False,
        "glonassCapable": True,
        "goalCapable": True,
        "goalFileType": "FIT",
        "golfAppSyncCapable": False,
        "gpsRouteCapable": True,
        "handednessCapable": True,
        "hrZoneCapable": True,
        "hrvStressCapable": True,
        "intensityMinutesGoalCapable": True,
        "lactateThresholdCapable": True,
        "languageSettingCapable": True,
        "languageSettingFileType": None,
        "lowHrAlertCapable": True,
        "maxHRCapable": True,
        "maxWorkoutCount": 200,
        "metricsFitFileReceiveCapable": True,
        "metricsUploadCapable": True,
        "militaryTimeCapable": True,
        "moderateIntensityMinutesGoalCapable": True,
        "nfcCapable": True,
        "otherOptionCapable": False,
        "otherSportsCapable": False,
        "personalRecordCapable": True,
        "personalRecordFileType": "FIT",
        "poolSwimOptionCapable": False,
        "powerCurveCapable": True,
        "powerZonesCapable": True,
        "pulseOxAllDayCapable": True,
        "pulseOxOnDemandCapable": True,
        "pulseOxSleepCapable": True,
        "remCapable": True,
        "reminderAlarmCapable": False,
        "reorderablePagesCapable": False,
        "restingHRCapable": True,
        "rideOptionsCapable": False,
        "runOptionIndoorCapable": False,
        "runOptionsCapable": False,
        "runningSegmentCapable": True,
        "runningSportsCapable": False,
        "runningWorkoutCapable": True,
        "scheduleCapable": True,
        "scheduleFileType": "FIT",
        "segmentCapable": True,
        "segmentPointCapable": True,
        "settingCapable": True,
        "settingFileType": "FIT",
        "sleepTimeCapable": True,
        "smallFitFileOnlyCapable": False,
        "sportCapable": True,
        "sportFileType": "FIT",
        "stairStepperOptionCapable": False,
        "strengthOptionsCapable": False,
        "strengthWorkoutCapable": True,
        "supportedHrZones": ["RUNNING", "CYCLING", "SWIMMING", "ALL"],
        "swimWorkoutCapable": True,
        "trainingPlanCapable": True,
        "trainingStatusCapable": True,
        "trainingStatusPauseCapable": True,
        "userProfileCapable": False,
        "userProfileFileType": None,
        "userTcxExportCapable": False,
        "vo2MaxBikeCapable": True,
        "vo2MaxRunCapable": True,
        "walkOptionCapable": False,
        "walkingSportsCapable": False,
        "weatherAlertsCapable": False,
        "weatherSettingsCapable": False,
        "workoutCapable": True,
        "workoutFileType": "FIT",
        "yogaCapable": True,
        "yogaOptionCapable": False,
        "heatAndAltitudeAcclimationCapable": True,
        "trainingLoadBalanceCapable": True,
        "indoorTrackOptionsCapable": False,
        "indoorBikeOptionsCapable": False,
        "indoorWalkOptionsCapable": False,
        "trainingEffectLabelCapable": True,
        "pacebandCapable": True,
        "respirationCapable": True,
        "openWaterSwimOptionCapable": False,
        "phoneVerificationCheckRequired": False,
        "weightGoalCapable": False,
        "yogaWorkoutCapable": True,
        "pilatesWorkoutCapable": True,
        "connectedGPSCapable": False,
        "diveAppSyncCapable": False,
        "golfLiveScoringCapable": True,
        "solarPanelUtilizationCapable": False,
        "sweatLossCapable": True,
        "diveAlertCapable": False,
        "requiresInitialDeviceNickname": False,
        "defaultSettingsHbaseMigrated": True,
        "sleepScoreCapable": True,
        "fitnessAgeV2Capable": True,
        "intensityMinutesV2Capable": True,
        "collapsibleControlMenuCapable": False,
        "measurementUnitSettingCapable": False,
        "onDeviceSleepCalculationCapable": True,
        "hiitWorkoutCapable": True,
        "runningHeartRateZoneCapable": True,
        "cyclingHeartRateZoneCapable": True,
        "swimmingHeartRateZoneCapable": True,
        "defaultHeartRateZoneCapable": True,
        "cyclingPowerZonesCapable": True,
        "xcSkiPowerZonesCapable": True,
        "swimAlgorithmCapable": True,
        "benchmarkExerciseCapable": True,
        "spectatorMessagingCapable": False,
        "ecgCapable": False,
        "lteLiveEventSharingCapable": False,
        "sleepFitFileReceiveCapable": True,
        "secondaryWorkoutStepTargetCapable": False,
        "assistancePlusCapable": False,
        "powerGuidanceCapable": True,
        "airIntegrationCapable": False,
        "healthSnapshotCapable": True,
        "racePredictionsRunCapable": True,
        "vivohubCompatible": False,
        "stepsTrueUpChartCapable": True,
        "sportingEventCapable": True,
        "solarChargeCapable": False,
        "realTimeSettingsCapable": True,
        "emergencyCallingCapable": False,
        "personalRepRecordCapable": False,
        "hrvStatusCapable": True,
        "trainingReadinessCapable": True,
        "publicBetaSoftwareCapable": True,
        "workoutAudioPromptsCapable": False,
        "actualStepRecordingCapable": True,
        "groupTrack2Capable": False,
        "golfAppPairingCapable": False,
        "localWindConditionsCapable": False,
        "multipleGolfCourseCapable": False,
        "beaconTrackingCapable": False,
        "batteryStatusCapable": False,
        "runningPowerZonesCapable": True,
        "acuteTrainingLoadCapable": True,
        "criticalSwimSpeedCapable": False,
        "primaryTrainingCapable": True,
        "dayOfWeekSleepWindowCapable": True,
        "golfCourseDownloadCapable": False,
        "launchMonitorEventSharingCapable": False,
        "lhaBackupCapable": True,
        "jetlagCapable": True,
        "bloodPressureCapable": False,
        "bbiRecordingCapable": False,
        "wheelchairCapable": False,
        "primaryActivityTrackerSettingCapable": True,
        "setBodyCompositionCapable": False,
        "acuteChronicWorkloadRatioCapable": True,
        "sleepNeedCapable": False,
        "wearableBackupRestoreCapable": True,
        "cyclingComputerBackupRestoreCapable": False,
        "descriptiveTrainingEffectCapable": False,
        "sleepSkinTemperatureCapable": False,
        "runningLactateThresholdCapable": False,
        "altitudeAcclimationPercentageCapable": True,
        "hillScoreAndEnduranceScoreCapable": True,
        "swimWorkout2Capable": False,
        "enhancedWorkoutStepCapable": False,
        "primaryTrainingBackupCapable": False,
        "hideSoftwareUpdateVersionCapable": False,
        "adaptiveCoachingScheduleCapable": False,
        "datasource": "C",
        "deviceStatus": "active",
        "registeredDate": 1658531394000,
        "actualProductSku": "010-02539-00",
        "vivohubConfigurable": None,
        "serialNumber": "70H001824",
        "shortName": None,
        "displayName": "fenix 7S",
        "wifiSetup": False,
        "currentFirmwareVersionMajor": 14,
        "currentFirmwareVersionMinor": 36,
        "activeInd": 1,
        "primaryActivityTrackerIndicator": True,
        "unRetirable": False,
        "corporateDevice": False,
        "prePairedWithHRM": False,
        "otherAssociation": False,
        "currentFirmwareVersion": "14.36",
        "isPrimaryUser": False,
    }

    for _ in range(3):
        devices_entry["userProfilePk"] = random.randint(10000000, 99999999)
        devices_entry["unitId"] = random.randint(1000000000, 9999999999)
        devices_entry["deviceId"] = random.randint(1000000000, 9999999999)
        devices_data.append(devices_entry)
    return devices_data


def get_device_last_used_data(start_date, num_days):
    """Generate synthetic data for the last used device.

    This function generates synthetic data for the last used device. It simulates various attributes such as
    userDeviceId, userProfileNumber, applicationNumber, lastUsedDeviceApplicationKey, lastUsedDeviceName,
    lastUsedDeviceUploadTime, imageUrl, and released.

    :return: A dictionary containing synthetic data for the last used device.
    :rtype: Dict
    """
    device_last_used_data = {
        "userDeviceId": random.randint(0, 100),
        "userProfileNumber": random.randint(10000000, 99999999),
        "applicationNumber": random.randint(0, 100),
        "lastUsedDeviceApplicationKey": "default",
        "lastUsedDeviceName": "Default",
        "lastUsedDeviceUploadTime": None,
        "imageUrl": None,
        "released": False,
    }
    return device_last_used_data


def get_device_settings_data(num_devices):
    """Generate synthetic device settings data for the specified number of devices.

    This function generates synthetic device settings data for the specified number of devices. Each device"s settings
    include various configuration options such as time format, units of measurement, activity tracking settings, alarm modes,
    language preferences, and more. The generated data is structured as a list of dictionaries.

    :param num_devices: The number of devices for which to generate settings data.
    :type num_devices: int

    :return: A list of dictionaries containing synthetic device settings data for the specified number of devices.
    :rtype: List[Dict]
    """
    device_settings = []

    # Generate random data for two devices
    for _ in range(num_devices):
        device_data = {
            "deviceId": random.randint(1000000000, 9999999999),
            "timeFormat": random.choice(["time_twelve_hr", "time_twenty_four_hr"]),
            "dateFormat": "date_month_day",
            "measurementUnits": random.choice(["statute_us", "metric"]),
            "allUnits": "statute_us" if random.choice([True, False]) else "metric",
            "visibleScreens": None,
            "enabledScreens": {},
            "screenLists": None,
            "isVivohubEnabled": None,
            "alarms": [],
            "supportedAlarmModes": [
                "ON",
                "OFF",
                "DAILY",
                "WEEKDAYS",
                "WEEKENDS",
                "ONCE",
            ],
            "multipleAlarmEnabled": True,
            "maxAlarm": random.randint(0, 10),
            "activityTracking": {
                "activityTrackingEnabled": True,
                "moveAlertEnabled": True,
                "moveBarEnabled": None,
                "pulseOxSleepTrackingEnabled": random.choice([True, False]),
                "spo2Threshold": None,
                "lowSpo2AlertEnabled": None,
                "highHrAlertEnabled": random.choice([True, False]),
                "highHrAlertThreshold": random.randint(80, 130),
                "pulseOxAcclimationEnabled": random.choice([True, False]),
                "lowHrAlertEnabled": random.choice([True, False]),
                "lowHrAlertThreshold": random.randint(30, 70),
                "bloodEfficiencySleepTrackingEnabled": None,
                "bloodEfficiencyAcclimationEnabled": None,
            },
            "keyTonesEnabled": None,
            "keyVibrationEnabled": None,
            "alertTonesEnabled": None,
            "userNoticeTonesEnabled": None,
            "glonassEnabled": None,
            "turnPromptEnabled": None,
            "segmentPromptEnabled": None,
            "supportedLanguages": [{"id": i, "name": "lang_{i}"} for i in range(40)],
            "language": random.randint(0, 39),
            "supportedAudioPromptDialects": [
                "AR_AE",
                "CS_CZ",
                "DA_DK",
                "DE_DE",
                "EL_GR",
                "EN_AU",
                "EN_GB",
                "EN_US",
                "ES_ES",
                "ES_MX",
                "FI_FI",
                "FR_CA",
                "FR_FR",
                "HE_IL",
                "HR_HR",
                "HU_HU",
                "ID_ID",
                "IT_IT",
                "JA_JP",
                "KO_KR",
                "MS_MY",
                "NL_NL",
                "NO_NO",
                "PL_PL",
                "PT_BR",
                "RO_RO",
                "RU_RU",
                "SK_SK",
                "SV_SE",
                "TH_TH",
                "TR_TR",
                "VI_VI",
                "ZH_CN",
                "ZH_TW",
            ],
            "defaultPage": None,
            "displayOrientation": None,
            "mountingSide": "RIGHT",
            "backlightMode": "AUTO_BRIGHTNESS",
            "backlightSetting": "ON",
            "customWheelSize": None,
            "gestureMode": None,
            "goalAnimation": "NOT_IN_ACTIVITY",
            "autoSyncStepsBeforeSync": 2000,
            "autoSyncMinutesBeforeSync": 240,
            "bandOrientation": None,
            "screenOrientation": None,
            "duringActivity": {
                "screens": None,
                "defaultScreen": None,
                "smartNotificationsStatus": "SHOW_ALL",
                "smartNotificationsSound": None,
                "phoneNotificationPrivacyMode": None,
            },
            "phoneVibrationEnabled": None,
            "connectIQ": {"autoUpdate": True},
            "opticalHeartRateEnabled": True,
            "autoUploadEnabled": True,
            "bleConnectionAlertEnabled": None,
            "phoneNotificationMode": None,
            "lactateThresholdAutoDetectEnabled": None,
            "wiFiAutoUploadEnabled": None,
            "blueToothEnabled": None,
            "smartNotificationsStatus": "SHOW_ALL",
            "smartNotificationsSound": None,
            "dndEnabled": random.choice([True, False]),
            "distanceUnit": None,
            "paceSpeedUnit": None,
            "elevationUnit": None,
            "weightUnit": None,
            "heightUnit": None,
            "temperatureUnit": None,
            "runningFormat": None,
            "cyclingFormat": None,
            "hikingFormat": None,
            "strengthFormat": None,
            "cardioFormat": None,
            "xcSkiFormat": None,
            "otherFormat": None,
            "startOfWeek": "SUNDAY",
            "dataRecording": "SMART",
            "soundVibrationEnabled": None,
            "soundInAppOnlyEnabled": None,
            "backlightKeysAndAlertsEnabled": None,
            "backlightWristTurnEnabled": None,
            "backlightTimeout": "MEDIUM",
            "supportedBacklightTimeouts": None,
            "screenTimeout": None,
            "colorTheme": None,
            "autoActivityDetect": {
                "autoActivityDetectEnabled": True,
                "autoActivityStartEnabled": False,
                "runningEnabled": True,
                "cyclingEnabled": True,
                "swimmingEnabled": True,
                "walkingEnabled": True,
                "ellipticalEnabled": True,
                "drivingEnabled": True,
            },
            "sleep": None,
            "screenMode": None,
            "watchFace": None,
            "watchFaceItemList": None,
            "multipleSupportedWatchFace": {},
            "supportedScreenModes": None,
            "supportedWatchFaces": None,
            "supportedWatchFaceColors": None,
            "autoSyncFrequency": None,
            "supportedBacklightSettings": [
                "AUTO_INTERACTION_ONLY",
                "AUTO_INTERACTION_GESTURE",
                "OFF",
            ],
            "supportedColorThemes": None,
            "disableLastEnabledScreen": None,
            "nickname": None,
            "avatar": None,
            "controlsMenuList": [
                {"id": "POWER_OFF", "index": 0, "required": True},
                {"id": "PAYMENTS", "index": 1, "required": None},
                {"id": "MUSIC_CONTROLS", "index": 2, "required": None},
                {"id": "FIND_MY_PHONE", "index": 3, "required": None},
                {"id": "SAVE_LOCATION", "index": 4, "required": None},
                {"id": "DO_NOT_DISTURB", "index": 5, "required": None},
                {"id": "BLUETOOTH", "index": 6, "required": None},
                {"id": "STOPWATCH", "index": 7, "required": None},
                {"id": "BRIGHTNESS", "index": 8, "required": None},
                {"id": "LOCK_DEVICE", "index": 9, "required": None},
                {"id": "SYNC", "index": None, "required": None},
                {"id": "SET_TIME", "index": None, "required": None},
                {"id": "ALARMS", "index": None, "required": None},
                {"id": "TIMER", "index": None, "required": None},
                {"id": "FLASHLIGHT", "index": None, "required": None},
            ],
            "customUserText": None,
            "metricsFileTrueupEnabled": True,
            "relaxRemindersEnabled": True,
            "smartNotificationTimeout": "MEDIUM",
            "intensityMinutesCalcMethod": "AUTO",
            "moderateIntensityMinutesHrZone": 3,
            "vigorousIntensityMinutesHrZone": 4,
            "keepUserNamePrivate": None,
            "audioPromptLapEnabled": False,
            "audioPromptSpeedPaceEnabled": False,
            "audioPromptSpeedPaceType": "AVERAGE",
            "audioPromptSpeedPaceFrequency": "INVALID",
            "audioPromptSpeedPaceDuration": 180,
            "audioPromptHeartRateEnabled": False,
            "audioPromptHeartRateType": "HEART_RATE",
            "audioPromptHeartRateFrequency": "INVALID",
            "audioPromptHeartRateDuration": 180,
            "audioPromptDialectType": None,
            "audioPromptActivityAlertsEnabled": False,
            "audioPromptPowerEnabled": False,
            "audioPromptPowerType": "AVERAGE",
            "audioPromptPowerFrequency": "INVALID",
            "audioPromptPowerDuration": 180,
            "weightOnlyModeEnabled": None,
            "phoneNotificationPrivacyMode": "OFF",
            "diveAlerts": None,
            "liveEventSharingEnabled": None,
            "liveTrackEnabled": None,
            "liveEventSharingEndTimestamp": None,
            "liveEventSharingMsgContents": None,
            "liveEventSharingTargetDistance": None,
            "liveEventSharingMsgTriggers": None,
            "liveEventSharingTriggerDistance": None,
            "liveEventSharingTriggerTime": None,
            "dbDrivenDefaults": None,
            "schoolMode": None,
            "customMeasurementDate": None,
            "customBodyFatPercent": None,
            "customMuscleMass": None,
            "customDeviceWeight": None,
            "customDeviceBodyFatPercent": None,
            "customDeviceMuscleMass": None,
            "vivohubEnabled": None,
        }

        device_settings.append(device_data)

    return device_settings


def get_device_alarms_data(start_date, num_days):
    """Generate synthetic device alarms data for a specified number of days.

    This function generates synthetic device alarms data for a specified number of days. Device alarms can include
    notifications, alerts, or reminders. The generated data structure is an empty list, and no specific alarm
    information is provided. You can customize this function to generate alarms data as needed.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which device alarms data should be generated.
    :type num_days: int
    :return: An empty list representing device alarms data.
    :rtype: List
    """
    device_alarms_data = []
    return device_alarms_data


def get_active_goals_data(start_date, num_days):
    """Generate synthetic active goals data for a range of days.

    This function generates synthetic active goals data for a specified number of days, starting from the given `start_date`
    and extending for `num_days` days. Active goals can include step goals, distance goals, calorie goals, or active minute goals.
    The generated data is structured as a list of dictionaries.

    :param start_date: The starting date for generating active goals.
    :type start_date: datetime.date

    :param num_days: The number of days for which active goals should be generated.
    :type num_days: int

    :return: A list of dictionaries containing synthetic active goals data for the specified date range.
    :rtype: List[Dict]
    """

    active_goals_data = []
    return active_goals_data


def get_future_goals_data(start_date, num_days):
    """Generate synthetic future goals data for a range of days.

    This function generates synthetic future goals data for a specified number of days, starting from the given `start_date`
    and extending for `num_days` days. Future goals can include step goals, distance goals, calorie goals, or active minute goals.
    The generated data is structured as a list of dictionaries.

    :param start_date: The starting date for generating future goals.
    :type start_date: datetime.date

    :param num_days: The number of days for which future goals should be generated.
    :type num_days: int

    :return: A list of dictionaries containing synthetic future goals data for the specified date range.
    :rtype: List[Dict]
    """

    future_goals_data = []
    return future_goals_data


def get_past_goals_data(start_date, num_days):
    """Generate synthetic past goals data for a range of days.

    This function generates synthetic past goals data for a specified number of days, starting from the given `start_date`
    and extending for `num_days` days. Past goals can include step goals, distance goals, calorie goals, or active minute goals.
    The generated data is structured as a list of dictionaries.

    :param start_date: The starting date for generating past goals.
    :type start_date: datetime.date

    :param num_days: The number of days for which past goals should be generated.
    :type num_days: int

    :return: A list of dictionaries containing synthetic past goals data for the specified date range.
    :rtype: List[Dict]
    """

    past_goals_data = []
    return past_goals_data


def get_weigh_ins_data(start_date, num_days):
    """Generate synthetic weigh-ins data for a specified number of days.

    This function generates synthetic weigh-ins data for a specified number of days. It includes daily weight summaries,
    total average values, and information about the previous and next date's weight. The generated data structure is a
    dictionary with placeholders for various attributes. You can customize this function to provide specific values for
    weigh-ins data.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which weigh-ins data should be generated.
    :type num_days: int
    :return: A dictionary containing synthetic weigh-ins data with placeholder values.
    :rtype: dict
    """
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    from_timestamp = int(start_date_obj.timestamp() * 1000)
    end_date = start_date_obj + timedelta(days=num_days)
    end_timestamp = int(end_date.timestamp() * 1000)

    weigh_ins_data = {
        "dailyWeightSummaries": [],
        "totalAverage": {
            "from": from_timestamp,
            "until": end_timestamp,
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
        },
        "previousDateWeight": {
            "samplePk": 1658540493286,
            "date": from_timestamp,
            "calendarDate": start_date,
            "weight": random.randint(20000, 100000),
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
            "sourceType": "CHANGE_LOG",
            "timestampGMT": None,
            "weightDelta": None,
        },
        "nextDateWeight": {
            "samplePk": None,
            "date": None,
            "calendarDate": None,
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
            "sourceType": None,
            "timestampGMT": None,
            "weightDelta": None,
        },
    }

    return weigh_ins_data


def get_weigh_ins_daily_data(start_date, num_days):
    """Generate synthetic daily weigh-ins data for a specified number of days.

    This function generates synthetic daily weigh-ins data for a specified number of days. Each day includes a start date,
    end date, and a list of date-weight pairs. The generated data structure is a list of dictionaries containing
    weigh-ins information for each day.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which daily weigh-ins data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic daily weigh-ins data for the specified number of days.
    :rtype: List[Dict]
    """
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    weigh_ins_daily_data = []

    for i in range(num_days):
        current_date = start_date_obj + timedelta(days=i)
        current_date_str = current_date.strftime("%Y-%m-%d")
        timestamp = int(current_date.timestamp() * 1000)
        weight = random.randint(50000, 100000)

        weigh_ins_daily_entry = {
            "startDate": current_date_str,
            "endDate": current_date_str,
            "dateWeightList": [
                {
                    "samplePk": random.randint(1000000, 9999999),
                    "date": timestamp,
                    "calendarDate": current_date_str,
                    "weight": weight,
                    "bmi": None,
                    "bodyFat": None,
                    "bodyWater": None,
                    "boneMass": None,
                    "muscleMass": None,
                    "physiqueRating": None,
                    "visceralFat": None,
                    "metabolicAge": None,
                    "sourceType": "CHANGE_LOG",
                    "timestampGMT": timestamp,
                    "weightDelta": None,
                },
            ],
            "totalAverage": {
                "from": timestamp,
                "until": timestamp + 86400000,
                "weight": weight,
                "bmi": None,
                "bodyFat": None,
                "bodyWater": None,
                "boneMass": None,
                "muscleMass": None,
                "physiqueRating": None,
                "visceralFat": None,
                "metabolicAge": None,
            },
        }
        weigh_ins_daily_data.append(weigh_ins_daily_entry)

    return weigh_ins_daily_data


def get_hill_score_data(start_date, end_date):
    """Generate synthetic hill score data for a specified date range.

    This function generates synthetic hill score data for a specified start and end date. The generated data structure
    includes user profile information, the date range, period average score, maximum score, and a list of hill score DTOs.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date in the format "YYYY-MM-DD".
    :type end_date: str
    :return: A dictionary containing synthetic hill score data for the specified date range.
    :rtype: Dict
    """

    hill_score_data = {
        "userProfilePK": random.randint(10000000, 99999999),
        "startDate": start_date,
        "endDate": end_date,
        "periodAvgScore": {},
        "maxScore": None,
        "hillScoreDTOList": [],
    }

    return hill_score_data


def get_endurance_score_data(start_date, end_date):
    """Generate synthetic endurance score data for a specified date range.

    This function generates synthetic endurance score data for a specified start and end date. The generated data structure
    includes user profile information, the date range, average score, maximum score, and a group map with additional data.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date in the format "YYYY-MM-DD".
    :type end_date: str
    :return: A dictionary containing synthetic endurance score data for the specified date range.
    :rtype: Dict
    """
    calendar_date = datetime.strptime(start_date, "%Y-%m-%d")
    random_date1 = calendar_date + timedelta(days=random.randint(0, 7))
    random_date2 = calendar_date + timedelta(days=random.randint(15, 30))
    endurance_score_data = {
        "userProfilePK": random.randint(10000000, 99999999),
        "startDate": start_date,
        "endDate": end_date,
        "avg": None,
        "max": None,
        "groupMap": {
            datetime.strftime(random_date1, "%Y-%m-%d"): {
                "groupAverage": None,
                "groupMax": None,
                "enduranceContributorDTOList": [],
            },
            datetime.strftime(random_date2, "%Y-%m-%d"): {
                "groupAverage": None,
                "groupMax": None,
                "enduranceContributorDTOList": [],
            },
        },
        "enduranceScoreDTO": None,
    }

    return endurance_score_data


def get_adhoc_challenges_data(start_date, num_days):
    """Generate synthetic ad-hoc challenges data for a specified number of days.

    This function generates synthetic ad-hoc challenges data for a specified number of days. The generated data structure
    includes details about the challenges, such as challenge names, participants, and challenge goals.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which ad-hoc challenges data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic ad-hoc challenges data for the specified number of days.
    :rtype: List[Dict]
    """
    adhoc_challenges_data = []
    return adhoc_challenges_data


def get_available_badges_data(start_date, num_days):
    available_badges_data = []

    for i in range(100):
        start_date = datetime.now() + timedelta(days=random.randint(0, 30))
        end_date = start_date + timedelta(days=random.randint(1, 30))

        badge_id = random.randint(1000, 2000)
        badge_uuid = "NA".upper()
        challenge_name = f"Challenge {badge_id}"

        available_badges_entry = {
            "uuid": badge_uuid,
            "badgeChallengeName": challenge_name,
            "challengeCategoryId": random.randint(1, 10),
            "badgeChallengeStatusId": random.randint(1, 3),
            "startDate": start_date.strftime("%Y-%m-%dT00:00:00.0"),
            "endDate": end_date.strftime("%Y-%m-%dT23:59:59.0"),
            "createDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0"),
            "updateDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0"),
            "badgeId": badge_id,
            "badgeKey": f"challenge_key_{badge_id}",
            "badgeUuid": badge_uuid,
            "badgePoints": random.randint(1, 5),
            "badgeUnitId": random.randint(0, 5),
            "badgeProgressValue": None,
            "badgeEarnedDate": None,
            "badgeTargetValue": random.uniform(0.0, 10000.0),
            "badgeTypeIds": [random.randint(1, 10) for _ in range(2)],
            "userJoined": random.choice([True, False]),
            "challengeCategoryImageId": random.randint(1, 5),
            "badgePromotionCodeTypePk": None,
            "badgePromotionCode": None,
            "codeExpirationDate": None,
            "redemptionType": None,
            "partnerName": None,
            "partnerRewardUrl": None,
            "limitedCapacity": random.choice([True, False]),
            "joinDateLocal": None,
            "challengeGroupPk": None,
            "joinable": random.choice([True, False]),
            "approximateValue": None,
            "urlEmbeddedSupported": random.choice([True, False]),
        }

        available_badges_data.append(available_badges_entry)

    return available_badges_data


def get_available_badge_challenges_data(start_date, num_days):
    """Generate synthetic available badges data for a specified number of days.

    This function generates synthetic available badges data for a specified number of days. The generated data includes
    information about various badges, such as challenge names, start and end dates, badge points, and more.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which available badges data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic available badges data for the specified number of days.
    :rtype: List[Dict]
    """

    available_badge_challenges_data = []
    for i in range(100):
        start_date = datetime.now() + timedelta(days=random.randint(0, 60))
        end_date = start_date + timedelta(days=random.randint(1, 30))
        create_date = datetime.now() - timedelta(days=random.randint(1, 30))
        update_date = create_date + timedelta(days=random.randint(1, 5))

        badge_id = random.randint(1000, 2000)
        badge_uuid = "NA".upper()
        challenge_name = f"Challenge {badge_id}"

        available_badge_challenges_entry = {
            "uuid": badge_uuid,
            "badgeChallengeName": challenge_name,
            "challengeCategoryId": random.randint(1, 10),
            "badgeChallengeStatusId": random.randint(1, 3),
            "startDate": start_date.strftime("%Y-%m-%dT00:00:00.0"),
            "endDate": end_date.strftime("%Y-%m-%dT23:59:59.0"),
            "createDate": create_date.strftime("%Y-%m-%dT%H:%M:%S.0"),
            "updateDate": update_date.strftime("%Y-%m-%dT%H:%M:%S.0"),
            "badgeId": badge_id,
            "badgeKey": f"challenge_key_{badge_id}",
            "badgeUuid": badge_uuid,
            "badgePoints": random.randint(1, 5),
            "badgeUnitId": random.randint(0, 10),
            "badgeProgressValue": None,
            "badgeEarnedDate": None,
            "badgeTargetValue": random.uniform(0.0, 10000.0),
            "badgeTypeIds": [random.randint(1, 10) for _ in range(2)],
            "userJoined": random.choice([True, False]),
            "challengeCategoryImageId": random.randint(1, 5),
            "badgePromotionCodeTypePk": None,
            "badgePromotionCode": None,
            "codeExpirationDate": None,
            "redemptionType": None,
            "partnerName": None,
            "partnerRewardUrl": None,
            "limitedCapacity": random.choice([True, False]),
            "joinDateLocal": None,
            "challengeGroupPk": None,
            "joinable": random.choice([True, False]),
            "approximateValue": None,
            "urlEmbeddedSupported": random.choice([True, False]),
        }

        available_badge_challenges_data.append(available_badge_challenges_entry)
    return available_badge_challenges_data


def get_activities_date_data(start_date, num_days):
    """Generate synthetic activities data for a specified number of days.

    This function generates synthetic activities data for a specified number of days, each containing information about
    random activities with attributes such as activity name, start time, type, distance, duration, elevation gain, and
    average speed.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which activities data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic activities data for the specified number of days.
    :rtype: List[Dict]
    """
    activities_date_data = []
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(100):
        activity_date = start_date_obj + timedelta(days=i)
        start_time_local = activity_date + timedelta(
            hours=random.randint(0, 23), minutes=random.randint(0, 59)
        )
        # Simulating a time zone difference
        start_time_gmt = start_time_local + timedelta(hours=random.randint(-12, 12))

        # Random duration between 30 minutes and 3 hours
        duration = random.randint(1800, 10800)
        distance = random.uniform(0.0, 20.0)  # Distance in km
        elevation_gain = random.uniform(0.0, 500.0)  # Elevation gain in meters
        elevation_loss = random.uniform(0.0, 500.0)  # Elevation loss in meters
        average_speed = distance / (duration / 3600)  # Average speed in km/h

        activities_date_entry = {
            "activityId": random.randint(100000000, 999999999),
            "activityName": "Random Activity",
            "description": None,
            "startTimeLocal": start_time_local.strftime("%Y-%m-%d %H:%M:%S"),
            "startTimeGMT": start_time_gmt.strftime("%Y-%m-%d %H:%M:%S"),
            "activityType": {
                "typeId": random.randint(1, 20),
                "typeKey": "random_activity_type",
                "parentTypeId": random.randint(1, 20),
                "isHidden": False,
                "restricted": False,
                "trimmable": random.choice([True, False]),
            },
            "distance": distance,
            "duration": duration,
            "elevationGain": elevation_gain,
            "elevationLoss": elevation_loss,
            "averageSpeed": average_speed,
        }

        activities_date_data.append(activities_date_entry)
    return activities_date_data


def get_activities_fordate_aggregated_data(start_date, num_days):
    """Generate synthetic aggregated activities data for a specified number of days.

    This function generates synthetic aggregated activities data for a specified number of days. It includes information
    about heart rate values recorded at 15-minute intervals, sleep times, and other metadata for each day.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which aggregated activities data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic aggregated activities data for the specified number of days.
    :rtype: List[Dict]
    """
    activities_fordate_aggregated_data = []
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

    for i in range(num_days):
        current_date = start_date_obj + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")

        # Randomizing heart rate values for the day
        heart_rate_values = []
        for j in range(24 * 4):  # Assuming heart rate recorded every 15 minutes
            timestamp = int(
                (current_date + timedelta(minutes=15 * j)).timestamp() * 1000
            )
            heart_rate = random.randint(60, 100)
            heart_rate_values.append([timestamp, heart_rate])

        activities_fordate_aggregated_entry = {
            "ActivitiesForDay": {
                "requestUrl": "NA",
                "statusCode": 200,
                "headers": {},
                "errorMessage": None,
                "payload": [],
                "successful": True,
            },
            "AllDayHR": {
                "requestUrl": "NA",
                "statusCode": 200,
                "headers": {},
                "errorMessage": None,
                "payload": {
                    "userProfilePK": random.randint(10000000, 99999999),
                    "calendarDate": date_str,
                    "startTimestampGMT": f"{date_str}T07:00:00.0",
                    "endTimestampGMT": f"{date_str}T07:00:00.0",
                    "startTimestampLocal": f"{date_str}T00:00:00.0",
                    "endTimestampLocal": f"{date_str}T00:00:00.0",
                    "maxHeartRate": random.randint(100, 150),
                    "minHeartRate": random.randint(50, 70),
                    "restingHeartRate": random.randint(60, 80),
                    "lastSevenDaysAvgRestingHeartRate": random.randint(60, 80),
                    "heartRateValueDescriptors": [
                        {"key": "timestamp", "index": 0},
                        {"key": "heartrate", "index": 1},
                    ],
                    "heartRateValues": heart_rate_values,
                },
                "successful": True,
            },
            "SleepTimes": {
                "currentDaySleepEndTimeGMT": int(
                    (current_date + timedelta(hours=8)).timestamp() * 1000
                ),
                "currentDaySleepStartTimeGMT": int(current_date.timestamp() * 1000),
                "nextDaySleepEndTimeGMT": int(
                    (current_date + timedelta(days=1, hours=8)).timestamp() * 1000
                ),
                "nextDaySleepStartTimeGMT": int(
                    (current_date + timedelta(days=1)).timestamp() * 1000
                ),
            },
        }

        activities_fordate_aggregated_data.append(activities_fordate_aggregated_entry)

    return activities_fordate_aggregated_data


def get_badge_challenges_data(start_date, num_days):
    """Generate synthetic badge challenges data for a specified number of days.

    This function generates synthetic badge challenges data for a specified number of days. It can be used to simulate
    badge challenges and their details.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which badge challenges data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic badge challenges data for the specified number of days.
    :rtype: List[Dict]
    """
    badge_challenges_data = []
    return badge_challenges_data


def get_non_completed_badge_challenges_data(start_date, num_days):
    """Generate synthetic non-completed badge challenges data for a specified number of days.

    This function generates synthetic data for non-completed badge challenges for a specified number of days.
    It can be used to simulate badge challenges that have not been completed by users.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which non-completed badge challenges data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic non-completed badge challenges data for the specified number of days.
    :rtype: List[Dict]
    """
    non_completed_badge_challenges_data = []
    return non_completed_badge_challenges_data


def get_race_prediction_data(start_date, num_days):
    """Generate synthetic race prediction data for a specified number of days.

    This function generates synthetic data for race predictions for a specified number of days.
    It can be used to simulate race prediction information for users.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which race prediction data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic race prediction data for the specified number of days.
    :rtype: List[Dict]
    """
    race_prediction_data = []
    return race_prediction_data


def get_inprogress_virtual_challenges_data(start_date, num_days):
    """Generate synthetic data for in-progress virtual challenges.

    This function generates synthetic data for virtual challenges that are in progress
    for a specified number of days. It can be used to simulate virtual challenge information
    for users.

    :param start_date: The start date in the format "YYYY-MM-DD".
    :type start_date: str
    :param num_days: The number of days for which in-progress virtual challenge data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing synthetic in-progress virtual challenge data
             for the specified number of days.
    :rtype: List[Dict]
    """
    inprogress_virtual_challenges_data = []
    return inprogress_virtual_challenges_data


def create_syn_data(start_date, end_date):
    """
    Returns a dictionary of synthetic health and activity data for a specified date range.
    :param start_date: the start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: A dictionary containing synthetic data for various health and activity metrics, each
        element is a list or dictionary representing data for a specific day.
    :rtype: Dict
    """

    num_days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days

    synth_data = {
        "dates": [
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            for i in range(num_days)
        ],
        "hrv": get_hrv_data(start_date, num_days),
        "steps": get_steps_data(start_date, num_days),
        "daily_steps": get_daily_steps_data(start_date, num_days),
        "stats": get_stats_data(start_date, num_days),
        "body_composition": get_body_composition_data(start_date, num_days),
        "body_composition_aggregated": get_body_composition_aggregated_data(
            start_date, num_days
        ),
        "stats_and_body_aggregated": get_stats_and_body_aggregated_data(
            start_date, num_days
        ),
        "hr": None,
        "body_battery": get_body_battery_data(start_date, num_days),
        "training_readiness": get_training_readiness_data(start_date, num_days),
        "blood_pressure": get_blood_pressure_data(start_date, end_date, 100),
        "floors": get_floors_data(start_date, num_days),
        "training_status": get_training_status_data(start_date, num_days),
        "rhr": get_resting_hr_data(start_date, num_days),
        "hydration": get_hydration_data(start_date, num_days),
        "sleep": get_sleep_data(start_date, num_days),
        "earned_badges": get_earned_badges_data(start_date, num_days),
        "stress": get_stress_data(start_date, num_days),
        "day_stress_aggregated": get_day_stress_aggregated_data(start_date, num_days),
        "respiration": get_respiration_data(start_date, num_days),
        "spo2": get_spo2_data(start_date, num_days),
        "max_metrics": get_metrics_data(start_date, num_days),
        "personal_record": get_personal_record_data(start_date, end_date, num_days),
        "activities": get_activities_data(start_date, num_days),
        "activities_date": get_activities_date_data(start_date, num_days),
        "activities_fordate_aggregated": get_activities_fordate_aggregated_data(
            start_date, num_days
        ),
        "devices": get_devices_data(start_date, num_days),
        "device_last_used": get_device_last_used_data(start_date, num_days),
        "device_settings": get_device_settings_data(3),
        "device_alarms": get_device_alarms_data(start_date, num_days),
        "active_goals": get_active_goals_data(start_date, num_days),
        "future_goals": get_future_goals_data(start_date, num_days),
        "past_goals": get_past_goals_data(start_date, num_days),
        "weigh_ins": get_weigh_ins_data(start_date, num_days),
        "weigh_ins_daily": get_weigh_ins_daily_data(start_date, num_days),
        "hill_score": get_hill_score_data(
            start_date,
            end_date,
        ),
        "endurance_score": get_endurance_score_data(
            start_date,
            end_date,
        ),
        "adhoc_challenges": get_adhoc_challenges_data(start_date, num_days),
        "available_badges": get_available_badges_data(start_date, num_days),
        "available_badge_challenges": get_available_badge_challenges_data(
            start_date, num_days
        ),
        "badge_challenges": get_badge_challenges_data(start_date, num_days),
        "non_completed_badge_challenges": get_non_completed_badge_challenges_data(
            start_date, num_days
        ),
        "race_prediction": get_race_prediction_data(start_date, num_days),
        "inprogress_virtual_challenges": get_inprogress_virtual_challenges_data(
            start_date, num_days
        ),
    }

    synth_data["hr"] = get_heart_rate_data(start_date, num_days, synth_data["steps"])

    return synth_data
