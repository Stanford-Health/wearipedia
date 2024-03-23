import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm

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
