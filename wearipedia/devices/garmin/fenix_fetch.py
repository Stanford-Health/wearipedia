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
        "user_summary": "/usersummary-service/usersummary/daily",
        "body_composition": "/weight-service",
        "body_composition_aggregated": "/weight-service",
        "steps": "/wellness-service/wellness/dailySummaryChart",
        "hr": "/wellness-service/wellness/dailyHeartRate",
        "training_readiness": "/metrics-service/metrics/trainingreadiness",
        "blood_pressure": "/bloodpressure-service/bloodpressure/range",
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
        "activities": "/activitylist-service/activities/search/activities",
        "devices": "/device-service/deviceregistration/devices",
        "device_settings": "/device-service/deviceservice/device-info/settings",
        "active_goals": "/goal-service/goal/goals",
        "future_goals": "/goal-service/goal/goals",
        "past_goals": "/goal-service/goal/goals",
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

    # Group 1: Daily Data Types
    first_data_types = ["stats", "user_summary"]
    if data_type in first_data_types:
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        response = []
        for i in tqdm(range(num_days)):
            new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            params = {"calendarDate": str(new_date.date())}
            response.append(api.connectapi(url, params=params))
        return response

    # Group 2: Daily Data Types
    second_data_types = ["steps", "hr"]
    if data_type in second_data_types:
        url = f"{fetch_garmin_url(data_type)}/{display_name}"
        response = []
        for i in tqdm(range(num_days)):
            new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            params = {"date": str(new_date.date())}
            response.append(api.connectapi(url, params=params))
        return response

    # Group 3: Daily Data Types
    third_data_types = [
        "floors",
        "stress",
        "respiration",
        "spo2",
        "hydration",
        "hrv",
        "training_status",
        "training_readiness",
    ]
    if data_type in third_data_types:
        response = []
        for i in tqdm(range(num_days)):
            new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            url = f"{fetch_garmin_url(data_type)}/{new_date.date()}"
            response.append(api.connectapi(url))
        return response

    # Group 4: Single Fetch Data Types
    single_fetch_types = [
        "body_composition",
        "blood_pressure",
        "rhr",
        "personal_record",
        "earned_badges",
        "device_settings",
        "weigh_ins",
        "hill_score",
        "endurance_score",
        "virtual_challenges",
        "weigh_ins_daily",
        "activities",
    ]
    if data_type in single_fetch_types:
        response = None
        if data_type == "body_composition":
            url = f"{fetch_garmin_url(data_type)}/weight/dateRange"
            params = {"startDate": str(start_date), "endDate": str(end_date)}
            response = api.connectapi(url, params=params)
        elif data_type == "blood_pressure":
            url = f"{fetch_garmin_url(data_type)}/{start_date}/{end_date}"
            params = {"includeAll": True}
            response = api.connectapi(url, params=params)
        elif data_type == "rhr":
            url = f"{fetch_garmin_url(data_type)}/{display_name}"
            params = {
                "fromDate": str(start_date),
                "untilDate": str(end_date),
                "metricId": 60,
            }
            response = api.connectapi(url, params=params)
        elif data_type == "personal_record":
            url = f"{fetch_garmin_url(data_type)}/{display_name}"
            response = api.connectapi(url)
        elif data_type == "earned_badges":
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
        elif data_type == "weigh_ins":
            url = f"{fetch_garmin_url(data_type)}/{start_date}/{end_date}"
            params = {"includeAll": True}
            response = api.connectapi(url, params=params)
        elif data_type == "weigh_ins_daily":
            response = []
            for i in tqdm(range(num_days)):
                new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
                url = f"{fetch_garmin_url(data_type)}/{new_date.date()}"
                params = {"includeAll": True}
                response.append(api.connectapi(url, params=params))
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
        elif data_type == "activities":
            url = fetch_garmin_url(data_type)
            params = {"start": str(1), "limit": str(100)}
            response = api.connectapi(url, params=params)

        return response

    # Group 5: List Fetch Data Types
    list_fetch_types = [
        "dates",
        "sleep",
        "max_metrics",
        "active_goals",
        "future_goals",
        "past_goals",
    ]
    if data_type in list_fetch_types:
        response = []
        if data_type == "sleep":
            url = f"{fetch_garmin_url(data_type)}/{display_name}"
            response = []
            for i in tqdm(range(num_days)):
                new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
                params = {"date": str(new_date.date()), "nonSleepBufferMinutes": 60}
                response.append(api.connectapi(url, params=params))
        elif data_type == "max_metrics":
            response = []
            for i in tqdm(range(num_days)):
                new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
                url = (
                    f"{fetch_garmin_url(data_type)}/{new_date.date()}/{new_date.date()}"
                )
                response.append(api.connectapi(url))
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
        elif data_type == "dates":
            return [
                datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
                for i in tqdm(range(num_days))
            ]

        return response

    # Group 6 - Aggregated Data Types
    aggregated_fetch_types = [
        "body_composition_aggregated",
        "stats_and_body_aggregated",
    ]

    if data_type in aggregated_fetch_types:
        response = []
        if data_type == "body_composition_aggregated":
            # response = []
            for i in tqdm(range(num_days)):
                new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
                url = f"{fetch_garmin_url(data_type)}/weight/dateRange"
                params = {"startDate": str(new_date), "endDate": str(new_date)}
                response.append(api.connectapi(url, params=params))
        elif data_type == "stats_and_body_aggregated":
            stats_data_type = "stats"
            body_data_type = "body_composition"
            stats_url = f"{fetch_garmin_url(stats_data_type)}/{display_name}"
            body_url = f"{fetch_garmin_url(body_data_type)}/weight/dateRange"
            for i in tqdm(range(num_days)):
                new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)

                body_params = {"startDate": str(new_date), "endDate": str(new_date)}
                body_response = api.connectapi(body_url, params=body_params)

                stats_params = {"calendarDate": str(new_date.date())}
                stats_response = api.connectapi(stats_url, params=stats_params)
                comb_response = {"stats": stats_response, "body_composition": body_response["totalAverage"]}
                response.append(comb_response)


        return response



    return None
