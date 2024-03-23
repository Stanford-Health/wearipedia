import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm


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
