import collections
import random
import secrets
import string
from datetime import datetime, timedelta
from random import choice, randrange

import numpy as np

__all__ = ["create_syn_data"]


def get_steps(date):
    """Returns a an array of steps data

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :rtype: dictionary
    """
    date = datetime.strptime(date, "%Y-%m-%d")

    def generate_step_line():
        num_segments = random.randint(5, 20)

        step_segments = []
        for _ in range(num_segments):
            x = random.randint(0, 100)
            y = random.randint(0, 1000)
            step_segments.append(f"[{x},{y}]")

        step_line = f"[[15],[{','.join(step_segments)}]]"
        return step_line

    data = {
        "apiCode": "BB640AE4",
        "data": {
            "firstHappenDay": int(date.timestamp()),
            "firstSleepAlgoVersionStartTime": int(date.timestamp()) + 7 * 24 * 60 * 60,
            "maxSleepAlgoVersion": 1,
            "statisticData": {
                "dayDataList": [
                    {
                        "happenDay": int(date.timestamp()),
                        "performance": -1,
                        "step": random.randint(5000, 20000),
                        "stepLine": generate_step_line(),
                    }
                ]
            },
        },
        "message": "OK",
        "result": "0000",
    }

    return data


def get_exercise(date_str):
    """Returns a an array of exercise data

    :param date_str: the date as a string in the format "YYYY-MM-DD"
    :type date_str: str
    :rtype: dictionary
    """

    def generate_motion_time_line(motion_time):
        motion_time_line = f"[[15],[[63,{motion_time}]]]"
        return motion_time_line

    date = datetime.strptime(date_str, "%Y-%m-%d")

    data = {
        "apiCode": "BB640AE4",
        "data": {
            "firstHappenDay": int(date.timestamp()),
            "firstSleepAlgoVersionStartTime": int(date.timestamp()) + 7 * 24 * 60 * 60,
            "maxSleepAlgoVersion": 1,
            "statisticData": {
                "dayDataList": [
                    {
                        "happenDay": int(date.timestamp()),
                        "motionTime": random.randint(0, 120),
                        "motionTimeLine": generate_motion_time_line(
                            random.randint(0, 120)
                        ),
                        "performance": -1,
                    }
                ]
            },
        },
        "message": "OK",
        "result": "0000",
    }

    return data


def get_heart_rate(date_str):
    """Returns a an array of heart rate data

    :param date_str: the date as a string in the format "YYYY-MM-DD"
    :type date_str: str
    :rtype: dictionary
    """

    def generate_heart_rate_line():
        heart_rate_segments = []

        for hour in range(24):
            avg_hr = random.randint(40, 120)
            max_hr = avg_hr + random.randint(0, 20)
            min_hr = avg_hr - random.randint(0, 20)
            test_rhr = random.randint(40, 100)
            heart_rate_segments.append(
                f"[{hour},{avg_hr},{max_hr},{min_hr},{test_rhr}]"
            )

        heart_rate_line = f"[[15],[{','.join(heart_rate_segments)}]]"
        return heart_rate_line

    date = datetime.strptime(date_str, "%Y-%m-%d")

    data = {
        "apiCode": "BB640AE4",
        "data": {
            "firstHappenDay": int(date.timestamp()),
            "firstSleepAlgoVersionStartTime": int(date.timestamp()) + 7 * 24 * 60 * 60,
            "maxSleepAlgoVersion": 1,
            "statisticData": {
                "dayDataList": [
                    {
                        "happenDay": int(date.timestamp()),
                        "heartRateData": {
                            "avgHeartRate": random.randint(50, 90),
                            "maxHeartRate": random.randint(90, 140),
                            "minHeartRate": random.randint(40, 70),
                            "testRhr": random.randint(50, 90),
                            "testRhrTimestamp": int(date.timestamp())
                            + random.randint(0, 24) * 3600,
                            "testRhrTimestampzone": 8,
                        },
                        "heartRateLine": generate_heart_rate_line(),
                        "performance": -1,
                    }
                ]
            },
        },
        "message": "OK",
        "result": "0000",
    }

    return data


