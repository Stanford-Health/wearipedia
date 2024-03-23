import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm


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
