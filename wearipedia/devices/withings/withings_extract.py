# utility scripts to extract via Withings API

####################################
# Withings ScanWatch notebook code #
####################################

# @title Enter start and end dates
start_date = "2020-05-20"  # @param {type:"date"}
end_date = "2022-07-20"  # @param {type:"date"}

import json
import time
import urllib
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm

# import july
# from july.utils import date_range


num_to_description = {
    1: "Weight (kg)",
    4: "Height (meter)",
    5: "Fat Free Mass (kg)",
    6: "Fat Ratio (%)",
    8: "Fat Mass Weight (kg)",
    9: "Diastolic Blood Pressure (mmHg)",
    10: "Systolic Blood Pressure (mmHg)",
    11: "Heart Pulse (bpm) - only for BPM and scale devices",
    12: "Temperature (celsius)",
    54: "SP02 (%)",
    71: "Body Temperature (celsius)",
    73: "Skin Temperature (celsius)",
    76: "Muscle Mass (kg)",
    77: "Hydration (kg)",
    88: "Bone Mass (kg)",
    91: "Pulse Wave Velocity (m/s)",
    123: "VO2 max is a numerical measurement of your body’s ability to consume oxygen (ml/min/kg).",
    135: "QRS interval duration based on ECG signal",
    136: "PR interval duration based on ECG signal",
    137: "QT interval duration based on ECG signal",
    138: "Corrected QT interval duration based on ECG signal",
    139: "Atrial fibrillation result from PPG",
}

NUM_RETRIES = 3


def fetch_all_wrapper(endpoint_url, data, headers, arr_key, parse_data=lambda x: x):
    # wrapper around public API that retrieves arbitrarily large # of
    # records, since there is a restriction of # of records per API response
    # NOTES:
    # out['body'][arr_key] is concatenated across several requests
    # parse_data is a function that parses the returned array

    cur_offset = 0
    arr_complete = None

    arr = None

    while True:
        # endpoint can be flaky if the response payload is extremely large,
        # so retry at most NUM_RETRIES times
        for i in range(NUM_RETRIES):
            data_args = {**data, "offset": cur_offset}

            out = requests.post(endpoint_url, data=data_args, headers=headers)

            out = json.loads(out.text)

            if out["status"] == 401:
                raise Exception(
                    f"request response is {out} for request {data_args} to endpoint {endpoint_url}, headers {headers}"
                )

            try:
                arr = parse_data(out["body"][arr_key])
                break
            except KeyError:
                if "body" in out.keys():
                    raise Exception(
                        f'got key {arr_key}, expected one of {out["body"].keys()}'
                    )
                elif out["status"] == 2555:
                    # when the payload is too large, this is the status code
                    continue
                else:
                    raise Exception(
                        f"request response is {out} for request {data_args} to endpoint {endpoint_url}, headers {headers}"
                    )

        # for example, https://developer.withings.com/api-reference/#operation/measurev2-getactivity
        # vs. https://developer.withings.com/api-reference/#operation/measure-getmeas

        if arr is not None:
            if type(arr) == type({}):
                if arr_complete is None:
                    arr_complete = dict()

                arr_complete.update(arr)

            elif type(arr) == type([]):
                if arr_complete is None:
                    arr_complete = []

                arr_complete += arr

            # continue if there's still more to get
            if "more" in out["body"].keys() and out["body"]["more"] == 1:
                cur_offset = out["body"]["offset"]
            else:
                break
        else:
            break

    # replace with concatenated version
    if arr_complete is not None:
        out["body"][arr_key] = arr_complete

    return out


def fetch_all_heart_rate(access_token, start="2020-03-10", end="2022-05-28"):
    # get all dates heart rate was collected for
    out = fetch_all_wrapper(
        "https://wbsapi.withings.net/v2/heart",
        {
            "action": "list",
            "startdateymd": start,
            "enddateymd": end,
        },
        {"Authorization": f"Bearer {access_token}"},
        arr_key="series",
    )

    signals = [
        act["ecg"]["signalid"]
        for act in out["body"]["series"]
        if act["ecg"] and act["signalid"]
    ]

    # now for each date get the heart rate data and store as list of dicts
    dict_list = []
    for signal in tqdm(signals):
        out = fetch_all_wrapper(
            "https://wbsapi.withings.net/v2/heart",
            {
                "action": "get",
                "signalid": signal,
            },
            {"Authorization": f"Bearer {access_token}"},
            arr_key="series",
        )

        if "body" in out.keys():
            dict_list += [
                {"datetime": datetime.fromtimestamp(int(k)), **v}
                for k, v in out["body"]["series"].items()
                if datetime.strptime(start, "%Y-%m-%d")
                <= datetime.fromtimestamp(int(k))
                <= datetime.strptime(end, "%Y-%m-%d")
            ]

    df = pd.DataFrame.from_dict(dict_list)

    return df


