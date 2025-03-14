import json
from datetime import date, datetime, timedelta

import requests

year, month, day = 0, 1, 2

default_time_bucket = 86400000


def milliconvert(d):
    return int(
        datetime(
            int(d.split("-")[year]), int(d.split("-")[month]), int(d.split("-")[day])
        ).timestamp()
        * 1000
    )


def transform_response_bucket(data):
    """
    Convert response structure for real data: List[Dict] to List[List[Dict]]
    Transformation should match expected response for Google Fit notebook
    """
    output = []
    for row in data:
        if type(row) is dict:
            output.append([row])
        elif type(row) is list:
            output.append(row)
    return output


def fetch_real_data(
    self, start_date, end_date, data_type, time_bucket=default_time_bucket
):

    # URL to access all of participant's activities.
    api_url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

    # Access token that enables us to access the user's data using google's API
    g_access_token = self.access_token

    # Header that sends the Access Token in the GET request
    headers = {
        "Authorization": f"Bearer {g_access_token}",
        "Content-Type": "application/json;encoding=utf-8",
    }

    # The data type names and data source ids are used to specify the type of data we want to access
    # from the API.

    datatypenames = {
        "steps": "com.google.step_count.delta",
        "heart_rate": "com.google.heart_rate.bpm",
        "height": "com.google.height",
        "weight": "com.google.weight",
        "speed": "com.google.speed",
        "heart_minutes": "com.google.heart_minutes",
        "calories_expended": "com.google.calories.expended",
        "sleep": "com.google.sleep.segment",
        "blood_pressure": "com.google.blood_pressure",
        "blood_glucose": "com.google.blood_glucose",
        "activity_minutes": "com.google.activity_minutes",
        "distance": "com.google.distance.delta",
        "oxygen_saturation": "com.google.oxygen_saturation",
        "body_temperature": "com.google.body.temperature",
        "menstruation": "com.google.menstruation",
    }

    # The data source ids are used to specify the type of data we want to access from the API.
    datasourceids = {
        "steps": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps",
        "heart_rate": "derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm",
        "height": "derived:com.google.height:com.google.android.gms:merge_height",
        "weight": "derived:com.google.weight:com.google.android.gms:merge_weight",
        "speed": "derived:com.google.speed:com.google.android.gms:merge_speed",
        "heart_minutes": "derived:com.google.heart_minutes:com.google.android.gms:merge_heart_minutes",
        "calories_expended": "derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended",
        "sleep": "derived:com.google.sleep.segment:com.google.android.gms:merged",
        "blood_pressure": "derived:com.google.blood_pressure:com.google.android.gms:merged",
        "blood_glucose": "derived:com.google.blood_glucose:com.google.android.gms:merged",
        "activity_minutes": "derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes",
        "distance": "derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta",
        "oxygen_saturation": "derived:com.google.oxygen_saturation:com.google.android.gms:merged",
        "body_temperature": "derived:com.google.body.temperature:com.google.android.gms:merged",
        "menstruation": "derived:com.google.menstruation:com.google.android.gms:merged",
    }

    # The body of the GET request that specifies the data type, data source, start date, and end date
    body = {
        "aggregateBy": [
            {
                "dataTypeName": datatypenames[data_type],
                "dataSourceId": datasourceids[data_type],
            }
        ],
        "bucketByTime": {"durationMillis": time_bucket},
        "startTimeMillis": milliconvert(start_date),
        "endTimeMillis": milliconvert(end_date),
    }

    # GET request to get all your activities from the API
    response = requests.post(api_url, data=json.dumps(body), headers=headers)

    # If there is an error in the response, raise an exception
    if "error" in response.json():
        raise Exception(f"Error in response: {response.json()['error']}")

    # Return the bucket of data
    return transform_response_bucket(response.json()["bucket"])
