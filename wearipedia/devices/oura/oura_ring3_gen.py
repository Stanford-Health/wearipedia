import collections
from datetime import datetime, timedelta

import numpy as np

__all__ = ["create_syn_data"]


def convert_string_to_datetime(date_str):
    date_object = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date_str = f"{date_object.strftime('%Y-%m-%dT%H:%M:%S.%f')} -00:00"
    return formatted_date_str


def get_daily_activity(date):
    """Generate daily activity data for a given date.

    :param date: the date as a string in the format "YYYY-MM-DD"
    :type date: str
    :return: daily activity data dictionary
    :rtype: dictionary
    """

    random_number = np.random.randint(100, 999)

    daily_activity = {
        "id": f"fd54d467-4c71-450e-a3ce-7a3951f3d{random_number}",
        "class_5_min": "".join(str(np.random.randint(0, 9)) for _ in range(300)),
        "score": np.random.randint(50, 100),
        "active_calories": np.random.randint(300, 1500),
        "average_met_minutes": np.random.randint(500, 2000) / 1000,
        "contributors": {
            "meet_daily_targets": np.random.randint(50, 100),
            "move_every_hour": np.random.randint(50, 100),
            "recovery_time": np.random.randint(50, 100),
            "stay_active": np.random.randint(50, 100),
            "training_frequency": np.random.randint(50, 100),
            "training_volume": np.random.randint(50, 100),
        },
        "equivalent_walking_distance": np.random.randint(500, 10000),
        "high_activity_met_minutes": np.random.randint(500, 2000) / 1000,
        "high_activity_time": np.random.randint(500, 2000) / 1000 * 60,
        "inactivity_alerts": np.random.randint(0, 10),
        "low_activity_met_minutes": np.random.randint(500, 2000) / 1000 * 60,
        "low_activity_time": np.random.randint(500, 2000) / 1000 * 60,
        "medium_activity_met_minutes": np.random.randint(500, 2000) / 1000 * 60,
        "medium_activity_time": np.random.randint(500, 2000) / 1000 * 60,
        "met": {
            "interval": 60.0,
            "timestamp": convert_string_to_datetime(date),
            "items": [round(np.random.uniform(0.9, 5.0), 1) for _ in range(300)],
        },
        "meters_to_target": np.random.randint(50, 2000),
        "non_wear_time": np.random.randint(50, 18000),
        "resting_time": np.random.randint(50, 18000),
        "sedentary_met_minutes": np.random.randint(500, 2000) / 1000 * 60,
        "sedentary_time": np.random.randint(500, 2000) / 1000 * 60,
        "steps": np.random.randint(500, 10000),
        "target_calories": 500,
        "target_meters": 10000,
        "total_calories": np.random.randint(1500, 4000),
        "day": date,
        "timestamp": convert_string_to_datetime(date),
    }
    return daily_activity