def fetch_all_sleeps(access_token, start="2020-03-10", end="2022-05-28"):
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(end, "%Y-%m-%d")

    out = fetch_all_wrapper(
        "https://wbsapi.withings.net/v2/sleep",
        {
            "action": "get",
            "startdate": int(time.mktime(start_dt.timetuple())),
            "enddate": int(time.mktime(end_dt.timetuple())),
            "data_fields": "hr,rr,snoring,sdnn_1,rmssd,mvt_score,chest_movement_rate,withings_index,breathing_sounds",
        },
        {"Authorization": f"Bearer {access_token}"},
        arr_key="series",
    )

    df = pd.DataFrame.from_dict(out["body"]["series"])

    return df


def fetch_all_sleep_summaries(access_token, start="2020-03-10", end="2022-05-28"):
    out = fetch_all_wrapper(
        "https://wbsapi.withings.net/v2/sleep",
        {
            "action": "getsummary",
            "startdateymd": start,
            "enddateymd": end,
            "data_fields": "total_timeinbed,total_sleep_time,asleepduration,lightsleepduration,remsleepduration,deepsleepduration,sleep_efficiency,sleep_latency,wakeup_latency,wakeupduration,wakeupcount,waso,nb_rem_episodes,apnea_hypopnea_index,withings_index,durationtosleep,durationtowakeup,out_of_bed_count,hr_average,hr_min,hr_max,rr_average,rr_min,rr_max,snoring,snoringepisodecount,sleep_score,night_events,mvt_score_avg,mvt_active_duration,chest_movement_rate_average,chest_movement_rate_min,chest_movement_rate_max,breathing_sounds,breathing_sounds_episode_count",
        },
        {"Authorization": f"Bearer {access_token}"},
        arr_key="series",
    )

    df = pd.DataFrame.from_dict(out["body"]["series"])

    return df


#############################
# body+ scale notebook code #
#############################

# @title Extract data via the API!
use_synthetic = True  # @param {type:"boolean"}

num_to_description = {
    1: "Weight (kg)",
    4: "Height (meter)",
    5: "Fat Free Mass (kg)",
    6: "Fat Ratio (%)",
    8: "Fat Mass Weight (kg)",
    9: "Diastolic Blood Pressure (mmHg)",
    10: "Systolic Blood Pressure (mmHg)",
    11: "Heart Pulse (bpm) - only for BPM and scale devices",
    12: "Temperature (celsius)",
    54: "SP02 (%)",
    71: "Body Temperature (celsius)",
    73: "Skin Temperature (celsius)",
    76: "Muscle Mass (kg)",
    77: "Hydration (kg)",
    88: "Bone Mass (kg)",
    91: "Pulse Wave Velocity (m/s)",
    123: "VO2 max is a numerical measurement of your body’s ability to consume oxygen (ml/min/kg).",
    135: "QRS interval duration based on ECG signal",
    136: "PR interval duration based on ECG signal",
    137: "QT interval duration based on ECG signal",
    138: "Corrected QT interval duration based on ECG signal",
    139: "Atrial fibrillation result from PPG",
}


def fetch_measurements(access_token, start, end, measure_types="1,6"):
    # make public API requests, while specifying the measure_types we desire
    # we make potentially multiple because the public API can return only up
    # to 200 measurements

    cur_offset = 0
    data_complete = []
    while True:
        out = requests.post(
            "https://wbsapi.withings.net/measure",
            data={
                "action": "getmeas",
                "meastypes": measure_types,
                "offset": cur_offset,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        # convert this to python dict and get just the actual time series as
        # a pandas dataframe
        out = json.loads(out.text)
        measurements = out["body"]["measuregrps"]

        data = [
            {
                **{"date": datetime.fromtimestamp(meas["date"])},
                **{
                    num_to_description[meas_val["type"]]: meas_val["value"]
                    * 10 ** (meas_val["unit"])
                    for meas_val in meas["measures"]
                },
            }
            for meas in measurements
            if start < datetime.fromtimestamp(meas["date"]) < end
        ]
        # filter by start/end, even though this is kind of mutating what
        # the API gives us raw...

        data_complete += data

        if "more" in out["body"].keys() and out["body"]["more"] == 1:
            cur_offset = out["body"]["offset"]
        else:
            break

    df = pd.DataFrame(data)

    return df
