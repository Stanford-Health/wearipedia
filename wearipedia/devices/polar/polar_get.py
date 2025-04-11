import datetime
import io
import re
import zipfile

import numpy as np
import pandas as pd
import requests


def fetch_real_data(
    start_date, end_date, data_type, session, post, elite_hrv_session=None
):
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
    :param elite_hrv_session: current login session to Elite HRV, pre authenticated, defaults to None
    :type elite_hrv_session: requests.sessions.Session, optional
    :return: a dictionary with keys the training session dates and values a dictionary with keys heart_rates, calories, and minutes
    :rtype: Dict[str: Dict[str: list, str: int, str: int]]
    """

    # declare some new functions to help us parse the data
    result = {}
    func = lambda x: list(str(x).split())[0]

    if data_type == "sessions":

        headers = {
            "x-requested-with": "XMLHttpRequest",
        }

        json_data = {
            "userId": None,
            "fromDate": start_date,
            "toDate": end_date,
        }

        # using regular expressions, we can search for the userId in the session response
        target = re.search("AppGlobal.init((.*))", post.text)
        if target is None:
            return {}
        target = str(target.group(1)).split('"')
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

        for sesh in trainhist[::-1]:
            train_id = sesh["id"]
            date = list(sesh["startDate"].split())[0]
            r = session.get(
                f"https://flow.polar.com/api/export/training/csv/{str(train_id)}"
            )
            raw = pd.read_csv(io.StringIO(r.text), sep=",", engine="python")

            # the columns processed by panda are named wrong
            # that is, the time and bpm are named "Sport" and "Date" respectively
            raw = raw.iloc[2:, :]
            raw = raw[["Sport", "Date"]]
            raw.columns = ["time", "bpm"]

            # add the date and time stamp of data point
            mapping = lambda x: np.datetime64(f"{date} {x}")
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
    elif data_type == "rr":

        # set the session data
        session_id = elite_hrv_session["sessionId"]
        user_id = elite_hrv_session["user"]["id"]

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://dashboard.elitehrv.com",
            "Referer": "https://dashboard.elitehrv.com/",
        }

        data = f"userId={user_id}&startDate={start_date}%3A01%3A52.615Z&endDate={end_date}T23%3A01%3A52.615Z&version=*&locale=en-us&language=en&sessionId={session_id}"

        # get the output raw text file
        response = requests.post(
            "https://app.elitehrv.com/application/reading/exportUser",
            headers=headers,
            data=data,
        )

        # elitehrv returns empty byte stream if no data is available
        if response.content == b"":
            return {}

        z = zipfile.ZipFile(io.BytesIO(response.content))

        # for each of the session data, read the file
        s = None
        for f in z.namelist():
            if f.endswith(".txt") and f != "!About This Export.txt":
                dte = (f.split("/")[1]).split(".")[0]  # get the date from the file name
                s = z.read(f)

                # convert to bytes then read raw text as csv
                bstring = str(s, "utf-8")
                data = io.StringIO(bstring)
                df = pd.read_csv(data)

                # rename the columns correctly
                df = df.rename(columns={str(df.columns[0]): "rr"})

                # create a list of timestamps
                cur_time = datetime.datetime.strptime("00:00:00.0", "%H:%M:%S.%f")
                date_list = []

                for interval in list(df["rr"]):
                    date_list.append(cur_time)
                    cur_time = cur_time + datetime.timedelta(milliseconds=interval)

                # complete dataframe by setting index to the time
                df["time"] = date_list
                df = df.set_index("time")

                # add the data to the result dictionary
                result[dte] = {
                    "rr": list(df["rr"]),
                    "time": list(df.index),
                }

        return result
