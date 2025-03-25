import random
from datetime import datetime, timedelta

import numpy as np


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
            steps = int(np.random.normal(90, 30))
            steps_entry = {
                "startGMT": interval_start.strftime("%Y-%m-%dT%H:%M:%S.0"),
                "endGMT": interval_end.strftime("%Y-%m-%dT%H:%M:%S.0"),
                "steps": max(steps, 0),
                "pushes": 0,
                "primaryActivityLevel": random.choice(
                    ["active", "sedentary", "sleeping", "none"]
                ),
                "activityLevelConstant": random.choice([True, False]),
            }
            steps_day.append(steps_entry)
        steps_data.append(steps_day)

    return steps_data


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
            heart_rate = int(step_val_avg * 0.5 + 75 + np.random.randn() * 10)
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
