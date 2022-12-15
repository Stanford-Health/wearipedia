import requests
import pandas as pd
import time
import numpy as np

perPageLimit = 200
pageCount = 1

dateConvert = lambda date_string: int(time.mktime(time.strptime(date_string, '%Y-%m-%d')))


def fetch_real_data(self, start_date, end_date, data_type):
    # URL to access all of participant's activities.

    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    #Header that sends the Access Token in the GET request
    header = {'Authorization': 'Bearer ' + self.access_token}
    param = {'per_page': perPageLimit, 'page': pageCount, 'before': dateConvert(end_date), 'after': dateConvert(start_date)}

    #GET request to get all your activities from the API
    my_dataset = requests.get(activites_url, headers=header, params=param).json()

    df_strava = pd.json_normalize(my_dataset)

    if data_type == 'map_summary_polyline':
        data_type = 'map.summary_polyline'

    filtered = df_strava.get(['name','id',
       'start_date',data_type]).to_dict('index')

    arr = []

    for i in filtered:
        arr.append(filtered[i])

    return arr