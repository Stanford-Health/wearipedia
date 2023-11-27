from typing import List

import requests as rq

__all__ = ["fetch_real_data"]


def fetch_real_data(data_type, access_token, start_date, end_date):
    """Main function for fetching real data from the Fitbit API.
    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param data_type: the type of data to fetch, one of "sleep", "steps","minutesVeryActive", "minutesLightlyActive", "minutesFairlyActive", "distance", "minutesSedentary"
    :type data_type: str
    :param access_token: access token for the API
    :type access_token: str
    :return: the data fetched from the API according to the inputs
    :rtype: List
    """
    # From intercepting the API requests, we were able to retrieve the following requests

    # dictionary to aggregate the data in
    data = dict()

    ## Getting user data
    response = rq.post(
        url=f"https://api.coros.com/coros/data/userExtend/query?accessToken={access_token}"
    )
    data["user_data"] = response.text

    # Getting steps data
    j = {
        "startTime": start_date,
        "endTime": end_date,
        "accessToken": access_token,
        "dataType": [3, 16],
        "dataVersion": 1,
        "statisticType": 1,
    }

    response = rq.post(
        url=f"https://api.coros.com/coros/data/statistic/daily?accessToken={access_token}",
        json=j,
    )
    data["steps"] = response.text

    # Getting exercise time data
    j = {
        "startTime": start_date,
        "endTime": end_date,
        "accessToken": access_token,
        "dataType": [2, 15],
        "dataVersion": 1,
        "statisticType": 1,
    }

    response = rq.post(
        url=f"https://api.coros.com/coros/data/statistic/daily?accessToken={access_token}",
        json=j,
    )
    data["exercise_time"] = response.text

    # Getting Heart_rate data
    j = {
        "startTime": start_date,
        "endTime": end_date,
        "accessToken": access_token,
        "dataType": [4, 17],
        "dataVersion": 1,
        "statisticType": 1,
    }

    response = rq.post(
        url=f"https://api.coros.com/coros/data/statistic/daily?accessToken={access_token}",
        json=j,
    )
    data["heart_rate"] = response.text

    # Getting sports data
    j = {
        "accessToken": access_token,
        "month": start_date[0:7],
        "size": 20,
    }

    response = rq.post(
        url=f"https://api.coros.com/coros/data/sport/query?accessToken={access_token}",
        json=j,
    )
    data["sports"] = response.text

    # Getting sleep data

    j = {
        "startTime": start_date,
        "endTime": end_date,
        "accessToken": access_token,
        "dataType": [5, 13],
        "dataVersion": 1,
        "statisticType": 1,
    }

    response = rq.post(
        url=f"https://api.coros.com/coros/data/statistic/daily?accessToken={access_token}",
        json=j,
    )
    data["sleep"] = response.text

    j = {
        "startTime": start_date,
        "endTime": end_date,
        "accessToken": access_token,
        "dataType": [1, 14],
        "dataVersion": 1,
        "statisticType": 1,
    }
    response = rq.post(
        url=f"https://api.coros.com/coros/data/statistic/daily?accessToken={access_token}",
        json=j,
    )
    data["active_energy"] = response.text

    return data
