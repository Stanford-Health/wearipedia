import requests as rq

__all__ = ["fetch_real_data"]


def fetch_real_data(data_type, access_token, start_date, end_date):
    """Main function for fetching real data from the Fitbit API.
    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param single_date: the day data is being requested from represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param data_type: the type of data to fetch, one of "sleep", "steps","minutesVeryActive", "minutesLightlyActive", "minutesFairlyActive", "distance", "minutesSedentary"
    :type data_type: str
    :param access_token: access token for the API
    :type api: str
    :return: the data fetched from the API according to the inputs
    :rtype: List
    """
    # # From intercepting the API requests, we were able to retrieve the following requests

    # dictionary to aggregate the data in
    data = dict()

    ## Getting user data
    saver = rq.post(
        url="https://api.coros.com/coros/data/userExtend/query?accessToken=YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9"
    )
    data["user_data"] = saver.text

    # Getting steps data
    j = {
        "startTime": start_date,
        "endTime": end_date,
        "accessToken": "YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        "dataType": [3, 16],
        "dataVersion": 1,
        "statisticType": 1,
    }

    saver = rq.post(
        url="https://api.coros.com/coros/data/statistic/daily?accessToken=YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        json=j,
    )
    data["steps"] = saver.text

    # Getting exercise tiem data
    j = {
        "startTime": start_date,
        "endTime": end_date,
        "accessToken": "YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        "dataType": [2, 15],
        "dataVersion": 1,
        "statisticType": 1,
    }

    saver = rq.post(
        url="https://api.coros.com/coros/data/statistic/daily?accessToken=YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        json=j,
    )
    data["exercise_time"] = saver.text

    # Getting Heart_rate data
    j = {
        "startTime": start_date,
        "endTime": end_date,
        "accessToken": "YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        "dataType": [4, 17],
        "dataVersion": 1,
        "statisticType": 1,
    }

    saver = rq.post(
        url="https://api.coros.com/coros/data/statistic/daily?accessToken=YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        json=j,
    )
    data["heart_rate"] = saver.text

    # Getting sports data
    j = {
        "accessToken": "YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        "month": start_date[0:7],
        "size": 20,
    }

    saver = rq.post(
        url="https://api.coros.com/coros/data/sport/query?accessToken=YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        json=j,
    )
    data["sports"] = saver.text

    # Getting sleep data

    j = {
        "startTime": 20221108,
        "endTime": 20230206,
        "accessToken": "YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        "dataType": [5, 13],
        "dataVersion": 1,
        "statisticType": 1,
    }

    saver = rq.post(
        url="https://api.coros.com/coros/data/statistic/daily?accessToken=YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        json=j,
    )
    data["sleep"] = saver.text

    j = {
        "startTime": 20221108,
        "endTime": 20230206,
        "accessToken": "YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        "dataType": [1, 14],
        "dataVersion": 1,
        "statisticType": 1,
    }
    saver = rq.post(
        url="https://api.coros.com/coros/data/statistic/daily?accessToken=YJ1VVZ3EUCC7Z9OWLCFDN2L0P7EET2P9",
        json=j,
    )
    data["active_energy"] = saver.text

    return data