def get_daily_sleep(date):
    daily_sleep_data = {
        "id": 1,
        "contributors": {
            "deep_sleep": np.random.randint(1, 100),
            "efficiency": np.random.randint(1, 100),
            "latency": np.random.randint(1, 100),
            "rem_sleep": np.random.randint(1, 100),
            "restfulness": np.random.randint(1, 100),
            "timing": np.random.randint(1, 100),
            "total_sleep": np.random.randint(1, 100),
        },
        "day": date,
        "score": np.random.randint(1, 100),
        "timestamp": convert_string_to_datetime(date),
    }
    return daily_sleep_data


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
    timezone = np.random.randint(-600, 600)
    bedtime_end = (
        summary_date + timedelta(minutes=np.random.randint(0, 1440))
    ).isoformat()
    bedtime_start = (
        summary_date + timedelta(minutes=np.random.randint(0, 1440))
    ).isoformat()
    sleep_type = np.random.choice(["long_sleep", "short_sleep"])
    breath_average = round(np.random.uniform(10, 20), 3)
    average_breath_variation = round(np.random.uniform(0, 5), 3)
    duration = np.random.randint(18000, 43200)
    total = np.random.randint(int(duration * 0.9), duration)
    awake = np.random.randint(0, int(duration * 0.1))
    rem = np.random.randint(int(duration * 0.2), int(duration * 0.3))
    deep = np.random.randint(int(duration * 0.4), int(duration * 0.6))
    light = total - rem - deep
    midpoint_time = np.random.randint(int(duration * 0.4), int(duration * 0.6))
    efficiency = np.random.randint(80, 100)
    restless = np.random.randint(5 * 60, 30 * 60)
    onset_latency = np.random.randint(600, 1800)
    got_up_count = 0
    wake_up_count = np.random.randint(0, 10)
    hr_5min = [np.random.randint(50, 60) for _ in range(96)] + [0]

    hr_average = round(sum(hr_5min) / len(hr_5min), 3)
    hr_lowest = min(hr_5min)
    lowest_heart_rate_time_offset = hr_5min.index(hr_lowest) * 300

    hypnogram_5min = "".join([str(np.random.randint(1, 4)) for _ in range(96)])

    rmssd_5min = [np.random.randint(20, 120) for _ in range(96)] + [0]
    rmssd = round(sum(rmssd_5min) / len(rmssd_5min))

    score = np.random.randint(60, 90)
    score_alignment = np.random.randint(40, 80)
    score_deep = np.random.randint(80, 100)
    score_disturbances = np.random.randint(60, 90)
    score_efficiency = np.random.randint(80, 100)
    score_latency = np.random.randint(60, 90)
    score_rem = np.random.randint(40, 70)
    score_total = np.random.randint(50, 80)

    temperature_deviation = round(np.random.uniform(-1, 1), 2)
    temperature_trend_deviation = round(np.random.uniform(-0.1, 0.1), 2)
    bedtime_start_delta = np.random.randint(3000, 4000)
    bedtime_end_delta = np.random.randint(18000, 43200)
    midpoint_at_delta = np.random.randint(7200, 21600)
    temperature_delta = round(np.random.uniform(-1, 1), 2)

    sleep_data = {
        "id": period_id,
        "average_breath": breath_average,
        "average_heart_rate": hr_average,
        "average_hrv": np.random.randint(45, 65),
        "awake_time": awake,
        "bedtime_end": bedtime_end,
        "bedtime_start": bedtime_start,
        "day": summary_date.strftime("%Y-%m-%d"),
        "deep_sleep_duration": deep,
        "efficiency": efficiency,
        "heart_rate": {
            "interval": 0,
            "items": [0],
            "timestamp": convert_string_to_datetime(date),
        },
        "hrv": {
            "interval": 0,
            "items": [0],
            "timestamp": convert_string_to_datetime(date),
        },
        "latency": np.random.randint(600, 1800),
        "light_sleep_duration": light,
        "low_battery_alert": False,
        "lowest_heart_rate": hr_lowest,
        "movement_30_sec": "1",
        "period": period_id,
        "readiness": {
            "contributors": {
                "activity_balance": np.random.randint(1, 100),
                "body_temperature": np.random.randint(1, 100),
                "hrv_balance": np.random.randint(1, 100),
                "previous_day_activity": np.random.randint(1, 100),
                "previous_night": np.random.randint(1, 100),
                "recovery_index": np.random.randint(1, 100),
                "resting_heart_rate": np.random.randint(1, 100),
                "sleep_balance": np.random.randint(1, 100),
            },
            "score": np.random.randint(1, 100),
            "temperature_deviation": round(np.random.uniform(-1, 1), 2),
            "temperature_trend_deviation": round(np.random.uniform(-1, 1), 2),
        },
        "readiness_score_delta": np.random.randint(-100, 100),
        "rem_sleep_duration": rem,
        "restless_periods": restless,
        "sleep_phase_5_min": "1",
        "sleep_score_delta": np.random.randint(-100, 100),
        "sleep_algorithm_version": "1.0.0",
        "time_in_bed": total + awake,
        "total_sleep_duration": total,
        "type": sleep_type,
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

    cal_active = np.random.randint(300, 800)
    cal_total = cal_active + np.random.randint(1500, 2000)
    steps = np.random.randint(8000, 15000)
    daily_movement = np.random.randint(7000, 12000)

    non_wear = np.random.randint(0, 120) * 60
    rest = np.random.randint(400, 600) * 60
    inactive = np.random.randint(500, 800)
    low = np.random.randint(200, 400)
    medium = np.random.randint(50, 150) * 60
    high = np.random.randint(0, 20)
    inactivity_alerts = np.random.randint(0, 3)
    average_met = round(np.random.uniform(1.0, 1.8), 2)

    met_1min = [round(np.random.uniform(0.9, 5.0), 1) for _ in range(1440)]

    activity_data = {
        "summary_date": summary_date.strftime("%Y-%m-%d"),
        "timezone": timezone_offset,
        "day_start": start_time.isoformat(),
        "day_end": end_time.isoformat(),
        "cal_active": cal_active,
        "cal_total": cal_total,
        "class_5min": "".join(str(np.random.randint(0, 5)) for _ in range(288)),
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
    score = np.random.randint(70, 100)
    score_activity_balance = np.random.randint(70, 100)
    score_hrv_balance = np.random.randint(70, 100)
    score_previous_day = np.random.randint(70, 100)
    score_previous_night = np.random.randint(70, 100)
    score_recovery_index = np.random.randint(70, 100)
    score_resting_hr = np.random.randint(70, 100)
    score_sleep_balance = np.random.randint(70, 100)
    score_temperature = np.random.randint(70, 99)

    rest_mode_state = np.random.randint(0, 1)
    period_id = np.random.randint(1, 4)

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

    start_time = np.random.randint(0, 86400)
    end_time = np.random.randint(start_time, 86400)

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

    bpm = np.random.randint(50, 120)

    for i in range(0, number_of_minues_in_a_day, 5):
        # Calculate the current hour based on the timestamp
        hour = int((date + timedelta(minutes=i)).strftime("%H"))

        # Determine if the person is awake (6 AM to 10 PM)
        is_awake = 6 <= hour < 22
        status = "awake" if is_awake else "asleep"

        # Gradually change the heart rate within a realistic range
        if is_awake:
            # Simulate an increase in heart rate during awake hours
            bpm += np.random.randint(-3, 5)
            bpm = min(
                np.random.randint(100, 120), bpm
            )  # Ensure heart rate doesn't exceed 120 bpm
        else:
            # Simulate a decrease in heart rate during asleep hours
            bpm -= np.random.randint(-3, 5)
            bpm = max(
                np.random.randint(50, 70), bpm
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


def get_session(date):
    return []


def get_enhanced_tag(date):
    return []


def get_workout(date):
    return []


def create_syn_data(seed, start_date, end_date):
    """Returns a dict of daily activity data, sleep data, ideal bedtime, readiness, and activity

    :param start_date: the start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: a defaultdict of daily activity data, sleep data, ideal bedtime, readiness, and activity
    :rtype: defaultdict
    """
    np.random.seed(seed)

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
        full_dict["heart_rate"].extend(get_heart_rate(date))
        full_dict["session"].extend(get_session(date))
        full_dict["enhanced_tag"].extend(get_enhanced_tag(date))
        full_dict["workout"].extend(get_workout(date))
        full_dict["daily_activity"].append(get_daily_activity(date))
        full_dict["daily_sleep"].append(get_daily_sleep(date))
        full_dict["sleep"].append(get_sleep(date))
        full_dict["readiness"].append(get_readiness(date))
        full_dict["ideal_sleep_time"].append(get_ideal_bedtime(date))

    return full_dict
