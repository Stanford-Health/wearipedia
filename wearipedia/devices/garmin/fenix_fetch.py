import os
from datetime import datetime, timedelta
from threading import Lock, Thread

from tqdm import tqdm

__all__ = ["fetch_real_data"]


def fetch_garmin_url(data_type):
    """Fetches the Garmin Connect API endpoint URL corresponding to a given data type.

    This function takes a data type as input and retrieves the associated API endpoint URL from a predefined dictionary.
    If the provided data type is found in the dictionary keys, it returns the respective endpoint URL.
    If the data type is not found, it returns None.

    :param data_type: A string representing the type of data for which the API endpoint URL is requested.
    :type data_type: str
    :return: The Garmin Connect API endpoint URL for the given data type, or None if not found.
    :rtype: Union[str, None]
    """

    url_dict = {
        "stats": "/usersummary-service/usersummary/daily",
        "body_composition": "/weight-service/weight/dateRange",
        "body_composition_aggregated": "/weight-service",
        "steps": "/wellness-service/wellness/dailySummaryChart",
        "daily_steps": "/usersummary-service/stats/steps/daily",
        "body_battery": "/wellness-service/wellness/bodyBattery/reports/daily",
        "hr": "/wellness-service/wellness/dailyHeartRate",
        "training_readiness": "/metrics-service/metrics/trainingreadiness",
        "blood_pressure": "/bloodpressure-service/bloodpressure/range",
        "floors": "/wellness-service/wellness/floorsChartData/daily",
        "training_status": "/metrics-service/metrics/trainingstatus/aggregated",
        "rhr": "/userstats-service/wellness/daily",
        "hydration": "/usersummary-service/usersummary/hydration/daily",
        "sleep": "/wellness-service/wellness/dailySleepData",
        "stress": "/wellness-service/wellness/dailyStress",
        "day_stress_aggregated": "/wellness-service/wellness/dailyStress",
        "respiration": "/wellness-service/wellness/daily/respiration",
        "spo2": "/wellness-service/wellness/daily/spo2",
        "max_metrics": "/metrics-service/metrics/maxmet/daily",
        "personal_record": "/personalrecord-service/personalrecord/prs",
        "earned_badges": "/badge-service/badge/earned",
        "adhoc_challenges": "/adhocchallenge-service/adHocChallenge/historical",
        "available_badges": "/badgechallenge-service/badgeChallenge/available",
        "available_badge_challenges": "/badgechallenge-service/badgeChallenge/available",
        "badge_challenges": "/badgechallenge-service/badgeChallenge/completed",
        "non_completed_badge_challenges": "/badgechallenge-service/badgeChallenge/non-completed",
        "activities": "/activitylist-service/activities/search/activities",
        "activities_fordate_aggregated": "/mobile-gateway/heartRate/forDate",
        "devices": "/device-service/deviceregistration/devices",
        "device_last_used": "/device-service/deviceservice/mylastused",
        "device_settings": "/device-service/deviceservice/device-info/settings",
        "active_goals": "/goal-service/goal/goals",
        "future_goals": "/goal-service/goal/goals",
        "past_goals": "/goal-service/goal/goals",
        "hrv": "/hrv-service/hrv",
        "weigh_ins": "/weight-service/weight/range",
        "weigh_ins_daily": "/weight-service/weight/dayview",
        "hill_score": "/metrics-service/metrics/hillscore/stats",
        "endurance_score": "/metrics-service/metrics/endurancescore/stats",
        "inprogress_virtual_challenges": "/badgechallenge-service/virtualChallenge/inProgress",
        "race_prediction": "/metrics-service/metrics/racepredictions/latest",
    }
    if data_type in url_dict.keys():
        return url_dict[data_type]
    else:
        return None


# Stats
def fetch_stats(api, data_type, start_date, num_days, params=None):
    display_name = api.profile["displayName"]
    url = f"{fetch_garmin_url(data_type)}/{display_name}"
    response = []
    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        params = {"calendarDate": str(new_date.date())}
        response.append(api.connectapi(url, params=params))
    return response


# Steps, HR
def fetch_steps_and_hr(api, data_type, start_date, num_days, params=None):
    display_name = api.profile["displayName"]
    url = f"{fetch_garmin_url(data_type)}/{display_name}"
    response = []
    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        params = {"date": str(new_date.date())}
        response.append(api.connectapi(url, params=params))
    return response


