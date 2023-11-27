import collections
import random
from datetime import datetime, timedelta

import numpy as np

__all__ = ["create_syn_data"]


def get_daily_activity(date):
    """Generate daily activity data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: daily activity data dictionary
    :rtype: dictionary
    """

    def convert_string_to_datetime(date_str):
        date_object = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date_str = f"{date_object.strftime('%Y-%m-%dT%H:%M:%S.%f')} -00:00"
        return formatted_date_str

    random_number = random.randint(100, 999)

    daily_activity = {
        "id": f"fd54d467-4c71-450e-a3ce-7a3951f3d{random_number}",
        "class_5_min": "".join(str(random.randint(0, 9)) for _ in range(300)),
        "score": random.randint(50, 100),
        "active_calories": random.randint(300, 1500),
        "average_met_minutes": random.randint(500, 2000) / 1000,
        "contributors": {
            "meet_daily_targets": random.randint(50, 100),
            "move_every_hour": random.randint(50, 100),
            "recovery_time": random.randint(50, 100),
            "stay_active": random.randint(50, 100),
            "training_frequency": random.randint(50, 100),
            "training_volume": random.randint(50, 100),
        },
        "equivalent_walking_distance": random.randint(500, 10000),
        "high_activity_met_minutes": random.randint(500, 2000) / 1000,
        "high_activity_time": random.randint(500, 2000) / 1000 * 60,
        "inactivity_alerts": random.randint(0, 10),
        "low_activity_met_minutes": random.randint(500, 2000) / 1000 * 60,
        "low_activity_time": random.randint(500, 2000) / 1000 * 60,
        "medium_activity_met_minutes": random.randint(500, 2000) / 1000 * 60,
        "medium_activity_time": random.randint(500, 2000) / 1000 * 60,
        "met": {
            "interval": 60.0,
            "timestamp": convert_string_to_datetime(date),
            "items": [round(random.uniform(0.9, 5.0), 1) for _ in range(300)],
        },
        "meters_to_target": random.randint(50, 2000),
        "non_wear_time": random.randint(50, 18000),
        "resting_time": random.randint(50, 18000),
        "sedentary_met_minutes": random.randint(500, 2000) / 1000 * 60,
        "sedentary_time": random.randint(500, 2000) / 1000 * 60,
        "steps": random.randint(500, 10000),
        "target_calories": 500,
        "target_meters": 10000,
        "total_calories": random.randint(1500, 4000),
        "day": date,
        "timestamp": convert_string_to_datetime(date),
    }
    return daily_activity


