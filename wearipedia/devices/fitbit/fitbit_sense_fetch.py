from datetime import datetime, timedelta

import requests

__all__ = ["fetch_real_data"]


def call_API(url: str, access_token: str, call: str = "GET"):
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.request(call, url=url, headers=headers)
    # Handle specific HTTP status codes
    if response.status_code != 200:
        error_msg = f"{response.status_code}"
        try:
            error_detail = response.json()
            if isinstance(error_detail, dict):
                error_msg = f"{error_msg} - {error_detail}"
        except:
            pass

        raise Exception("Request failed with error: " + error_msg)
    return response.json()


def fetch_real_data(data_type, access_token, start_date=None, end_date=None):
    """Main function for fetching real data from the Fitbit API.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param data_type: the type of data to fetch, one of "sleep", "steps","minutesVeryActive", "minutesLightlyActive", "minutesFairlyActive", "distance", "minutesSedentary", "heart_rate_day", "hrv", "distance_day", "breath_rate"
    :type data_type: str
    :param access_token: access token for the API
    :type api: str
    :return: the data fetched from the API according to the inputs
    :rtype: List
    """
    categories = {
        "sleep": {
            "url": f"https://api.fitbit.com/1.2/user/-/sleep/date/{start_date}/{end_date}.json"
        },
        "steps": {
            "url": f"https://api.fitbit.com/1/user/-/activities/steps/date/{start_date}/{end_date}.json"
        },
        "minutesVeryActive": {
            "url": f"https://api.fitbit.com/1/user/-/activities/minutesVeryActive/date/{start_date}/{end_date}.json"
        },
        "minutesFairlyActive": {
            "url": f"https://api.fitbit.com/1/user/-/activities/minutesFairlyActive/date/{start_date}/{end_date}.json"
        },
        "minutesLightlyActive": {
            "url": f"https://api.fitbit.com/1/user/-/activities/minutesLightlyActive/date/{start_date}/{end_date}.json"
        },
        "distance": {
            "url": f"https://api.fitbit.com/1/user/-/activities/distance/date/{start_date}/{end_date}.json"
        },
        "minutesSedentary": {
            "url": f"https://api.fitbit.com/1/user/-/activities/minutesSedentary/date/{start_date}/{end_date}.json"
        },
        "heart_rate_day": {
            "url": f"https://api.fitbit.com/1/user/-/activities/heart/date/{start_date}/{end_date}/1d.json"
        },
        "hrv": {
            "url": f"https://api.fitbit.com/1/user/-/hrv/date/{start_date}/{end_date}.json"
        },
        "distance_day": {
            "url": f"https://api.fitbit.com/1/user/-/activities/distance/date/{start_date}/{end_date}/1d.json"
        },
    }

    arr = []

    if "intraday" in data_type:
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        # Iterate through dates until end date is reached
        while current_date <= end:
            current_date
            current_date += timedelta(days=1)
            current_date_str = current_date.strftime("%Y-%m-%d")
            intraday_categories = {
                "intraday_breath_rate": {
                    "url": f"https://api.fitbit.com/1/user/-/br/date/{current_date_str}/all.json"
                },
                "intraday_active_zone_minute": {
                    "url": f"https://api.fitbit.com/1/user/-/activities/active-zone-minutes/date/{current_date_str}/1d/1min.json"
                },
                "intraday_activity": {
                    "url": f"https://api.fitbit.com/1/user/-/activities/steps/date/{current_date_str}/1d/1min.json"
                },
                "intraday_heart_rate": {
                    "url": f"https://api.fitbit.com/1/user/-/activities/heart/date/{current_date_str}/1d/1sec.json"
                },
                "intraday_hrv": {
                    "url": f"https://api.fitbit.com/1/user/-/hrv/date/{current_date_str}/all.json"
                },
                "intraday_spo2": {
                    "url": f"https://api.fitbit.com/1/user/-/spo2/date/{current_date_str}/all.json"
                },
            }
            response = call_API(
                url=intraday_categories[data_type]["url"], access_token=access_token
            )
            arr.append(response)
    else:
        response = call_API(url=categories[data_type]["url"], access_token=access_token)
    arr.append(response)

    return arr
