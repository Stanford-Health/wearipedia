import collections
import random
from datetime import datetime, time, timedelta
from random import choice, choices, randrange

import numpy as np

__all__ = ["create_syn_data"]


def get_sleep(date):
    """Generate sleep data for a given date.


    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
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
        "dateOfSleep": date,
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

    very_active = np.random.randint(0, 240)
    fairly_active = np.random.randint(0, 240)
    lightly_active = np.random.randint(0, 240)

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

    # Initialize the time
    the_time = datetime.strptime(date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

    # Determine the number of iterations based on intraday flag
    iterations_in_a_day = 1440 if not intraday else 1440 * 60

    # Initialize the bpm value
    bpm = np.clip(np.random.normal(75, 15, 1)[0], 50, 195)

    # Precompute time intervals
    time_intervals = [
        the_time + timedelta(seconds=(i if intraday else i * 60))
        for i in range(iterations_in_a_day)
    ]

    heart_rate_zones = heart_rate_data["heart_rate_day"][0]["activities-heart"][0][
        "value"
    ]["heartRateZones"]

    for i in range(iterations_in_a_day):
        hour = time_intervals[i].hour

        # Determine which heart rate zone based on the hour
        if hour < 6 or hour >= 22:
            inx = 0
        elif 6 <= hour < 10:
            inx = 1
        elif 10 <= hour < 18:
            inx = 2
        else:
            inx = 3

        # Update heart rate zone data
        heart_rate_zones[inx]["minutes"] += 1
        heart_rate_zones[inx]["caloriesOut"] += 2 * (inx + 0.5)

        random_walk = np.random.randint(-1, 2, size=iterations_in_a_day)

        # Update bpm value using precomputed random walk changes
        bpm = np.clip(bpm + random_walk[i], 50, 195)

        # Add new data point to dataset
        heart_rate_data["heart_rate_day"][0]["activities-heart-intraday"][
            "dataset"
        ].append({"time": time_intervals[i].strftime("%H:%M:%S"), "value": bpm})

    return heart_rate_data


def get_intraday_azm(date, hr):
    """Generate hrv for a given date.

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
    dataset_length = len(
        hr["heart_rate_day"][0]["activities-heart-intraday"]["dataset"]
    )

    for i in range(minutes_in_a_day):
        if i * 60 + 59 < dataset_length:
            mean_hr_in_minute = (
                sum(
                    hr["heart_rate_day"][0]["activities-heart-intraday"]["dataset"][j][
                        "value"
                    ]
                    for j in range(i * 60, (i + 1) * 60)
                )
                / 60
            )
        else:
            mean_hr_in_minute = hr["heart_rate_day"][0]["activities-heart-intraday"][
                "dataset"
            ][-1]["value"]

        if mean_hr_in_minute > 111:
            minute_info = {
                "minute": the_time.strftime("%H:%M:%S"),
                "value": {"peakActiveZoneMinutes": 1, "activeZoneMinutes": 1},
            }
        elif mean_hr_in_minute > 98:
            minute_info = {
                "minute": the_time.strftime("%H:%M:%S"),
                "value": {"cardioActiveZoneMinutes": 1, "activeZoneMinutes": 1},
            }
        elif mean_hr_in_minute > 87:
            minute_info = {
                "minute": the_time.strftime("%H:%M:%S"),
                "value": {"fatBurnActiveZoneMinutes": 1, "activeZoneMinutes": 1},
            }
        else:
            minute_info = {
                "minute": the_time.strftime("%H:%M:%S"),
                "value": {"activeZoneMinutes": 0},
            }

        azm["activities-active-zone-minutes-intraday"][0]["minutes"].append(minute_info)
        the_time += timedelta(minutes=1)

    return azm


def get_intraday_activity(date, hr):
    """Generate intraday activity for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: dictionary of intraday activity details
    :rtype: dictionary
    """
    azm = {
        "activities-active-zone-minutes-intraday": [{"dateTime": date, "minutes": []}]
    }

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

    # Extract the heart rate dataset once to avoid repeated lookups
    hr_dataset = hr["heart_rate_day"][0]["activities-heart-intraday"]["dataset"]
    dataset_length = len(hr_dataset)

    # Precompute mean heart rates for each minute
    mean_hr_per_minute = []
    for i in range(1440):  # 1440 minutes in a day
        if i * 60 + 59 < dataset_length:
            mean_hr = np.mean(
                [hr_dataset[j]["value"] for j in range(i * 60, (i + 1) * 60)]
            )
        else:
            mean_hr = hr_dataset[-1]["value"]
        mean_hr_per_minute.append(mean_hr)

    for i in range(1440):
        mean_hr_in_minute = mean_hr_per_minute[i]

        if mean_hr_in_minute > 111:
            value = {"peakActiveZoneMinutes": 1, "activeZoneMinutes": 1}
        elif mean_hr_in_minute > 98:
            value = {"cardioActiveZoneMinutes": 1, "activeZoneMinutes": 1}
        elif mean_hr_in_minute > 87:
            value = {"fatBurnActiveZoneMinutes": 1, "activeZoneMinutes": 1}
        else:
            value = {"activeZoneMinutes": 0}

        minute_info = {"minute": the_time.strftime("%H:%M:%S"), "value": value}

        azm["activities-active-zone-minutes-intraday"][0]["minutes"].append(minute_info)
        the_time += timedelta(minutes=1)

    return azm


