import time

import numpy as np
import pandas as pd
import requests

PER_PAGE_LIMIT = 200
PAGE_COUNT = 1

# Convert date to timestamp


def dateConvert(date_string):
    """
    Converts a date string into a timestamp.

    :param date_string: The date string in the format "YYYY-MM-DD".
    :type date_string: str

    :return timestamp: The timestamp corresponding to the input date string.
    :rtype: int
    """
    return int(time.mktime(time.strptime(date_string, "%Y-%m-%d")))


def fetch_real_data(self, start_date, end_date, data_type, id=""):
    """
    Fetches real data from the Strava API based on the provided parameters.

    :param start_date: The start date for the data generation in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date for the data generation in the format "YYYY-MM-DD".
    :type end_date: str
    :param data_type: The type of data to fetch, one of "distance", "moving_time", "elapsed_time", "total_elevation_gain", "average_speed", "map_summary_polyline", "heartrate".
    :type data_type: str
    :param id: The id of the activity to fetch data for.
    :type id: int, optional

    :return: The data fetched from the API according to the inputs.
    :rtype: list
    """
    # URL to access all of participant's activities.

    stream_data = set(["heartrate"])

    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    if data_type in stream_data:

        if id == "":
            raise ValueError("id must be provided for stream data")

        # URL for the API request
        activities_url = f"https://www.strava.com/api/v3/activities/{id}/streams"
        # Header that sends the Access Token in the GET request
        headers = {"Authorization": f"Bearer {self.access_token}"}
        # Parameters for the GET request
        params = {"keys": [data_type], "key_by_type": True}

        # GET request to get activity streams from the API
        response = requests.get(activities_url, headers=headers, params=params).json()

        if response is None:
            return []
        else:
            return [response]

    # Header that sends the Access Token in the GET request
    header = {"Authorization": "Bearer " + self.access_token}
    param = {
        "per_page": PER_PAGE_LIMIT,
        "page": PAGE_COUNT,
        "before": dateConvert(end_date),
        "after": dateConvert(start_date),
    }

    # GET request to get all your activities from the API
    my_dataset = requests.get(activites_url, headers=header, params=param).json()

    # Normalize the json data
    df_strava = pd.json_normalize(my_dataset)

    # map.summary_polyline is not a valid column name so we need to rename it
    if data_type == "map_summary_polyline":
        data_type = "map.summary_polyline"

    # Filter the data
    filtered = df_strava.get(["name", "id", "start_date", data_type]).to_dict("index")

    # Convert the dictionary to array
    arr = []

    # Loop through the dictionary and append the values to the array
    for i in filtered:
        arr.append(filtered[i])

    return arr
