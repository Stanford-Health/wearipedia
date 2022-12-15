
import wearipedia
import numpy as np


strava = wearipedia.get_device("strava/strava")

strava.authenticate({
"client_id": '83434',
"client_secret": '915c245ef1949c64e9a1e01dfa7a52f78bc4628c',
"refresh_token": '7c7c2b4ff166f43e7a0d7329a60c379419623766'
})


for v in ['distance', 'moving_time', 'elapsed_time',
       'total_elevation_gain', 'average_speed',
       'max_speed','average_heartrate','max_heartrate','map_summary_polyline',
       'elev_high','elev_low','average_cadence',
       'average_watts','kilojoules']:
    print(strava.get_data(v, params={"start_date": "2022-05-01", "end_date": "2022-05-10"}))


# garmin = wearipedia.get_device("garmin/fenix_7s")

# print(garmin.get_data("steps")[0][0])