def get_sleep(date):
    """Generate sleep data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: sleep data dictionary
    :rtype: dictionary
    """
    summary_date = datetime.strptime(date, "%Y-%m-%d")

    period_id = 1
    is_longest = 1
    timezone = random.randint(-600, 600)
    bedtime_end = (
        summary_date + timedelta(minutes=random.randint(0, 1440))
    ).isoformat()
    bedtime_start = (
        summary_date + timedelta(minutes=random.randint(0, 1440))
    ).isoformat()
    sleep_type = random.choice(["long_sleep", "short_sleep"])
    breath_average = round(random.uniform(10, 20), 3)
    average_breath_variation = round(random.uniform(0, 5), 3)
    duration = random.randint(18000, 43200)
    total = random.randint(int(duration * 0.9), duration)
    awake = random.randint(0, int(duration * 0.1))
    rem = random.randint(int(duration * 0.2), int(duration * 0.3))
    deep = random.randint(int(duration * 0.4), int(duration * 0.6))
    light = total - rem - deep - awake
    midpoint_time = random.randint(int(duration * 0.4), int(duration * 0.6))
    efficiency = random.randint(80, 100)
    restless = random.randint(0, 10)
    onset_latency = random.randint(600, 1800)
    got_up_count = 0
    wake_up_count = random.randint(0, 10)
    hr_5min = [random.randint(50, 60) for _ in range(96)] + [0]

    hr_average = round(sum(hr_5min) / len(hr_5min), 3)
    hr_lowest = min(hr_5min)
    lowest_heart_rate_time_offset = hr_5min.index(hr_lowest) * 300

    hypnogram_5min = "".join([str(random.randint(1, 4)) for _ in range(96)])

    rmssd_5min = [random.randint(20, 120) for _ in range(96)] + [0]
    rmssd = round(sum(rmssd_5min) / len(rmssd_5min))

    score = random.randint(60, 90)
    score_alignment = random.randint(40, 80)
    score_deep = random.randint(80, 100)
    score_disturbances = random.randint(60, 90)
    score_efficiency = random.randint(80, 100)
    score_latency = random.randint(60, 90)
    score_rem = random.randint(40, 70)
    score_total = random.randint(50, 80)

    temperature_deviation = round(random.uniform(-1, 1), 2)
    temperature_trend_deviation = round(random.uniform(-0.1, 0.1), 2)
    bedtime_start_delta = random.randint(3000, 4000)
    bedtime_end_delta = random.randint(18000, 43200)
    midpoint_at_delta = random.randint(7200, 21600)
    temperature_delta = round(random.uniform(-1, 1), 2)

    sleep_data = {
        "summary_date": summary_date.strftime("%Y-%m-%d"),
        "period_id": period_id,
        "is_longest": is_longest,
        "timezone": timezone,
        "bedtime_end": bedtime_end,
        "bedtime_start": bedtime_start,
        "type": sleep_type,
        "breath_average": breath_average,
        "average_breath_variation": average_breath_variation,
        "duration": duration,
        "total": total,
        "awake": awake,
        "rem": rem,
        "deep": deep,
        "light": light,
        "midpoint_time": midpoint_time,
        "efficiency": efficiency,
        "restless": restless,
        "onset_latency": onset_latency,
        "got_up_count": got_up_count,
        "wake_up_count": wake_up_count,
        "hr_5min": hr_5min,
        "hr_average": hr_average,
        "hr_lowest": hr_lowest,
        "lowest_heart_rate_time_offset": lowest_heart_rate_time_offset,
        "hypnogram_5min": hypnogram_5min,
        "rmssd": rmssd,
        "rmssd_5min": rmssd_5min,
        "score": score,
        "score_alignment": score_alignment,
        "score_deep": score_deep,
        "score_disturbances": score_disturbances,
        "score_efficiency": score_efficiency,
        "score_latency": score_latency,
        "score_rem": score_rem,
        "score_total": score_total,
        "temperature_deviation": temperature_deviation,
        "temperature_trend_deviation": temperature_trend_deviation,
        "bedtime_start_delta": bedtime_start_delta,
        "bedtime_end_delta": bedtime_end_delta,
        "midpoint_at_delta": midpoint_at_delta,
        "temperature_delta": temperature_delta,
    }
    return sleep_data


def get_activity(date):
    """Generate activity data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: dictionary of activity data
    :rtype: dictionary
    """
    summary_date = datetime.strptime(date, "%Y-%m-%d")
    start_time = summary_date.replace(hour=4, minute=0, second=0)
    end_time = start_time + timedelta(days=1) - timedelta(seconds=1)
    timezone_offset = -420

    cal_active = random.randint(300, 800)
    cal_total = cal_active + random.randint(1500, 2000)
    steps = random.randint(8000, 15000)
    daily_movement = random.randint(7000, 12000)

    non_wear = random.randint(0, 120)
    rest = random.randint(400, 600)
    inactive = random.randint(500, 800)
    low = random.randint(200, 400)
    medium = random.randint(50, 150)
    high = random.randint(0, 20)
    inactivity_alerts = random.randint(0, 3)
    average_met = round(random.uniform(1.0, 1.8), 2)

    met_1min = [round(random.uniform(0.9, 5.0), 1) for _ in range(1440)]

    activity_data = {
        "summary_date": summary_date.strftime("%Y-%m-%d"),
        "timezone": timezone_offset,
        "day_start": start_time.isoformat(),
        "day_end": end_time.isoformat(),
        "cal_active": cal_active,
        "cal_total": cal_total,
        "class_5min": "".join(str(random.randint(0, 5)) for _ in range(288)),
        "steps": steps,
        "daily_movement": daily_movement,
        "non_wear": non_wear,
        "rest": rest,
        "inactive": inactive,
        "low": low,
        "medium": medium,
        "high": high,
        "inactivity_alerts": inactivity_alerts,
        "average_met": average_met,
        "met_1min": met_1min,
    }

    return activity_data


