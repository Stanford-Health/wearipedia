import os
from datetime import datetime, timedelta
from threading import Lock, Thread

__all__ = ["fetch_real_data"]


def fetch_garmin_url(data_type):

    url_dict = {
        "stats": "/usersummary-service/usersummary/daily",
        "user_summary": "/usersummary-service/usersummary/daily",
        "body_composition": "/weight-service",
        "steps": "/wellness-service/wellness/dailySummaryChart",
        "hr": "/wellness-service/wellness/dailyHeartRate",
        "training_readiness": "/metrics-service/metrics/trainingreadiness",
        "body_battery": "/wellness-service/wellness/bodyBattery/reports/daily",
        "blood_pressure": "/bloodpressure-service/bloodpressure/range",
        "daily_steps": "/usersummary-service/stats/steps/daily",
        "floors": "/wellness-service/wellness/floorsChartData/daily",
        "training_status": "/metrics-service/metrics/trainingstatus/aggregated",
        "rhr": "/userstats-service/wellness/daily",
        "hydration": "/usersummary-service/usersummary/hydration/daily",
        "sleep": "/wellness-service/wellness/dailySleepData",
        "stress": "/wellness-service/wellness/dailyStress",
        "respiration": "/wellness-service/wellness/daily/respiration",
        "spo2": "/wellness-service/wellness/daily/spo2",
        "max_metrics": "/metrics-service/metrics/maxmet/daily",
        "personal_record": "/personalrecord-service/personalrecord/prs",
        "earned_badges": "/badge-service/badge/earned",
        "adhoc_challenges": "/adhocchallenge-service/adHocChallenge/historical",
        "avail_badge_challenges": "/badgechallenge-service/badgeChallenge/available",
        "activities": "/activitylist-service/activities/search/activities",
        "devices": "/device-service/deviceregistration/devices",
        "device_settings": "/device-service/deviceservice/device-info/settings",
        "active_goals": "/goal-service/goal/goals",
        "future_goals": "/goal-service/goal/goals",
        "past_goals": "/goal-service/goal/goals",
        "alarms": "/device-service/deviceservice/device-info/settings",
        "hrv": "/hrv-service/hrv",
        "weigh_ins": "/weight-service/weight/range",
        "weigh_ins_daily": "/weight-service/weight/dayview",
        "hill_score": "/metrics-service/metrics/hillscore",
        "endurance_score": "/metrics-service/metrics/endurancescore",
        "virtual_challenges": "/badgechallenge-service/virtualChallenge/inProgress",
    }
    if data_type in url_dict.keys():
        return url_dict[data_type]
    else:
        return None

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
    full_name = api.profile['fullName']

    if data_type == "stats":
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        params = {"calendarDate": str(end_date)}
        response = api.connectapi(url, params=params)

    elif data_type == "user_summary":
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        params = {"calendarDate": str(end_date)}
        response = api.connectapi(url, params=params)

    elif data_type == "body_composition":
        url = f"{fetch_garmin_url(data_type)}/weight/dateRange"
        params = {"startDate": str(start_date), "endDate": str(end_date)}
        response = api.connectapi(url, params=params)

    elif data_type == "steps":
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        params = {"date": str(end_date)}
        response = api.connectapi(url, params=params)

    elif data_type == "hr":
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        params = {"date": str(end_date)}
        response = api.connectapi(url, params=params)

    elif data_type == "training_readiness":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "body_battery":
        url = fetch_garmin_url(data_type)
        params = {"startDate": str(start_date), "endDate": str(end_date)}
        response = api.connectapi(url, params=params)

    elif data_type == "blood_pressure":
        url = f"{fetch_garmin_url(data_type)}/{start_date}/{end_date}"
        params = {"includeAll": True}
        response = api.connectapi(url, params=params)

    elif data_type == "daily_steps":
        url = f"{fetch_garmin_url(data_type)}/{start_date}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "floors":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "training_status":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "rhr":
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        params = {
            "fromDate": str(start_date),
            "untilDate": str(end_date),
            "metricId": 60,
        }
        response = api.connectapi(url, params=params)

    elif data_type == "hydration":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "sleep":
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        params = {"date": str(end_date), "nonSleepBufferMinutes": 60}
        response = api.connectapi(url, params=params)

    elif data_type == "stress":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "respiration":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "spo2":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "max_metrics":
        url = f"{fetch_garmin_url(data_type)}/{end_date}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "personal_record":
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        response = api.connectapi(url)

    elif data_type == "earned_badges":
        url = fetch_garmin_url(data_type)
        response = api.connectapi(url)

    elif data_type == "adhoc_challenges":
        url = fetch_garmin_url(data_type)
        params = {"start": str(1), "limit": str(100)}
        response = api.connectapi(url, params=params)

    elif data_type == "avail_badge_challenges":
        url = fetch_garmin_url(data_type)
        params = {"start": str(1), "limit": str(1)}
        response = api.connectapi(url, params=params)

    elif data_type == "activities":
        url = fetch_garmin_url(data_type)
        params = {"start": str(1), "limit": str(100)}
        response = api.connectapi(url, params=params)

    elif data_type == "devices":
        url = fetch_garmin_url(data_type)
        response = api.connectapi(url)

    elif data_type == "device_settings":
        response = []
        devices = api.connectapi(fetch_garmin_url("devices"))
        for device in devices:
            device_id = device["deviceId"]
            url = f"{fetch_garmin_url(data_type)}/{device_id}"
            device_settings = api.connectapi(url)
            response.append(device_settings)


    elif data_type == "active_goals":
        start = 1
        limit = 30
        status = "active"

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
        response = goals

    elif data_type == "future_goals":
        start = 1
        limit = 30
        status = "future"

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
        response = goals

    elif data_type == "past_goals":
        start = 1
        limit = 30
        status = "past"

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
        response = goals

    elif data_type == "alarms":

        alarms=[]
        devices = api.connectapi(fetch_garmin_url("devices"))
        for device in devices:
            device_id = device["deviceId"]
            url = f"{fetch_garmin_url(data_type)}/{device_id}"
            device_settings = api.connectapi(url)
            device_alarms = device_settings["alarms"]
            if device_alarms is not None:
                alarms += device_alarms
        response = alarms

    elif data_type == "hrv":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        response = api.connectapi(url)

    elif data_type == "weigh_ins":
        url = f"{fetch_garmin_url(data_type)}/{start_date}/{end_date}"
        params = {"includeAll": True}
        response = api.connectapi(url, params=params)

    elif data_type == "weigh_ins_daily":
        url = f"{fetch_garmin_url(data_type)}/{end_date}"
        params = {"includeAll": True}
        response = api.connectapi(url, params=params)

    elif data_type == "hill_score":
        url = f"{fetch_garmin_url(data_type)}/stats"
        params = {
            "startDate": str(start_date),
            "endDate": str(end_date),
            "aggregation": "daily",
        }
        response = api.connectapi(url, params=params)

    elif data_type == "endurance_score":
        url = f"{fetch_garmin_url(data_type)}/stats"
        params = {
            "startDate": str(start_date),
            "endDate": str(end_date),
            "aggregation": "weekly",
        }
        response = api.connectapi(url, params=params)

    elif data_type == "virtual_challenges":
        url = fetch_garmin_url(data_type)
        params = {"start": str(start_date), "limit": str(end_date)}
        response = api.connectapi(url, params=params)


    return response
