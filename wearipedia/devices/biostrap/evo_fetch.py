import json
from datetime import datetime, timedelta

import requests


def fetch_real_data(access_token, start_date, end_date, data_type):
    print("Fetching real data from Biostrap API...")
    print(f"Start date: {start_date}, End date: {end_date}, Data type: {data_type}")
    BASE_URL = "https://api-beta.biostrap.com/v1/"

    ENDPOINT = ""
    METRIC = ""

    if data_type == "steps":
        ENDPOINT = "step/details"
        METRIC = "Steps"
    elif data_type == "calories":
        ENDPOINT = "calorie/details"
        METRIC = "Active Calories"
    elif data_type in ["bpm", "brpm", "spo2"]:
        ENDPOINT = "biometrics"
        METRIC = data_type
    else:
        raise ValueError(f"Invalid data_type: {data_type}")

    URL = BASE_URL + ENDPOINT
    headers = {"Authorization": f"Bearer {access_token}"}

    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    all_data = {}

    if data_type in ["steps", "calories"]:
        while start_date_obj <= end_date_obj:
            date = start_date_obj.strftime("%Y-%m-%d")
            params = {"date": date, "granularity": "day"}

            response = requests.get(URL, params=params, headers=headers)
            if response.status_code != 200:
                raise Exception(
                    f"Request failed with status code {response.status_code}"
                )

            data = response.json()

            for metric in data["metrics"]:
                if metric["name"] == METRIC:
                    all_data[start_date_obj.strftime("%Y-%m-%d")] = metric["value"]

            # Move to the next day
            start_date_obj += timedelta(days=1)
    else:
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

            for metric in data["data"]:
                timestamp = metric["timestamp"] / 1000  # Convert to seconds
                current_datetime = datetime.fromtimestamp(timestamp)

                # Break the loop if the timestamp is beyond the end date
                if current_datetime > end_date_obj:
                    break

                date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

                # Add data only if the value is not 0
                if (
                    start_date_obj <= current_datetime <= end_date_obj
                    and metric[METRIC] != 0
                ):
                    all_data[date] = metric[METRIC]

            if "next" in data["links"]:
                last_timestamp = data["data"][-1]["timestamp"]
            else:
                break

    return all_data
