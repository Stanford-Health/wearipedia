import requests

__all__ = ["fetch_real_data"]


def call_api_version_2(
    url: str,
    access_token,
    start_date,
    end_date,
    start_date_col,
    end_date_col,
    call: str = "GET",
):
    """
    Second version of the api, the only supported API version as of 1/24/25
    """
    headers = {"Authorization": "Bearer " + access_token}
    params = {start_date_col: start_date, end_date_col: end_date}

    response = requests.request(call, url=url, headers=headers, params=params)

    # Handle specific HTTP status codes
    if response.status_code != 200:
        error_msg = f"{response.status_code}"
        try:
            error_detail = response.json()
            if isinstance(error_detail, dict):
                error_msg = f"{error_msg} - {error_detail.get('detail', '')}"
        except:
            pass

        raise Exception("Request failed with error: " + error_msg)
    return response.json()


def fetch_real_data(data_type, access_token, start_date, end_date):
    """Main function for fetching real data from the Oura Ring API.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :param data_type: the type of data to fetch, one of "Personal Info", "Heart Rate", "Sessions", "Tags", "Workouts", "Daily Sleep", "Daily Activity", "Daily Readiness", "Ideal Bedtime"
    :param access_token: access token for the API
    :return: the data fetched from the API according to the inputs
    :rtype: List
    """

    start_date_col = "start_date"
    end_date_col = "end_date"
    if data_type == "heart_rate":
        endpoint = "https://api.ouraring.com/v2/usercollection/heartrate"
        start_date_col = "start_datetime"
        end_date_col = "end_datetime"
        start_date = start_date + "T00:00:00-23:59"
        end_date = end_date + "T00:00:00-23:59"
    elif data_type == "personal_info":
        endpoint = "https://api.ouraring.com/v2/usercollection/personal_info"
    elif data_type == "session":
        endpoint = "https://api.ouraring.com/v2/usercollection/session"
    elif data_type == "enhanced_tag":
        # Tag is deprecated, and the Oura website recommends transitioning to enhanced_tag
        # (https://cloud.ouraring.com/v2/docs#tag/Tag-Routes)
        endpoint = "https://api.ouraring.com/v2/usercollection/enhanced_tag"
    elif data_type == "workout":
        endpoint = "https://api.ouraring.com/v2/usercollection/workout"
    elif data_type == "daily_activity":
        endpoint = "https://api.ouraring.com/v2/usercollection/daily_activity"
    elif data_type == "daily_sleep":
        endpoint = "https://api.ouraring.com/v2/usercollection/daily_sleep"
    elif data_type == "sleep":
        endpoint = "https://api.ouraring.com/v2/usercollection/sleep"
    elif data_type == "readiness":
        endpoint = "https://api.ouraring.com/v2/usercollection/daily_readiness"
    elif data_type == "ideal_sleep_time":
        endpoint = "https://api.ouraring.com/v2/usercollection/sleep_time"

    response = call_api_version_2(
        endpoint, access_token, start_date, end_date, start_date_col, end_date_col
    )

    if data_type == "personal_info":
        return [response]
    return response["data"]
