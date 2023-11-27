import requests

__all__ = ["fetch_real_data"]


def call_API(access_token: str, url: str, call: str = "GET"):
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.request(call, url=url, headers=headers).json()


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
    }

    arr = []

    response = call_API(url=categories[data_type]["url"], access_token=access_token)
    arr.append(response)

    return arr
