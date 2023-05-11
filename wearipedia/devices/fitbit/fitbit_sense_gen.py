import collections
from datetime import datetime, time, timedelta

import numpy as np
from random import choice, choices, randrange


__all__ = ["create_syn_data"]


################
# some helpers #
################


def get_sleep(date):
    """Generate sleep data for a given date.

    :return: sleep data dictionary
    :rtype: dictionary
    """

    duration = np.random.randint(14400, 36000)

    awake = np.random.randint(2, 9)
    afterwake = np.random.randint(0, 200) / 100
    tofall = np.random.randint(0, 200) / 100

    percents = (100 - awake - afterwake - tofall, awake, afterwake, tofall)
    start = datetime.strptime(date + " 9:00 PM", "%Y-%m-%d %I:%M %p")
    end = datetime.strptime(date + " 11:58 PM", "%Y-%m-%d %I:%M %p")

    # generate random date
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)

    start_time = start + timedelta(seconds=random_second)
    end_time = start_time + timedelta(seconds=duration)

    sleep_dict = {
        "dateOfSleep": "2022-08-27",
        "duration": duration * 1000,
        "efficiency": np.random.randint(90, 99),
        "endTime": str(end_time.isoformat()),
        "infoCode": 0,
        "isMainSleep": True,
        "logId": np.random.randint(0, 1000000000),
        "logType": "auto_detected",
        "minutesAfterWakeup": round(duration / 60 * percents[2] / 100),
        "minutesAsleep": round(duration / 60 * percents[0] / 100),
        "minutesAwake": round(duration / 60 * percents[1] / 100),
        "minutesToFallAsleep": round(duration / 60 * percents[3] / 100),
        "startTime": str(start_time.isoformat()),
        "timeInBed": round(duration / 60),
        "levels": dict(),
        "type": "stages",
    }
    sleep_dict["levels"]["data"] = []
    sleep_dict["levels"]["shortData"] = []
    sleep_dict["levels"]["summary"] = {
        "deep": {"count": 0, "minutes": 0},
        "light": {"count": 0, "minutes": 0},
        "rem": {"count": 0, "minutes": 0},
        "wake": {"count": 2, "minutes": round(duration / 60 * percents[1] / 100)},
    }
    #  core sleep levels
    sleep_dict["levels"]["data"].append(
        {
            "dateTime": str(start_time.isoformat()),
            "level": "wake",
            "seconds": round(duration / 60 * percents[3] / 100) * 60,
        }
    )
    # split sleep times
    def split_the_duration(duration):
        saver_of_duration = duration
        while duration > 1:
            n = np.random.randint(1, round(saver_of_duration / 12))
            if duration - n >= 0:
                yield n
            else:
                yield duration
            duration -= n

    generator = split_the_duration(round(duration * percents[0] / 100))

    arr_of_durations = list(generator)

    start_phases = start_time + timedelta(
        seconds=round(duration / 60 * percents[3] / 100) * 60
    )

    # add phases
    for i, item in enumerate(arr_of_durations):
        if i != 0:
            start_phases += timedelta(seconds=arr_of_durations[i - 1])

        type = choice(["deep", "rem", "light"])

        sleep_dict["levels"]["summary"][type]["count"] += 1
        sleep_dict["levels"]["summary"][type]["minutes"] += round(item / 60)

        sleep_dict["levels"]["data"].append(
            {"dateTime": str(start_phases.isoformat()), "level": type, "seconds": item}
        )

    start_phases += timedelta(seconds=arr_of_durations[-1])
    sleep_dict["levels"]["data"].append(
        {
            "dateTime": str(start_phases.isoformat()),
            "level": "wake",
            "seconds": round(duration / 60 * percents[2] / 100) * 60,
        }
    )

    # do the same for wakeups
    generator = split_the_duration(round(duration * percents[0] / 100))
    arr_of_durations = list(generator)

    for i, item in enumerate(arr_of_durations):
        if i != 0:
            start_phases += timedelta(seconds=arr_of_durations[i - 1])
            sleep_dict["levels"]["summary"]["wake"]["count"] += 1
        # generate random date
        delta = end_time - start_time
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        randtime = start_time + timedelta(seconds=random_second)
        start_time = start_time + timedelta(seconds=arr_of_durations[i - 1])

        sleep_dict["levels"]["shortData"].append(
            {"dateTime": str(randtime.isoformat()), "level": "wake", "seconds": item}
        )

    return sleep_dict


def get_activity(date):
    """Generate activity data for a given date.

    :return: dictionaries of "steps", "minutesVeryActive", "minutesFairlyActive", "minutesLightlyActive", "distance", "minutesSedentary"
    :rtype: dictionary
    """

    very_active = np.random.randint(0, 240)
    fairly_active = np.random.randint(0, 240)
    lightly_active = np.random.randint(0, 240)

    steps = {
        "dateTime": date,
        "value": very_active * 50 + fairly_active * 25 + lightly_active * 10,
    }
    minutesVeryActive = {"dateTime": date, "value": very_active}
    minutesFairlyActive = {"dateTime": date, "value": fairly_active}
    minutesLightlyActive = {"dateTime": date, "value": lightly_active}
    distance = {
        "dateTime": date,
        "value": (very_active * 50 + fairly_active * 25 + lightly_active * 10) / 1326,
    }
    minutesSedentary = {
        "dateTime": date,
        "value": 1440 - very_active + fairly_active + lightly_active,
    }

    return (
        steps,
        minutesVeryActive,
        minutesFairlyActive,
        minutesLightlyActive,
        distance,
        minutesSedentary,
    )


