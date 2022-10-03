from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm

__all__ = ["create_syn_data"]


def get_act_level(steps):
    if steps < 100:
        return "sedentary"
    else:
        return "active"


start_date = "2022-03-01"  # @param {type:"string"}
end_date = "2022-06-17"  # @param {type:"string"}
num_days = (
    datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")
).days

# for each day, determine length of chunk that is taken out, then randomly place it
def get_start_end(start_remove, remove_duration, mult):
    return int(start_remove * mult), int((start_remove + remove_duration) * mult)


def get_steps():
    steps_synth = []

    for day_idx in range(num_days):

        sedentary_poi = np.random.poisson(20, size=96)

        medium_poi = np.random.poisson(500, size=96)
        high_poi = np.random.poisson(1500, size=96)

        mask = []
        cur_state = 0
        for i in range(96):
            rand_draw = np.random.randn()
            if cur_state == 0:
                if rand_draw < 0.9:
                    cur_state = 0
                elif rand_draw < 0.97:
                    cur_state = 1
                else:
                    cur_state = 2
            elif cur_state == 1:
                if rand_draw < 0.6:
                    cur_state = 1
                elif rand_draw < 0.8:
                    cur_state = 2
                else:
                    cur_state = 0
            elif cur_state == 2:
                if rand_draw < 0.4:
                    cur_state = 2
                elif rand_draw < 0.8:
                    cur_state = 1
                else:
                    cur_state = 0

            mask.append(cur_state)

        medium_idxes = np.where(np.array(mask) == 1)[0]
        high_idxes = np.where(np.array(mask) == 2)[0]

        sedentary_poi[medium_idxes] = medium_poi[medium_idxes]
        sedentary_poi[high_idxes] = high_poi[high_idxes]

        synth_steps_day = sedentary_poi

        start_gmts = [
            datetime.strptime(start_date, "%Y-%m-%d")
            + timedelta(days=day_idx, hours=7, minutes=15 * i)
            for i in range(96)
        ]

        end_gmts = [start_gmt + timedelta(minutes=15) for start_gmt in start_gmts]

        primary_activity_levels = [
            get_act_level(synth_step) for synth_step in synth_steps_day
        ]

        activity_level_constants = [True] * 96

        steps_arrdict_day = [
            {
                "startGMT": start_gmt,
                "endGMT": end_gmt,
                "steps": synth_step,
                "primaryActivityLevel": primary_activity_level,
                "activityLevelConstant": activity_level_constant,
            }
            for start_gmt, end_gmt, synth_step, primary_activity_level, activity_level_constant in zip(
                start_gmts,
                end_gmts,
                synth_steps_day,
                primary_activity_levels,
                activity_level_constants,
            )
        ]

        steps_synth.append(steps_arrdict_day)

    return steps_synth


def get_hrs(steps_synth):
    synth_hrs = []

    for day_idx in tqdm(range(num_days)):
        hr_timestamps = [
            datetime.strptime(start_date, "%Y-%m-%d")
            + timedelta(days=day_idx, hours=7, minutes=2 * i)
            for i in range(720)
        ]

        steps_arrdict_day = steps_synth[day_idx]

        hr_vals = []

        for i, hr_timestamp in enumerate(hr_timestamps):
            step_timestamps = np.array(
                [x["startGMT"].timestamp() for x in steps_arrdict_day]
            )

            step_idx = np.where(
                np.logical_and(
                    hr_timestamp.timestamp() >= step_timestamps,
                    hr_timestamp.timestamp() <= step_timestamps + 15 * 60,
                )
            )[0][0]

            step_val_avg = steps_arrdict_day[step_idx]["steps"]

            hr_val = int(step_val_avg * 0.03 + 80 + np.random.randn() * 5)

            hr_vals.append([int(hr_timestamp.timestamp()) * 1000, hr_val])

        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day_idx)
        date_str = datetime.strftime(date, "%Y-%m-%d")

        hr_day_dict = {
            "userProfilePK": 104779225,
            "calendarDate": date_str,
            "startTimestampGMT": f"{date_str}T07:00:00.0",
            "endTimestampGMT": f'{datetime.strftime(date + timedelta(days=1), "%Y-%m-%d")}T07:00:00.0',
            "startTimestampLocal": f"{date_str}T00:00:00.0",
            "endTimestampLocal": f'{datetime.strftime(date + timedelta(days=1), "%Y-%m-%d")}T00:00:00.0',
            "maxHeartRate": max([hr_val[1] for hr_val in hr_vals]),
            "minHeartRate": min([hr_val[1] for hr_val in hr_vals]),
            "restingHeartRate": 60,  # hard code
            "lastSevenDaysAvgRestingHeartRate": 60,  # hard code
            "heartRateValueDescriptors": [
                {"key": "timestamp", "index": 0},
                {"key": "heartrate", "index": 1},
            ],
            "heartRateValues": hr_vals,
        }

        synth_hrs.append(hr_day_dict)

    return synth_hrs


