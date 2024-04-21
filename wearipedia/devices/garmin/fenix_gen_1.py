import random
from datetime import datetime, timedelta


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
