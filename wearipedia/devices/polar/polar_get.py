import io
import re

import numpy as np
import pandas as pd
import requests


def fetch_real_data(start_date, end_date, data_type, session, post):
    """Main function for fetching real data from the Polar website.
    Does not use Polar's API, but instead scrapes the website.

    :param start_date: the start date represented as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date represented as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :param data_type: the type of data to fetch, one of "sessions"
    :type data_type: str
    :param session: current login session to the Polar website, pre authenticated
    :type session: requests.sessions.Session
    :param post: response from logging into polar. Contains relevant global variables.
    :type post: requests.models.Response
    :return: a dictionary with keys the training session dates and values a dictionary with keys heart_rates, calories, and minutes
    :rtype: Dict[str: Dict[str: list, str: int, str: int]]
    """

    headers = {
        "x-requested-with": "XMLHttpRequest",
    }

    json_data = {
        "userId": None,
        "fromDate": start_date,
        "toDate": end_date,
    }

    # using regular expressions, we can search for the userId in the session response
    result = re.search("AppGlobal.init((.*))", post.text)
    target = str(result.group(1)).split('"')
    userid = int(target[1])

    # get the actual training session data
    json_data["userId"] = userid

    trainhist = session.post(
        "https://flow.polar.com/api/training/history",
        cookies=session.cookies.get_dict(),
        headers=headers,
        json=json_data,
    )
    trainhist = trainhist.json()

    # this is just to filter unwanted entries (i.e. too short sessions, error in data)
    trainhist = [
        e for e in trainhist if (e["hrAvg"] != None and e["duration"] > 1200000)
    ]

    # declare some new functions to help us parse the data
    result = {}
    func = lambda x: list(str(x).split())[0]

    if data_type == "sessions":
        for sesh in trainhist[::-1]:
            train_id = sesh["id"]
            date = list(sesh["startDate"].split())[0]
            r = session.get(
                "https://flow.polar.com/api/export/training/csv/" + str(train_id)
            )
            raw = pd.read_csv(io.StringIO(r.text), sep=",", engine="python")

            # the columns processed by panda are named wrong
            # that is, the time and bpm are named "Sport" and "Date" respectively
            raw = raw.iloc[2:, :]
            raw = raw[["Sport", "Date"]]
            raw.columns = ["time", "bpm"]

            # add the date and time stamp of data point
            mapping = lambda x: np.datetime64(date + " " + x)
            raw["time"] = raw["time"].apply(mapping)
            raw["bpm"] = pd.to_numeric(raw["bpm"])

            # gets rid of not a number (NaN) entries if monitor loses connection to app
            raw.dropna(inplace=True)

            # add the data to the result dictionary
            result[date] = {
                "heart_rates": list(raw[raw["time"].apply(func) == date]["bpm"]),
                "calories": sesh["calories"],
                "minutes": sesh["duration"] / 60000,
            }

        return result