# Floors, Stress, Respiration, Spo2, Hydration, HRV, Training Status, Training Readiness, Activities for Date Aggregated, Day Stress Aggregated
def fetch_aggregated_data(api, data_type, start_date, num_days, params=None):
    response = []
    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        url = f"{fetch_garmin_url(data_type)}/{new_date.date()}"
        response.append(api.connectapi(url))
    return response


# Body Composition
def fetch_body_composition(api, data_type, start_date, end_date, params=None):
    url = f"{fetch_garmin_url(data_type)}"
    params = {"startDate": str(start_date), "endDate": str(end_date)}
    return api.connectapi(url, params=params)


# Blood Pressure, Weigh Ins
def fetch_blood_pressure_and_weigh_ins(
    api, data_type, start_date, end_date, params=None
):
    url = f"{fetch_garmin_url(data_type)}/{start_date}/{end_date}"
    params = {"includeAll": True}
    return api.connectapi(url, params=params)


# RHR
def fetch_resting_heart_rate(api, data_type, start_date, end_date, params=None):
    display_name = api.profile["displayName"]
    url = f"{fetch_garmin_url(data_type)}/{display_name}"
    params = {"fromDate": str(start_date), "untilDate": str(end_date), "metricId": 60}
    return api.connectapi(url, params=params)


# Personal Record, Race Prediction
def fetch_personal_record_and_race_prediction(api, data_type, params=None):
    display_name = api.profile["displayName"]
    url = f"{fetch_garmin_url(data_type)}/{display_name}"
    return api.connectapi(url)


# Earned Badges, Devices, Device Last Used
def fetch_badges_and_devices(api, data_type, params=None):
    url = fetch_garmin_url(data_type)
    return api.connectapi(url)


# Adhoc Challenges, Available Badges, Available Badge Challenges, Badge Challenges, Non Completed Badge Challenges, In Progress Virtual Challenges, Activities
def fetch_challenges_and_activities(api, data_type, params=None):
    url = f"{fetch_garmin_url(data_type)}"
    params = {"start": str(1), "limit": str(100)}
    return api.connectapi(url, params=params)


# Weigh Ins Daily
def fetch_daily_weigh_ins(api, data_type, start_date, num_days, params=None):
    response = []
    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        url = f"{fetch_garmin_url(data_type)}/{new_date.date()}"
        params = {"includeAll": True}
        response.append(api.connectapi(url, params=params))
    return response


# Hill Score, Endurance Score
def fetch_scores(api, data_type, start_date, end_date, params=None):
    url = f"{fetch_garmin_url(data_type)}"
    params = {
        "startDate": str(start_date),
        "endDate": str(end_date),
        "aggregation": "daily",
    }
    return api.connectapi(url, params=params)


# Activities Date
def fetch_activities_date(api, start_date, end_date, params=None):
    url = fetch_garmin_url("activities")
    params = {
        "startDate": str(start_date),
        "endDate": str(end_date),
        "start": str(0),
        "limit": str(100),
        "activityType": "",
    }
    return api.connectapi(url, params=params)


# Sleep
def fetch_sleep(api, data_type, start_date, num_days, params=None):
    display_name = api.profile["displayName"]
    response = []
    url = f"{fetch_garmin_url(data_type)}/{display_name}"
    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        params = {"date": str(new_date.date()), "nonSleepBufferMinutes": 60}
        response.append(api.connectapi(url, params=params))
    return response


# Max Metrics, Daily Steps
def fetch_max_metrics_and_daily_steps(
    api, data_type, start_date, num_days, params=None
):
    response = []
    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        url = f"{fetch_garmin_url(data_type)}/{new_date.date()}/{new_date.date()}"
        response.append(api.connectapi(url))
    return response


# Active Goals, Future Goals, Past Goals
def fetch_goals(api, data_type, status, params=None):
    start = 1
    limit = 30
    goals = []
    url = fetch_garmin_url(data_type)
    params = {
        "status": status,
        "start": str(start),
        "limit": str(limit),
        "sortOrder": "asc",
    }

    while True:
        params["start"] = str(start)
        goals_json = api.connectapi(url, params=params)
        if goals_json:
            goals.extend(goals_json)
            start = start + limit
        else:
            break
    return goals


# Body Composition Aggregated, Body Battery
def fetch_body_comp_agg_and_battery(api, data_type, start_date, num_days, params=None):
    response = []
    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        url = f"{fetch_garmin_url(data_type)}"
        params = {"startDate": str(new_date), "endDate": str(new_date)}
        response.append(api.connectapi(url, params=params))
    return response


