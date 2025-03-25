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
        "steps": "/wellness-service/wellness/dailySummaryChart",
        "body_battery": "/wellness-service/wellness/bodyBattery/reports/daily",
        "hr": "/wellness-service/wellness/dailyHeartRate",
        "blood_pressure": "/bloodpressure-service/bloodpressure/range",
        "floors": "/wellness-service/wellness/floorsChartData/daily",
        "rhr": "/userstats-service/wellness/daily",
        "hydration": "/usersummary-service/usersummary/hydration/daily",
        "sleep": "/wellness-service/wellness/dailySleepData",
        "stress": "/wellness-service/wellness/dailyStress",
        "respiration": "/wellness-service/wellness/daily/respiration",
        "spo2": "/wellness-service/wellness/daily/spo2",
        "hrv": "/hrv-service/hrv",
    }
    if data_type in url_dict.keys():
        return url_dict[data_type]
    else:
        return None


# Steps, HR
def fetch_steps_and_hr(api, data_type, start_date, num_days, params=None):
    display_name = api.display_name
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


# Blood Pressure, Weigh Ins
def fetch_blood_pressure_and_weigh_ins(
    api, data_type, start_date, end_date, params=None
):
    url = f"{fetch_garmin_url(data_type)}/{start_date}/{end_date}"
    params = {"includeAll": True}
    return api.connectapi(url, params=params)


# RHR
def fetch_resting_heart_rate(api, data_type, start_date, end_date, params=None):
    display_name = api.display_name
    url = f"{fetch_garmin_url(data_type)}/{display_name}"
    params = {"fromDate": str(start_date), "untilDate": str(end_date), "metricId": 60}
    return api.connectapi(url, params=params)


# Sleep
def fetch_sleep(api, data_type, start_date, num_days, params=None):
    display_name = api.display_name
    response = []
    url = f"{fetch_garmin_url(data_type)}/{display_name}"
    for i in tqdm(range(num_days)):
        new_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        params = {"date": str(new_date.date()), "nonSleepBufferMinutes": 60}
        response.append(api.connectapi(url, params=params))
    return response


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
    display_name = api.display_name

    if data_type in ["steps", "hr"]:
        return fetch_steps_and_hr(api, data_type, start_date, num_days)

    elif data_type in ["blood_pressure", "weigh_ins"]:
        return fetch_blood_pressure_and_weigh_ins(api, data_type, start_date, end_date)

    elif data_type in ["rhr"]:
        return fetch_resting_heart_rate(api, data_type, start_date, end_date)

    elif data_type in ["sleep"]:
        return fetch_sleep(api, data_type, start_date, num_days)

    elif data_type in ["body_battery"]:
        return fetch_body_comp_agg_and_battery(api, data_type, start_date, num_days)

    elif data_type in ["floors", "stress", "respiration", "spo2", "hydration", "hrv"]:
        return fetch_aggregated_data(api, data_type, start_date, num_days)

    elif data_type == "dates":
        return [
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            for i in tqdm(range(num_days))
        ]

    return None