def get_brpms(synth_hrs):
    synth_brpms = []

    for day_idx in tqdm(range(num_days)):

        synth_hr_vals = synth_hrs[day_idx]["heartRateValues"]
        synth_brpm_vals = [
            [synth_hr_val[0], int(synth_hr_val[1] * 0.1 + 5)]
            for synth_hr_val in synth_hr_vals
        ]

        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day_idx)
        date_str = datetime.strftime(date, "%Y-%m-%d")

        brpm_dict = {
            "userProfilePK": 104779225,
            "calendarDate": date_str,
            "startTimestampGMT": f"{date_str}T07:00:00.0",
            "endTimestampGMT": f'{datetime.strftime(date + timedelta(days=1), "%Y-%m-%d")}T07:00:00.0',
            "startTimestampLocal": f"{date_str}T00:00:00.0",
            "endTimestampLocal": f'{datetime.strftime(date + timedelta(days=1), "%Y-%m-%d")}T00:00:00.0',
            "sleepStartTimestampGMT": None,
            "sleepEndTimestampGMT": None,
            "sleepStartTimestampLocal": None,
            "sleepEndTimestampLocal": None,
            "tomorrowSleepStartTimestampGMT": None,
            "tomorrowSleepEndTimestampGMT": None,
            "tomorrowSleepStartTimestampLocal": None,
            "tomorrowSleepEndTimestampLocal": None,
            "lowestRespirationValue": 12.0,
            "highestRespirationValue": 23.0,
            "avgWakingRespirationValue": 15.0,
            "avgSleepRespirationValue": None,
            "avgTomorrowSleepRespirationValue": None,
            "respirationValueDescriptorsDTOList": [
                {"key": "timestamp", "index": 0},
                {"key": "respiration", "index": 1},
            ],
            "respirationValuesArray": synth_brpm_vals,
        }

        synth_brpms.append(brpm_dict)

    return synth_brpms


def delete_stuff(dates, steps, hrs, brpms):
    for day_idx in tqdm(range(num_days)):
        remove_duration = np.clip(np.random.exponential(3), 0, 16)

        start_remove = np.random.uniform(0, 24 - remove_duration)

        start_idx, end_idx = get_start_end(start_remove, remove_duration, 30)

        filler = [hrs[day_idx]["heartRateValues"][start_idx][0], None]
        hrs[day_idx]["heartRateValues"] = (
            hrs[day_idx]["heartRateValues"][:start_idx]
            + [filler]
            + hrs[day_idx]["heartRateValues"][end_idx:]
        )
        filler = [brpms[day_idx]["respirationValuesArray"][start_idx][0], None]
        brpms[day_idx]["respirationValuesArray"] = (
            brpms[day_idx]["respirationValuesArray"][:start_idx]
            + [filler]
            + brpms[day_idx]["respirationValuesArray"][end_idx:]
        )

        start_idx, end_idx = get_start_end(start_remove, remove_duration, 4)

        steps[day_idx] = steps[day_idx][:start_idx] + steps[day_idx][end_idx:]

    return dates, steps, hrs, brpms


def create_syn_data():
    synth_dates = [
        datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        for i in range(num_days)
    ]

    synth_steps = get_steps()
    synth_hrs = get_hrs(synth_steps)
    synth_brpms = get_brpms(synth_hrs)

    for i, synth_steps_day in enumerate(synth_steps):
        for j, steps_dict in enumerate(synth_steps_day):
            synth_steps[i][j]["startGMT"] = datetime.strftime(
                synth_steps[i][j]["startGMT"], "%Y-%-m-%dT%H:%M:%S"
            )
            synth_steps[i][j]["endGMT"] = datetime.strftime(
                synth_steps[i][j]["endGMT"], "%Y-%-m-%dT%H:%M:%S"
            )

    # randomly delete stuff
    synth_dates, synth_steps, synth_hrs, synth_brpms = delete_stuff(
        synth_dates, synth_steps, synth_hrs, synth_brpms
    )

    return synth_dates, synth_steps, synth_hrs, synth_brpms
