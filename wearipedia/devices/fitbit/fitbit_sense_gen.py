import collections
import random
from datetime import datetime, timedelta
from random import choice, randrange

import numpy as np

__all__ = ["create_syn_data"]

sleep_stages = {
    "deepSleepSummary": {"mean": 12, "std": 1.5},
    "remSleepSummary": {"mean": 16, "std": 1.5},
    "lightSleepSummary": {"mean": 18, "std": 2},
}


def get_sleep(date):
    """Generate sleep data for a given date.


    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: sleep data dictionary
    :rtype: dictionary
    """

    duration = random.randint(14400, 36000)

    awake = random.randint(2, 9)
    afterwake = random.randint(0, 200) / 100
    tofall = random.randint(0, 200) / 100

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
        "dateOfSleep": date,
        "duration": duration * 1000,
        "efficiency": random.randint(90, 99),
        "endTime": str(end_time.isoformat()),
        "infoCode": 0,
        "isMainSleep": True,
        "logId": random.randint(0, 1000000000),
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
            n = random.randint(1, round(saver_of_duration / 12))
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

        type = choice(["deep", "rem", "light"])

        sleep_dict["levels"]["summary"][type]["count"] += 1
        sleep_dict["levels"]["summary"][type]["minutes"] += round(item / 60)

        sleep_dict["levels"]["data"].append(
            {"dateTime": str(start_phases.isoformat()), "level": type, "seconds": item}
        )

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

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: dictionaries of "steps", "minutesVeryActive", "minutesFairlyActive", "minutesLightlyActive", "distance", "minutesSedentary"
    :rtype: dictionary
    """

    very_active = random.randint(0, 240)
    fairly_active = random.randint(0, 240)
    lightly_active = random.randint(0, 240)

    minutes_in_a_day = 1440

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
        "value": minutes_in_a_day - (very_active + fairly_active + lightly_active),
    }

    return (
        steps,
        minutesVeryActive,
        minutesFairlyActive,
        minutesLightlyActive,
        distance,
        minutesSedentary,
    )


def get_heart_rate(date, intraday=False):
    """Generate heart rate data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :param intraday: whether the heart rate is reported per second
    :type intraday: bool
    :return: dictionary of heart rate values and details
    :rtype: dictionary
    """

    HR_MEAN = 75
    HR_STD = 15
    HR_MIN = 50
    HR_MAX = 195
    ZONE_CALORIES = [0, 1, 2, 3]

    heart_rate_zones = [
        {
            "caloriesOut": 2877.06579,
            "max": 110,
            "min": 30,
            "minutes": 0,
            "name": "Out of Range",
        },
        {"caloriesOut": 1000, "max": 136, "min": 110, "minutes": 0, "name": "Fat Burn"},
        {"caloriesOut": 1000, "max": 169, "min": 136, "minutes": 0, "name": "Cardio"},
        {"caloriesOut": 1000, "max": 220, "min": 169, "minutes": 0, "name": "Peak"},
    ]

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
    iterations_in_a_day = 1440 if not intraday else 1440 * 60

    bpm_start = np.clip(np.random.normal(HR_MEAN, HR_STD), HR_MIN, HR_MAX)
    time_intervals = np.arange(iterations_in_a_day)

    random_walk = np.random.randint(-1, 2, size=iterations_in_a_day)
    heart_rate_values = np.clip(np.cumsum(random_walk) + bpm_start, HR_MIN, HR_MAX)

    hours = (time_intervals // 60) % 24

    zone_indices = np.where(
        hours < 6, 0, np.where(hours < 10, 1, np.where(hours < 18, 2, 3))
    )

    zone_minutes = np.bincount(zone_indices, minlength=4)
    zone_calories = np.array([ZONE_CALORIES[i] * zone_minutes[i] for i in range(4)])

    for i, zone in enumerate(heart_rate_zones):
        zone["minutes"] += zone_minutes[i]
        zone["caloriesOut"] += zone_calories[i]

    dataset = [
        {
            "time": (
                the_time + timedelta(seconds=(i if intraday else i * 60))
            ).strftime("%H:%M:%S"),
            "value": bpm,
        }
        for i, bpm in enumerate(heart_rate_values)
    ]

    heart_rate_data = {
        "heart_rate_day": [
            {
                "activities-heart": [
                    {
                        "dateTime": date,
                        "value": {
                            "customHeartRateZones": [],
                            "heartRateZones": heart_rate_zones,
                            "restingHeartRate": 58,
                        },
                    }
                ],
                "activities-heart-intraday": {
                    "dataset": dataset,
                    "datasetInterval": 1,
                    "datasetType": "minute" if not intraday else "second",
                },
            }
        ]
    }

    return heart_rate_data


def get_intraday_azm(date, hr):
    """Generate active zone minutes for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :param hr: heart rate data collected per second on the same day as date
    :type hr: dict
    :return: dictionary of intraday active zone minute details
    :rtype: dictionary
    """
    azm = {
        "activities-active-zone-minutes-intraday": [{"dateTime": date, "minutes": []}]
    }

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

    minutes_in_a_day = 1440
    hr_dataset = hr["heart_rate_day"][0]["activities-heart-intraday"]["dataset"]
    dataset_length = len(hr_dataset)

    mean_hr_per_minute = [
        np.mean(
            [
                hr_dataset[j]["value"]
                for j in range(i * 60, min((i + 1) * 60, dataset_length))
            ]
        )
        if i * 60 < dataset_length
        else hr_dataset[-1]["value"]
        for i in range(minutes_in_a_day)
    ]

    def get_activity_value(hr):
        if hr > 111:
            return {"peakActiveZoneMinutes": 1, "activeZoneMinutes": 1}
        elif hr > 98:
            return {"cardioActiveZoneMinutes": 1, "activeZoneMinutes": 1}
        elif hr > 87:
            return {"fatBurnActiveZoneMinutes": 1, "activeZoneMinutes": 1}
        else:
            return {"activeZoneMinutes": 0}

    azm["activities-active-zone-minutes-intraday"][0]["minutes"] = [
        {
            "minute": (the_time + timedelta(minutes=i)).strftime("%H:%M:%S"),
            "value": get_activity_value(mean_hr_per_minute[i]),
        }
        for i in range(minutes_in_a_day)
    ]

    return azm


def get_intraday_breath_rate(date):
    """Generate breath rate during sleep for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: dictionary of breath rate during sleep details
    :rtype: dictionary
    """
    breathing_rates = {
        stage: np.random.normal(info["mean"], info["std"])
        for stage, info in sleep_stages.items()
    }
    full_breathing_rate = np.mean(list(breathing_rates.values()))

    br = {
        "br": [
            {
                "value": {
                    **{
                        stage: {"breathingRate": rate}
                        for stage, rate in breathing_rates.items()
                    },
                    "fullSleepSummary": {"breathingRate": full_breathing_rate},
                },
                "dateTime": date,
            }
        ]
    }

    return br


def get_hrv(date):
    """Generate hrv for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: dictionary of hrv details
    :rtype: dictionary
    """
    hrv = {
        "hrv": [
            {
                "hrv": [
                    {
                        "value": {
                            "dailyRmssd": random.randint(13, 48),
                            "deepRmssd": random.randint(13, 48),
                        },
                        "dateTime": date,
                    }
                ]
            }
        ]
    }

    return hrv


def get_random_sleep_start_time():
    """Generate a random start time for sleep in terms of hour, minute and second, and a random duration of sleep in minutes."""
    random_hour = random.choice([21, 22, 23, 0, 1, 2])
    random_min = random.randint(0, 59)
    random_sec = random.randint(0, 59)
    random_duration = random.randint(360, 540)

    return random_hour, random_min, random_sec, random_duration


def get_intraday_hrv(date, random_hour, random_min, random_sec, random_duration):
    """Generate intraday HRV data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :param random_hour: the starting hour
    :type random_hour: int
    :param random_min: the starting minute
    :type random_min: int
    :param random_sec: the starting second
    :type random_sec: int
    :param random_duration: the number of minutes for which to generate data
    :type random_duration: int
    :return: dictionary of intraday HRV data details
    :rtype: dictionary
    """

    hrv = {"hrv": [{"minutes": [], "dateTime": date}]}

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(
        hour=random_hour, minute=random_min, second=random_sec
    )

    random_values = np.random.uniform(0, 1, (random_duration, 4))
    hf_values = np.round(100 + 900 * random_values[:, 0], 3)
    rmssd_values = np.round(20 + 60 * random_values[:, 1], 3)
    coverage_values = np.round(0.9 + 0.09 * random_values[:, 2], 3)
    lf_values = np.round(hf_values * (0.2 + 0.2 * random_values[:, 3]), 3)

    times = [the_time + timedelta(minutes=i) for i in range(random_duration)]

    hrv["hrv"][0]["minutes"] = [
        {
            "minute": f"{date}T{time.strftime('%H:%M:%S')}.000",
            "value": {
                "rmssd": rmssd,
                "coverage": coverage,
                "hf": hf,
                "lf": lf,
            },
        }
        for hf, rmssd, coverage, lf, time in zip(
            hf_values, rmssd_values, coverage_values, lf_values, times
        )
    ]

    return hrv


def get_intraday_spo2(date, random_hour, random_min, random_sec, random_duration):
    """Generate intraday SpO2 data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :param random_hour: the starting hour
    :type random_hour: int
    :param random_min: the starting minute
    :type random_min: int
    :param random_sec: the starting second
    :type random_sec: int
    :param random_duration: the number of minutes for which to generate data
    :type random_duration: int
    :return: dictionary of intraday SpO2 data details
    :rtype: dictionary
    """

    spo2_data = {"dateTime": date, "minutes": []}

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(
        hour=random_hour, minute=random_min, second=random_sec
    )

    mean = 97.5
    std_dev = 3
    spo2_value = round(np.random.normal(mean, std_dev), 1)
    spo2_value = max(95, min(100, spo2_value))

    random_changes = np.round(np.random.uniform(-0.5, 0.5, random_duration), 1)
    times = [the_time + timedelta(minutes=i) for i in range(random_duration)]

    spo2_data["minutes"] = [
        {
            "value": (spo2_value := max(95, min(100, spo2_value + change))),
            "minute": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        for change, time in zip(random_changes, times)
    ]

    return spo2_data


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

    minutes_in_a_day = 1440
    distance = [0, 0.1]
    weights = [0.6, 0.3]

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

    for i in range(minutes_in_a_day):
        distance = [0, 0.1]
        weights = [0.6, 0.3]
        max_distance = random.choices(distance, weights)
        if max_distance[0] == 0:
            val = 0
        else:
            val = random.randint(1, 1000) / 10000

        if 0 <= the_time.hour < 6 or 21 <= the_time.hour < 24:
            val = 0

        distance_day["distance_day"][0]["activities-distance-intraday"][
            "dataset"
        ].append({"time": the_time.strftime("%H:%M:%S"), "value": val})
        the_time = the_time + timedelta(seconds=60)

    return distance_day


def create_syn_data(seed, start_date, end_date):
    """Returns a dict of heart_rate data, activity data, "sleep", "steps","minutesVeryActive", "minutesLightlyActive", "minutesFairlyActive", "distance", "minutesSedentary", "heart_rate_day", "hrv", "distance_day"

    :param start_date: the start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: a dict of heart_rate data, activity data, "sleep", "steps","minutesVeryActive", "minutesLightlyActive", "minutesFairlyActive", "distance", "minutesSedentary", "heart_rate_day", "hrv", "distance_day"
    :rtype: dict
    """

    random.seed(seed)

    num_days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days

    # Generate dates as strings
    synth_dates = [
        (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime(
            "%Y-%m-%d"
        )
        for i in range(num_days)
    ]

    full_dict = {}
    full_dict["sleep"] = []
    full_dict["steps"] = []
    full_dict["minutesVeryActive"] = []
    full_dict["minutesFairlyActive"] = []
    full_dict["minutesLightlyActive"] = []
    full_dict["minutesSedentary"] = []
    full_dict["distance"] = []
    full_dict["heart_rate_day"] = []
    full_dict["hrv"] = []
    full_dict["distance_day"] = []
    full_dict["intraday_breath_rate"] = []
    full_dict["intraday_active_zone_minute"] = []
    full_dict["intraday_heart_rate"] = []
    full_dict["intraday_activity"] = []
    full_dict["intraday_heart_rate"] = []
    full_dict["intraday_hrv"] = []
    full_dict["intraday_spo2"] = []

    for date in synth_dates:
        (
            random_hour,
            random_min,
            random_sec,
            random_duration,
        ) = get_random_sleep_start_time()

        activity = get_activity(date)

        hr = get_heart_rate(date, intraday=False)
        intraday_hr = get_heart_rate(date, intraday=True)

        # Collect all data points

        full_dict["sleep"].append(get_sleep(date))
        full_dict["steps"].append(activity[0])
        full_dict["minutesVeryActive"].append(activity[1])
        full_dict["minutesFairlyActive"].append(activity[2])
        full_dict["minutesLightlyActive"].append(activity[3])
        full_dict["distance"].append(activity[4])
        full_dict["minutesSedentary"].append(activity[5])
        full_dict["heart_rate_day"].append(get_heart_rate(date))
        full_dict["hrv"].append(get_hrv(date))

        full_dict["distance_day"].append(get_distance_day(date))
        full_dict["intraday_breath_rate"].append(get_intraday_breath_rate(date))
        full_dict["intraday_active_zone_minute"].append(
            get_intraday_azm(date, intraday_hr)
        )
        full_dict["intraday_activity"].append(activity[0])
        full_dict["intraday_heart_rate"].append(intraday_hr)
        full_dict["intraday_hrv"].append(
            get_intraday_hrv(date, random_hour, random_min, random_sec, random_duration)
        )
        full_dict["intraday_spo2"].append(
            get_intraday_spo2(
                date, random_hour, random_min, random_sec, random_duration
            )
        )

    # encapsulate to match original data shape
    data = []
    for ele in full_dict["sleep"]:
        data.append(ele)
    full_dict["sleep"] = [{"sleep": data}]

    data = []
    for ele in full_dict["hrv"]:
        data.append(ele)
    full_dict["hrv"] = [{"hrv": data}]

    keys_to_update = [
        "steps",
        "minutesVeryActive",
        "minutesFairlyActive",
        "minutesLightlyActive",
        "distance",
        "minutesSedentary",
    ]

    for key in keys_to_update:
        data = []
        for ele in full_dict[key]:
            data.append(ele)
        full_dict[key] = [{f"activities-{key}": data}]

    full_dict["distance_day"] = full_dict["distance_day"][0]["distance_day"]
    full_dict["heart_rate_day"] = full_dict["heart_rate_day"][0]["heart_rate_day"]

    return full_dict
