import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm


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