def fetch_real_data(start_date, end_date, data_type, api):
    """Main function for fetching real data from the Garmin Connect API.
    We parallelize this since making requests to the API is day-by-day,
    and API requests are I/O bound.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param data_type: the type of data to fetch, one of "dates", "steps", "hrs", "brpms"
    :type data_type: str
    :param api: the Garmin Connect API object
    :type api: Garmin
    :return: the data fetched from the API according to the inputs
    :rtype: List
    """

    num_days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days
    display_name = api.profile["displayName"]

    if data_type in ["stats"]:
        return fetch_stats(api, data_type, start_date, num_days)

    elif data_type in ["steps", "hr"]:
        return fetch_steps_and_hr(api, data_type, start_date, num_days)

    elif data_type in ["body_composition"]:
        return fetch_body_composition(api, data_type, start_date, end_date)

    elif data_type in ["blood_pressure", "weigh_ins"]:
        return fetch_blood_pressure_and_weigh_ins(api, data_type, start_date, end_date)

    elif data_type in ["rhr"]:
        return fetch_resting_heart_rate(api, data_type, start_date, end_date)

    elif data_type in ["personal_record", "race_prediction"]:
        return fetch_personal_record_and_race_prediction(api, data_type)

    elif data_type in ["earned_badges", "devices", "device_last_used"]:
        return fetch_badges_and_devices(api, data_type)

    elif data_type in [
        "adhoc_challenges",
        "available_badges",
        "available_badge_challenges",
        "badge_challenges",
        "non_completed_badge_challenges",
        "inprogress_virtual_challenges",
        "activities",
    ]:
        return fetch_challenges_and_activities(api, data_type)

    elif data_type in ["weigh_ins_daily"]:
        return fetch_daily_weigh_ins(api, data_type, start_date, num_days)

    elif data_type in ["hill_score", "endurance_score"]:
        return fetch_scores(api, data_type, start_date, end_date)

    elif data_type in ["activities_date"]:
        return fetch_activities_date(api, start_date, end_date)

    elif data_type in ["sleep"]:
        return fetch_sleep(api, data_type, start_date, num_days)

    elif data_type in ["max_metrics", "daily_steps"]:
        return fetch_max_metrics_and_daily_steps(api, data_type, start_date, num_days)

    elif data_type in ["active_goals", "future_goals", "past_goals"]:
        return fetch_goals(api, data_type, data_type.split("_")[0])

    elif data_type in ["body_composition_aggregated", "body_battery"]:
        return fetch_body_comp_agg_and_battery(api, data_type, start_date, num_days)

    elif data_type in [
        "floors",
        "stress",
        "respiration",
        "spo2",
        "hydration",
        "hrv",
        "training_status",
        "training_readiness",
        "activities_fordate_aggregated",
        "day_stress_aggregated",
    ]:
        return fetch_aggregated_data(api, data_type, start_date, num_days)

    elif data_type == "device_settings":
        response = []
        devices = api.connectapi(fetch_garmin_url("devices"))
        for device in devices:
            device_id = device["deviceId"]
            url = f"{fetch_garmin_url(data_type)}/{device_id}"
            device_settings = api.connectapi(url)
            response.append(device_settings)
        return response

    elif data_type == "device_alarms":
        alarms = []
        devices = api.connectapi(fetch_garmin_url("devices"))
        for device in devices:
            settings_data_type = "device_settings"
            device_id = device["deviceId"]
            device_settings = api.connectapi(
                f"{fetch_garmin_url(settings_data_type)}/{device_id}"
            )
            device_alarms = device_settings["alarms"]
            if device_alarms is not None:
                alarms += device_alarms
        return alarms

    elif data_type == "stats_and_body_aggregated":
        response = []
        stats_data_type = "stats"
        body_data_type = "body_composition"
        stats_url = f"{fetch_garmin_url(stats_data_type)}/{display_name}"
        body_url = f"{fetch_garmin_url(body_data_type)}"
        for i in tqdm(range(num_days)):
            new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)

            body_params = {"startDate": str(new_date), "endDate": str(new_date)}
            body_response = api.connectapi(body_url, params=body_params)

            stats_params = {"calendarDate": str(new_date.date())}
            stats_response = api.connectapi(stats_url, params=stats_params)
            comb_response = {
                "stats": stats_response,
                "body_composition": body_response["totalAverage"],
            }
            response.append(comb_response)
        return response
    elif data_type == "dates":
        return [
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            for i in tqdm(range(num_days))
        ]

    return None
