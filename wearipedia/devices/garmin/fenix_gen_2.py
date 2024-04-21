import random
from datetime import datetime, timedelta

import numpy as np


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
