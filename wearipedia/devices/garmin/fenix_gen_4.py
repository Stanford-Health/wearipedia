import random
from datetime import datetime, timedelta


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