def get_intraday_breath_rate(date):
    """Generate breath rate during sleep for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: dictionary of breath rate during sleep details
    :rtype: dictionary
    """
    # Define mean and standard deviation for each sleep stage
    sleep_stages = {
        "deepSleepSummary": {"mean": 12, "std": 1.5},
        "remSleepSummary": {"mean": 16, "std": 1.5},
        "lightSleepSummary": {"mean": 18, "std": 2},
    }

    # Generate breathing rates using Gaussian distribution and calculate full breathing rate
    breathing_rates = {
        stage: np.random.normal(info["mean"], info["std"])
        for stage, info in sleep_stages.items()
    }
    full_breathing_rate = np.mean(list(breathing_rates.values()))

    # Construct the result dictionary
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


def get_random_sleep_start_time():
    """Generate a random start time for sleep in terms of hour, minute and second."""
    random_hour = random.choice([21, 22, 23, 0, 1, 2])
    random_min = random.randint(0, 59)
    random_sec = random.randint(0, 59)
    random_duration = random.randint(360, 540)

    return random_hour, random_min, random_sec, random_duration


def get_intraday_hrv(date, random_hour, random_min, random_sec, random_duration):
    """Generate intraday hrv for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: dictionary of intraday hrv details
    :rtype: dictionary
    """
    hrv = {"hrv": [{"minutes": [], "dateTime": date}]}

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(
        hour=random_hour, minute=random_min, second=random_sec
    )

    minutes = []
    for _ in range(random_duration):
        hf = round(random.uniform(100, 1000), 3)
        min_lf = max(100, hf * 0.20)
        max_lf = min(hf, hf * 0.40)
        lf = round(random.uniform(min_lf, max_lf), 3)

        minute_info = {
            "minute": f"{date}T{the_time.strftime('%H:%M:%S')}.000",
            "value": {
                "rmssd": round(random.uniform(20, 80), 3),
                "coverage": round(random.uniform(0.9, 0.99), 3),
                "hf": hf,
                "lf": lf,
            },
        }

        minutes.append(minute_info)
        the_time += timedelta(minutes=1)

    hrv["hrv"][0]["minutes"] = minutes
    return hrv


def get_intraday_spo2(date, random_hour, random_min, random_sec, random_duration):
    """Generate intraday SpO2 data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: dictionary of intraday SpO2 data details
    :rtype: dictionary
    """

    spo2_data = {"dateTime": date, "minutes": []}

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(
        hour=random_hour, minute=random_min, second=random_sec
    )

    # Initial SpO2 value from a Gaussian distribution
    mean = 97.5
    std_dev = 3
    spo2_value = round(np.random.normal(mean, std_dev), 1)
    spo2_value = max(95, min(100, spo2_value))

    minutes = []
    for _ in range(random_duration):
        # Simulate gradual SpO2 changes within a realistic range
        spo2_value += round(random.uniform(-0.5, 0.5), 1)
        spo2_value = max(95, min(100, spo2_value))

        minute_info = {
            "value": spo2_value,
            "minute": the_time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        minutes.append(minute_info)

        the_time += timedelta(minutes=1)

    spo2_data["minutes"] = minutes
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

    the_time = datetime.strptime(date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

    minutes_in_a_day = 1440

    for i in range(minutes_in_a_day):

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
        the_time += timedelta(minutes=1)

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

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end_dt - start_dt).days + 1

    # Generate dates as strings
    synth_dates = [
        (start_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)
    ]

    full_dict = collections.defaultdict(list)

    for date in synth_dates:
        (
            random_hour,
            random_min,
            random_sec,
            random_duration,
        ) = get_random_sleep_start_time()

        activity = get_activity(date)
        intraday_hr = get_heart_rate(date, intraday=True)

        # Collect all data points
        full_dict["sleep"].append(get_sleep(date))
        full_dict["steps"].append(activity[0])
        full_dict["minutesVeryActive"].append(activity[1])
        full_dict["minutesFairlyActive"].append(activity[2])
        full_dict["minutesLightlyActive"].append(activity[3])
        full_dict["distance"].append(activity[4])
        full_dict["minutesSedentary"].append(activity[5])
        full_dict["heart_rate"].append(get_heart_rate(date, intraday=False))
        full_dict["intraday_heart_rate"].append(intraday_hr)
        full_dict["hrv"].append(get_hrv(date))
        full_dict["distance_day"].append(get_distance_day(date))
        full_dict["intraday_spo2"].append(
            get_intraday_spo2(
                date, random_hour, random_min, random_sec, random_duration
            )
        )
        full_dict["intraday_hrv"].append(
            get_intraday_hrv(date, random_hour, random_min, random_sec, random_duration)
        )
        full_dict["intraday_activity"].append(get_intraday_activity(date, intraday_hr))
        full_dict["intraday_active_zone_minute"].append(
            get_intraday_azm(date, intraday_hr)
        )
        full_dict["intraday_breath_rate"].append(get_intraday_breath_rate(date))

    return full_dict
