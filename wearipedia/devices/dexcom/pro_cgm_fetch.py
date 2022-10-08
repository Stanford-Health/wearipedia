import json
from datetime import datetime

import pandas as pd
import requests

__all__ = ["fetch_data"]


def fetch_data(access_token, start_date="2022-02-16", end_date="2022-05-15"):
    start_date = start_date + "T15:30:00"
    end_date = end_date + "T15:45:00"

    headers = {"authorization": f"Bearer {access_token}"}

    endpoint = f"https://api.dexcom.com/v2/users/self/egvs?startDate={start_date}&endDate={end_date}"

    out = json.loads(requests.get(endpoint, headers=headers).text)

    if "errors" in out.keys():
        print(f'Got error(s) {out["errors"]}. Fix start and end dates and rerun.')
    elif "fault" in out.keys():
        print(
            f'Got fault {out["fault"]}. You might need to request another access token.'
        )
    else:

        def dt_string_to_obj(dt_str):
            # converts string like "2022-04-10T10:13:00" to a datetime object
            return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")

        data_dict = [
            {
                "datetime": dt_string_to_obj(x["displayTime"]),
                "glucose_level": x["realtimeValue"],
            }
            for x in out["egvs"][::-1]
        ]

        df = pd.DataFrame.from_dict(data_dict)

        return df