def get_heart_rate(date):
    """Generate heart rate data for a given date.

    :return: dictionary of heart rate values and details
    :rtype: dictionary
    """

    heart_rate_data = {
        "heart_rate_day": [
            {
                "activities-heart": [
                    {
                        "dateTime": date,
                        "value": {
                            "customHeartRateZones": [],
                            "heartRateZones": [
                                {
                                    "caloriesOut": 2877.06579,
                                    "max": 110,
                                    "min": 30,
                                    "minutes": 0,
                                    "name": "Out of Range",
                                },
                                {
                                    "caloriesOut": 0,
                                    "max": 136,
                                    "min": 110,
                                    "minutes": 0,
                                    "name": "Fat Burn",
                                },
                                {
                                    "caloriesOut": 0,
                                    "max": 169,
                                    "min": 136,
                                    "minutes": 0,
                                    "name": "Cardio",
                                },
                                {
                                    "caloriesOut": 0,
                                    "max": 220,
                                    "min": 169,
                                    "minutes": 0,
                                    "name": "Peak",
                                },
                            ],
                            "restingHeartRate": 58,
                        },
                    }
                ],
                "activities-heart-intraday": {
                    "dataset": [],
                    "datasetInterval": 1,
                    "datasetType": "minute",
                },
            }
        ]
    }

    the_time = time(hour=0, minute=0, second=0)
    for i in range(1440):

        max_heart_rate = [110, 136, 169, 220]
        min_dict = {110: 30, 136: 110, 169: 136, 220: 169}
        weights = [0.14, 0.0058, 0.0008, 0.0001]
        max_heart = choices(max_heart_rate, weights)

        inx = max_heart_rate.index(max_heart[0])
        heart_rate_data["heart_rate_day"][0]["activities-heart"][0]["value"][
            "heartRateZones"
        ][inx]["minutes"] += 1
        heart_rate_data["heart_rate_day"][0]["activities-heart"][0]["value"][
            "heartRateZones"
        ][inx]["caloriesOut"] += 2 * (inx + 0.5)

        val = np.random.randint(min_dict[max_heart[0]], max_heart)

        heart_rate_data["heart_rate_day"][0]["activities-heart-intraday"][
            "dataset"
        ].append({"time": the_time.strftime("%H:%M:%S"), "value": val})

        newtime = (
            datetime.combine(datetime.today(), the_time) + timedelta(seconds=60)
        ).time()
        the_time = newtime

    return heart_rate_data


def get_hrv(date):
    """Generate hrv for a given date.

    :return: dictionary of hrv details
    :rtype: dictionary
    """
    hrv = {
        "hrv": [
            {
                "hrv": [
                    {
                        "value": {
                            "dailyRmssd": np.random.randint(13, 48),
                            "deepRmssd": np.random.randint(13, 48),
                        },
                        "dateTime": date,
                    }
                ]
            }
        ]
    }

    return hrv


def get_distance_day(date):
    """Generate distance data for a given date.

    :return: dictionary of distance data details
    :rtype: dictionary
    """

    distance_day = {
        "distance_day": [
            {
                "activities-distance": [{"dateTime": date, "value": 0}],
                "activities-distance-intraday": {
                    "dataset": [],
                    "datasetInterval": 1,
                    "datasetType": "minute",
                },
            }
        ]
    }

    the_time = time(hour=0, minute=0, second=0)

    for i in range(1440):

        distance = [0, 0.1]
        weights = [0.6, 0.3]
        max_distance = choices(distance, weights)
        if max_distance[0] == 0:
            val = 0
        else:
            val = np.random.randint(1, 1000) / 10000

        distance_day["distance_day"][0]["activities-distance-intraday"][
            "dataset"
        ].append({"time": the_time.strftime("%H:%M:%S"), "value": val})
        newtime = (
            datetime.combine(datetime.today(), the_time) + timedelta(seconds=60)
        ).time()
        the_time = newtime

    return distance_day


def create_syn_data(start_date, end_date):
    """Returns a defaultdict of heart_rate data, activity data, "sleep", "steps","minutesVeryActive", "minutesLightlyActive", "minutesFairlyActive", "distance", "minutesSedentary", "heart_rate_day", "hrv", "distance_day"

    :param start_date: the start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: a defaultdict of heart_rate data, activity data, "sleep", "steps","minutesVeryActive", "minutesLightlyActive", "minutesFairlyActive", "distance", "minutesSedentary", "heart_rate_day", "hrv", "distance_day"
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

        activity = get_activity(date)

        full_dict["sleep"].append(get_sleep(date))
        full_dict["steps"].append(activity[0])
        full_dict["minutesVeryActive"].append(activity[1])
        full_dict["minutesFairlyActive"].append(activity[2])
        full_dict["minutesLightlyActive"].append(activity[3])
        full_dict["distance"].append(activity[4])
        full_dict["minutesSedentary"].append(activity[5])
        full_dict["heart_rate"].append(get_heart_rate(date))
        full_dict["hrv"].append(get_hrv(date))
        full_dict["distance_day"].append(get_distance_day(date))

    return full_dict