def get_readiness(date):
    """Generate readiness data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: daily activity data dictionary
    :rtype: dictionary
    """

    summary_date = datetime.strptime(date, "%Y-%m-%d")
    score = random.randint(70, 100)
    score_activity_balance = random.randint(70, 100)
    score_hrv_balance = random.randint(70, 100)
    score_previous_day = random.randint(70, 100)
    score_previous_night = random.randint(70, 100)
    score_recovery_index = random.randint(70, 100)
    score_resting_hr = random.randint(70, 100)
    score_sleep_balance = random.randint(70, 100)
    score_temperature = random.randint(70, 99)

    rest_mode_state = random.randint(0, 1)
    period_id = random.randint(1, 4)

    readiness_data = {
        "summary_date": summary_date.strftime("%Y-%m-%d"),
        "score": score,
        "score_activity_balance": score_activity_balance,
        "score_hrv_balance": score_hrv_balance,
        "score_previous_day": score_previous_day,
        "score_previous_night": score_previous_night,
        "score_recovery_index": score_recovery_index,
        "score_resting_hr": score_resting_hr,
        "score_sleep_balance": score_sleep_balance,
        "score_temperature": score_temperature,
        "rest_mode_state": rest_mode_state,
        "period_id": period_id,
    }

    return readiness_data


def get_ideal_bedtime(date):
    """Generate ideal bedtime data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: daily activity data dictionary
    :rtype: dictionary
    """
    date = datetime.strptime(date, "%Y-%m-%d")

    start_time = random.randint(0, 86400)
    end_time = random.randint(start_time, 86400)

    ideal_bedtime_data = {
        "date": date.strftime("%Y-%m-%d"),
        "bedtime_window": {"start": start_time, "end": end_time},
        "status": "IDEAL_BEDTIME_AVAILABLE",
    }

    return ideal_bedtime_data


def get_heart_rate(date):
    """Generate heart rate data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: heart rate data dictionary
    :rtype: dictionary
    """
    date = datetime.strptime(date, "%Y-%m-%d")

    timestamp = date.timestamp()

    heart_rate_data = []

    number_of_minues_in_a_day = 1440

    bpm = random.randint(50, 120)

    for i in range(0, number_of_minues_in_a_day, 5):
        # Calculate the current hour based on the timestamp
        hour = int((date + timedelta(minutes=i)).strftime("%H"))

        # Determine if the person is awake (6 AM to 10 PM)
        is_awake = 6 <= hour < 22
        status = "awake" if is_awake else "asleep"

        # Gradually change the heart rate within a realistic range
        if is_awake:
            # Simulate an increase in heart rate during awake hours
            bpm += random.randint(-3, 5)
            bpm = min(
                random.randint(100, 120), bpm
            )  # Ensure heart rate doesn't exceed 120 bpm
        else:
            # Simulate a decrease in heart rate during asleep hours
            bpm -= random.randint(-3, 5)
            bpm = max(
                random.randint(50, 70), bpm
            )  # Ensure heart rate doesn't go below 50 bpm

        formatted_timestamp = (date + timedelta(minutes=i)).strftime(
            "%Y-%m-%dT%H:%M:%S+00:00"
        )

        heart_rate_entry = {
            "bpm": bpm,
            "source": status,
            "timestamp": formatted_timestamp,
        }

        heart_rate_data.append(heart_rate_entry)

    return heart_rate_data


def create_syn_data(start_date, end_date):
    """Returns a dict of daily activity data, sleep data, ideal bedtime, readiness, and activity

    :param start_date: the start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: a defaultdict of daily activity data, sleep data, ideal bedtime, readiness, and activity
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
        full_dict["daily_activity"].append(get_daily_activity(date))
        full_dict["activity"].append(get_activity(date))
        full_dict["ideal_bedtime"].append(get_ideal_bedtime(date))
        full_dict["readiness"].append(get_readiness(date))
        full_dict["heart_rate"].extend(get_heart_rate(date))

    return full_dict
