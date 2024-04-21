import random
from datetime import datetime, timedelta


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
