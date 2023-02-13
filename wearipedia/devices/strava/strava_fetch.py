import time

import numpy as np
import pandas as pd
import requests

PER_PAGE_LIMIT = 200
PAGE_COUNT = 1

# Convert date to timestamp


def dateConvert(date_string):
    return int(time.mktime(time.strptime(date_string, "%Y-%m-%d")))


def fetch_real_data(self, start_date, end_date, data_type):
    # URL to access all of participant's activities.

    activites_url = "https://www.strava.com/api/v3/athlete/activities"

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