def get_sports(date_str):
    """Returns a an array of sports data

    :param date_str: the date as a string in the format "YYYY-MM-DD"
    :type date_str: str
    :rtype: dictionary
    """

    data = {"sports": {"apiCode": "B7D57DB7", "data": []}}

    date = datetime.strptime(date_str, "%Y-%m-%d")

    # (1,5) represents a random number of sport sessions
    for _ in range(random.randint(1, 5)):
        sport_entry = {
            "ascentDuration": random.randint(0, 600),
            "avgCadence": random.randint(0, 200),
            "avgHeartRate": random.randint(80, 180),
            "avgPace": random.randint(300, 600),
            "avgSpeed": random.randint(100, 5000) / 10,
            "calorie": random.randint(10000, 150000),
            "count": random.randint(0, 10),
            "createTimestamp": int(datetime.timestamp(datetime.now())),
            "deviceId": "COROS PACE 2 8FCE88",
            "distance": round(random.uniform(1, 50), 2),
            "duration": random.randint(1, 200),
            "endTime": int(date.timestamp()) + random.randint(3600, 86400),
            "fitCreateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "happenDate": int(date.strftime("%Y%m%d")),
            "happenDay": int(date.strftime("%Y%m%d")),
            "imageUrl": "https://example.com/image.jpg",
            "imageUrlType": 1,
            "isShowMs": random.randint(0, 1),
            "labelId": f"Label_{random.randint(100000, 999999)}",
            "laps": random.randint(0, 5),
            "max2s": random.randint(0, 10),
            "maxSpeed": random.randint(1000, 5000) / 10,
            "mode": random.randint(1, 10),
            "modifyTime": int(datetime.timestamp(datetime.now())),
            "name": f"Activity_{random.randint(1, 100)}",
            "pitch": random.randint(-10, 10),
            "rdType": random.randint(0, 1),
            "recalculateRecord": bool(random.getrandbits(1)),
            "sets": random.randint(0, 3),
            "speedType": random.randint(1, 3),
            "speedValue": random.randint(300, 6000) / 10,
            "startTime": int(date.timestamp()) + random.randint(0, 3600),
            "state": random.randint(0, 1),
            "step": random.randint(0, 10000),
            "subMode": random.randint(0, 2),
            "subSport": bool(random.getrandbits(1)),
            "taskStatus": random.randint(0, 1),
            "total": random.randint(0, 10),
            "totalAvgHr": random.randint(80, 160),
            "totalAvgSpeed": random.randint(0, 5000) / 10,
            "totalDecline": random.randint(0, 50),
            "totalDeclineDouble": random.uniform(0, 10),
            "totalElevation": random.randint(0, 100),
            "totalElevationDouble": random.uniform(0, 10),
            "unit": 2,
            "unitType": 2,
            "uploadedImageData": 0,
            "userId": random.randint(100000000000000000, 999999999999999999),
            "uuid": f"{random.randint(10000000, 99999999)}000001379100c8168fce88",
            "weatherLocationKey": f"{random.randint(100000, 999999)}",
            "weatherTime": int(date.timestamp()) - random.randint(0, 86400),
        }

        data["sports"]["data"].append(sport_entry)

    return data["sports"]


def get_sleep(date):
    """Returns a an array of active sleep data

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :rtype: dictionary
    """

    def generate_random_string(length):
        # Generate a random string of the specified length
        alphabet = string.ascii_letters + string.digits + "+/"
        return "".join(secrets.choice(alphabet) for _ in range(length))

    date = datetime.strptime(date, "%Y-%m-%d")
    sleep_list = generate_random_string(300)  # Adjust the length as needed

    data = {
        "apiCode": "BB640AE4",
        "data": {
            "firstHappenDay": date,
            "firstSleepAlgoVersionStartTime": 1662759720,
            "maxSleepAlgoVersion": 1,
            "statisticData": {
                "dayDataList": [
                    {
                        "happenDay": date,
                        "performance": -1,
                        # creating random numbers based on average sleep cycle lengths in humans
                        "sleepData": {
                            "avgHeartRate": random.randint(50, 70),
                            "deepTime": random.randint(40, 70),
                            "eyeTime": random.randint(100, 120),
                            "lightTime": random.randint(200, 230),
                            "maxHeartRate": random.randint(60, 80),
                            "minHeartRate": random.randint(45, 55),
                            "totalSleepTime": random.randint(350, 600),
                            "wakeTime": random.randint(8, 12),
                        },
                        # a unique identifier for the sleep session
                        "sleepList": [sleep_list],
                    }
                ]
            },
        },
        "message": "OK",
        "result": "0000",
    }

    return data


def get_active_energy(date):
    """Returns a an array of active energy data

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :rtype: dictionary
    """

    date = datetime.strptime(date, "%Y-%m-%d")
    data = {
        "apiCode": "BB640AE4",
        "data": {
            "firstHappenDay": date,
            "firstSleepAlgoVersionStartTime": 1662759720,
            "maxSleepAlgoVersion": 1,
            "statisticData": {
                "dayDataList": [
                    {
                        "calorie": random.randint(1000, 3000),
                        "calorieLine": f"[[15],[[{''.join([f'{i},{random.randint(100, 20000)}' for i in range(15, 95)])}]]",
                        "happenDay": date,
                        "performance": -1,
                    }
                ]
            },
        },
        "message": "OK",
        "result": "0000",
    }

    return data


def create_syn_data(start_date, end_date):
    """Returns a defaultdict of "steps", "exercise_time", "heart_rate", "sports", "sleep", "active_energy"

    :param start_date: the start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: a defaultdict of heart_rate data, activity data, "steps", "exercise_time", "heart_rate", "sports", "sleep", "active_energy"
    :rtype: defaultdict
    """

    num_days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days

    # first get the dates as datetime objects
    synth_dates = [
        datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        for i in range(num_days)
    ]

    for i, date in enumerate(synth_dates):
        synth_dates[i] = date.strftime("%Y-%m-%d")

    full_dict = collections.defaultdict(list)

    for date in synth_dates:

        full_dict["sleep"].append(get_sleep(date))
        full_dict["steps"].append(get_steps(date))
        full_dict["exercise_time"].append(get_exercise(date))
        full_dict["heart_rate"].append(get_heart_rate(date))
        full_dict["sports"].append(get_sports(date))
        full_dict["active_energy"].append(get_active_energy(date))

    return full_dict
