import io
import re

import pandas as pd
import requests

# This is the class that will be used to fetch data from Polar Flow


def fetch_real_data(
    session, uid, email, password, start_date, end_date, data_type, training_id=None
):

    # the json data that will be sent to the API as the request body
    json_data = {
        "userId": uid,
        "fromDate": start_date,
        "toDate": end_date,
    }

    # the headers that will be sent to the API as the request headers
    headers = {
        "x-requested-with": "XMLHttpRequest",
    }

    # login details are sent as payload
    payload = {
        "email": email,
        "password": password,
    }

    # if the session is not set, we need to throw an error
    if session == None:
        raise Exception("Not Authenticated, please login")

    # get the actual training session data
    if data_type == "training_history":

        # send the request to the API
        activities = session.post(
            "https://flow.polar.com/api/training/history",
            cookies=session.cookies.get_dict(),
            headers=headers,
            json=json_data,
        )

        # if the request was not successful, return an empty list
        if activities.status_code != 200:
            raise Exception("Activity data not found")

        # if the request was successful, return the json data
        activities = activities.json()

        # return the activities
        return activities

    # get the sleep data
    if data_type == "sleep":

        # find the dates between the start and end date
        dates = pd.date_range(start_date, end_date)

        # the endpoint link for the sleep data
        sleep_req_link = f"https://sleep-api.flow.polar.com/api/sleep/report?from={start_date}&to={end_date}"

        # send the request to the API
        sleep = session.get(
            sleep_req_link,
            cookies=session.cookies.get_dict(),
            headers=headers,
            json=json_data,
        )

        # if the request was not successful, return an empty list
        if sleep.status_code != 200:
            print("Sleep data not found")
            if len(dates) < 31:
                raise Exception("Please provide a date range of at 1 month")
            return []

        # if the request was successful, return the json data
        return sleep.json()

    # get the training data by id
    if data_type == "training_by_id":

        # if the training id is not provided, return an empty list
        if training_id == None:
            raise Exception("Please provide training_id")

        # send the request to the API
        r = session.get("https://flow.polar.com/api/export/training/csv/" + training_id)

        # if the request was not successful, return an empty list
        if r.status_code != 200:
            raise Exception("Training data not found")

        # this extracts the first row of the csv file, which contains the actvity info
        res_df_info = pd.read_csv(
            io.StringIO(r.text), sep=",", engine="python", nrows=1
        )

        # this extracts the rest of the csv file, which contains the activity data
        res_df_data = pd.read_csv(
            io.StringIO(r.text), sep=",", engine="python", skiprows=2
        )

        # convert the data to a dictionary
        filtered = res_df_data.to_dict("index")

        # create an array to store the data
        arr = [res_df_info.to_dict("index")[0]]

        # append the data to the array
        for i in filtered:
            arr.append(filtered[i])

        # return the array
        return arr
