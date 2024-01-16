import json
from datetime import datetime, timedelta

import requests


def fetch_real_data(access_token, start_date, end_date, data_type):
    """
    Fetch specified data from the Biostrap API within a given date range.

    This function can retrieve a variety of health-related metrics, such as activities,
    heart rate variability, steps, sleep data, and more. It adapts to different endpoints
    based on the type of data requested and iteratively fetches data to ensure comprehensive retrieval.

    :param access_token: The access token to authenticate requests to the Biostrap API.
    :type access_token: str
    :param start_date: The start date of the range for which data should be retrieved, in "YYYY-MM-DD" format.
    :type start_date: str
    :param end_date: The end date of the range for which data should be retrieved, in "YYYY-MM-DD" format.
    :type end_date: str
    :param data_type: The category of data to fetch. Must be one of the following:
                      "activities", "bpm", "brpm", "hrv", "spo2", "rest_cals", "work_cals", "active_cals",
                      "step_cals", "total_cals", "sleep_session", "sleep_detail", "steps", "distance".
    :type data_type: str

    :return: A dictionary containing the retrieved data. The format varies based on the data_type.
    :rtype: Dict

    :raises ValueError: If an unsupported data_type is provided.
    :raises Exception: If the API request encounters errors.
    """
    print(f"Fetching {data_type} data from Biostrap API...")
    print(f"Start date: {start_date}, End date: {end_date}")

    BASE_URL = "https://api-beta.biostrap.com/v1/"
    headers = {"Authorization": f"Bearer {access_token}"}

    # Convert start and end dates to datetime objects for comparison
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

    all_data = {}

    if data_type in [
        "activities",
        "bpm",
        "brpm",
        "hrv",
        "spo2",
        "steps",
        "distance",
    ]:

        if data_type == "activities":
            ENDPOINT = "activities"
        elif data_type in ["steps", "distance"]:
            ENDPOINT = "steps"
        else:
            ENDPOINT = "biometrics"

        URL = f"{BASE_URL}{ENDPOINT}"

        last_timestamp = 0
        limit = 50  # The max limit allowed by API

        while True:
            params = {"last-timestamp": last_timestamp, "limit": limit}
            response = requests.get(URL, params=params, headers=headers)

            if response.status_code != 200:
                raise Exception(
                    f"Request failed with status code {response.status_code}"
                )

            data = response.json()

            if data_type in ["activities", "steps", "distance"]:
                for activity in data["data"]:

                    timestamp = activity["timestamp"] / 1000  # Convert to seconds
                    current_datetime = datetime.fromtimestamp(timestamp)

                    # Break the loop if the timestamp is beyond the end date
                    if current_datetime > end_date_obj:
                        break

                    # Include data only if the timestamp is within the given date range
                    if start_date_obj <= current_datetime <= end_date_obj:
                        if data_type == "activities":
                            all_data[
                                current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            ] = activity
                        elif data_type == "steps":
                            all_data[
                                current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            ] = activity["steps"]
                        else:
                            all_data[
                                current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            ] = activity["distance"]
            else:
                for biometric in data["data"]:
                    timestamp = biometric["timestamp"] / 1000  # Convert to seconds
                    current_datetime = datetime.fromtimestamp(timestamp)

                    if current_datetime > end_date_obj:
                        break

                    if start_date_obj <= current_datetime <= end_date_obj:
                        key = (
                            current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                            biometric["tz_offset_mins"],
                        )
                        all_data[key] = biometric[data_type]

            if "next" in data["links"]:
                last_timestamp = data["data"][-1]["timestamp"]
            else:
                break

        return all_data

    elif data_type in [
        "rest_cals",
        "work_cals",
        "active_cals",
        "step_cals",
        "total_cals",
    ]:

        metric_mapping = {
            "rest_cals": "Resting Calories",
            "work_cals": "Workout Calories",
            "active_cals": "Active Calories",
            "step_cals": "Step Calories",
            "total_cals": "Total Calories",
        }

        URL = f"{BASE_URL}calorie/details"

        while start_date_obj <= end_date_obj:

            end_date_for_first_query = start_date_obj + timedelta(days=29)
            if end_date_for_first_query > end_date_obj:
                end_date_for_first_query = end_date_obj

            response = requests.get(
                URL,
                params={
                    "date": end_date_for_first_query.strftime("%Y-%m-%d"),
                    "granularity": "month",
                },
                headers=headers,
            )

            if response.status_code != 200:
                raise Exception(
                    f"Request failed with status code {response.status_code}"
                )

            data = response.json()

            for metric in data["metrics"]:
                if metric["type"] == metric_mapping[data_type]:
                    for timeseries_data in metric["timeseries"]:
                        date_str = timeseries_data["date"]
                        if (
                            start_date_obj
                            <= datetime.strptime(date_str, "%Y-%m-%d")
                            <= end_date_for_first_query
                        ):
                            all_data[date_str] = timeseries_data["value"]
                    break
            start_date_obj = end_date_for_first_query + timedelta(days=1)

        return all_data

    elif data_type in ["sleep_session", "sleep_detail"]:

        if data_type == "sleep_session":
            ENDPOINT = "sleep"
        else:
            ENDPOINT = "sleep/details/day"

        URL = f"{BASE_URL}{ENDPOINT}"

        # We'll loop through each date between the start_date_obj and end_date_obj (inclusive)
        current_date = start_date_obj
        while current_date <= end_date_obj:
            # For each date, we'll fetch the relevant data
            params = {"date": current_date.strftime("%Y-%m-%d")}
            response = requests.get(URL, params=params, headers=headers)

            # If empty response, move to the next date
            if response.status_code == 204:
                current_date += timedelta(days=1)
                continue

            data = response.json()

            # Check for successful response
            if response.status_code != 200:
                raise Exception(
                    f"Request failed for date {current_date.strftime('%Y-%m-%d')} with status code {response.status_code}"
                )

            # Check if the data exists in the response
            if data_type == "sleep_session" and "data" in data and data["data"]:
                all_data[current_date.strftime("%Y-%m-%d")] = data["data"]
            elif data_type == "sleep_detail" and data:
                all_data[current_date.strftime("%Y-%m-%d")] = data

            # Move to the next date
            current_date += timedelta(days=1)

        return all_data

    else:
        raise ValueError(f"Invalid data_type: {data_type}")
