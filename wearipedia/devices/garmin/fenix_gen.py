from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from tqdm import tqdm

__all__ = ["create_syn_data"]


################
# some helpers #
################


def get_act_level(steps):
    """Heuristically determine the activity level based on the number of steps.

    :param steps: number of steps
    :type steps: int
    :return: activity level
    :rtype: str
    """
    if steps < 100:
        return "sedentary"
    else:
        return "active"


def get_start_end(start_remove, remove_duration, mult):
    """Only used in the code that randomly deletes data (for missing data simulation purposes).
    This function computes the index of the first and last elements to remove.

    :param start_remove: point in time to start removing data
    :type start_remove: _type_
    :param remove_duration: point in time to stop removing data
    :type remove_duration: _type_
    :param mult: multiplier, meaning the number of chunks per hour
    :type mult: int
    :return: tuple of start and end indices
    :rtype: Tuple[int, int]
    """
    # we just multiply by `mult` and then round to the nearest integer
    return int(start_remove * mult), int((start_remove + remove_duration) * mult)


start_date = "2022-03-01"
end_date = "2022-06-17"
num_days = (
    datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")
).days


def get_steps():
    """Generate synthetic steps data for a given number of days."""
    steps_synth = []

    # num_step_elems represents the number of 15-minute chunks in a day
    num_step_elems = 96

    for day_idx in range(num_days):

        # sample the number of steps for this chunk for each
        # activity level as Poisson
        sedentary_poi = np.random.poisson(20, size=num_step_elems)
        medium_poi = np.random.poisson(500, size=num_step_elems)
        high_poi = np.random.poisson(1500, size=num_step_elems)

        # the below code samples from a Markov chain with 3 states:
        # 1. "sedentary"
        # 2. "medium"
        # 3. "high"
        # the values were heuristically determined

        mask = []
        cur_state = 0
        for i in range(num_step_elems):
            # draw from a uniform distribution
            rand_draw = np.random.randn()

            # now transition to the next state
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

            # record the state
            mask.append(cur_state)

        # just overwrite the values for the "sedentary" state
        # and save this as synth_steps_day
        medium_idxes = np.where(np.array(mask) == 1)[0]
        high_idxes = np.where(np.array(mask) == 2)[0]

        sedentary_poi[medium_idxes] = medium_poi[medium_idxes]
        sedentary_poi[high_idxes] = high_poi[high_idxes]

        synth_steps_day = sedentary_poi

        # compute the start and end timestamps for each 15-minute chunk
        start_gmts = [
            datetime.strptime(start_date, "%Y-%m-%d")
            + timedelta(days=day_idx, hours=7, minutes=15 * i)
            for i in range(num_step_elems)
        ]

        end_gmts = [start_gmt + timedelta(minutes=15) for start_gmt in start_gmts]

        # just heuristically determine the activity level for each chunk
        # based on the number of steps
        primary_activity_levels = [
            get_act_level(synth_step) for synth_step in synth_steps_day
        ]

        # just set everything to be true
        activity_level_constants = [True] * num_step_elems

        # put everything into a list of dictionaries
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
    """Get synthetic heart rate data for a given number of days, based on the steps data that
    has already been generated.

    :param steps_synth: step data outputted from get_steps()
    :type steps_synth: List[List[Dict]]
    :return: heart rate data, a list of dictionaries, where each dictionary represents a single day, and each dictionary contains a list of heart rate values throughout the day marked by timestamp
    :rtype: List[Dict]
    """

    synth_hrs = []

    for day_idx in tqdm(range(num_days)):
        # the heart rate values are represented by a list of 2-minute chunks,
        # so here we compute the timestamps for all 2-minute chunks in a day

        num_hr_elems = int(24 * (60 // 2))

        hr_timestamps = [
            datetime.strptime(start_date, "%Y-%m-%d")
            + timedelta(days=day_idx, hours=7, minutes=2 * i)
            for i in range(num_hr_elems)
        ]

        steps_arrdict_day = steps_synth[day_idx]

        hr_vals = []

        for hr_timestamp in hr_timestamps:
            # first get the steps 15-minute chunk corresponding to this heart rate timestamp
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

            # compute the heart rate as a linear function of the number of steps,
            # then add a small amount of noise (coefficients heuristically determined)
            hr_val = int(step_val_avg * 0.03 + 80 + np.random.randn() * 5)

            # multiply by 1000 since the API outputs in milliseconds
            hr_vals.append([int(hr_timestamp.timestamp()) * 1000, hr_val])

        # get the current day as a string
        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day_idx)
        date_str = datetime.strftime(date, "%Y-%m-%d")

        hr_day_dict = {
            "userProfilePK": 104779225,  # this was just copied from the real data
            "calendarDate": date_str,
            # this is a bit of hardcoding because of California (7 hours behind GMT)
            "startTimestampGMT": f"{date_str}T07:00:00.0",
            # again, hardcoding (but offset by a day)
            "endTimestampGMT": f'{datetime.strftime(date + timedelta(days=1), "%Y-%m-%d")}T07:00:00.0',
            # obviously no need to adjust here, it's just midnight
            "startTimestampLocal": f"{date_str}T00:00:00.0",
            # again, midnight (but offset by a day)
            "endTimestampLocal": f'{datetime.strftime(date + timedelta(days=1), "%Y-%m-%d")}T00:00:00.0',
            # just manually computed from our heart rate values
            "maxHeartRate": max([hr_val[1] for hr_val in hr_vals]),
            "minHeartRate": min([hr_val[1] for hr_val in hr_vals]),
            "restingHeartRate": 60,  # hard code
            "lastSevenDaysAvgRestingHeartRate": 60,  # hard code
            # copied from real API output
            "heartRateValueDescriptors": [
                {"key": "timestamp", "index": 0},
                {"key": "heartrate", "index": 1},
            ],
            # just the values we obtained earlier
            "heartRateValues": hr_vals,
        }

        synth_hrs.append(hr_day_dict)

    return synth_hrs


def get_brpms(synth_hrs):
    """Generate synthetic breath rate per minute data.

    This function is fairly straightforward.

    :param synth_hrs: list of dicts, each dict is a day of heart rate data
    :type synth_hrs: List[Dict]
    :return: _description_
    :rtype: _type_
    """
    synth_brpms = []

    for day_idx in tqdm(range(num_days)):
        # since the sample rate for breaths per minute is exactly the same
        # as for heart rate, we can just copy the heart rate timestamps
        # and generate breaths per minute values based on the heart rate values
        # (with a linear function)
        synth_hr_vals = synth_hrs[day_idx]["heartRateValues"]
        synth_brpm_vals = [
            [synth_hr_val[0], int(synth_hr_val[1] * 0.1 + 5)]
            for synth_hr_val in synth_hr_vals
        ]

        # just get the date as a string
        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day_idx)
        date_str = datetime.strftime(date, "%Y-%m-%d")

        brpm_dict = {
            # copied from real API output
            "userProfilePK": 104779225,
            "calendarDate": date_str,
            # this is a bit of hardcoding because of California (7 hours behind GMT)
            "startTimestampGMT": f"{date_str}T07:00:00.0",
            # again, hardcoding (but offset by a day)
            "endTimestampGMT": f'{datetime.strftime(date + timedelta(days=1), "%Y-%m-%d")}T07:00:00.0',
            # obviously no need to adjust here, it's just midnight
            "startTimestampLocal": f"{date_str}T00:00:00.0",
            # again, midnight (but offset by a day)
            "endTimestampLocal": f'{datetime.strftime(date + timedelta(days=1), "%Y-%m-%d")}T00:00:00.0',
            # all the stuff below is just copied from the real API output
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
            # just the values we obtained earlier
            "respirationValuesArray": synth_brpm_vals,
        }

        synth_brpms.append(brpm_dict)

    return synth_brpms


def delete_stuff(dates, steps, hrs, brpms):
    """Delete stuff randomly, since we want to simulate missing data.

    :param dates: List of dates (each date is a separate day represented as a string)
    :type dates: List[str]
    :param steps: List of step data (each element is a list of dictionaries, each dictionary represents the step data for a 15-minute chunk of time in the day)
    :type steps: List[List[Dict]]
    :param hrs: List of heart rate data (each element is a dictionary)
    :type hrs: List[Dict]
    :param brpms: List of breathing rate data (each element is a dictionary)
    :type brpms: List[Dict]
    :return: List of dates, List of step data, List of heart rate data, List of breathing rate data
    :rtype: Tuple[List[str], List[Dict], List[Dict], List[Dict]]
    """

    for day_idx in tqdm(range(num_days)):
        # the duration to remove (in hours) is sampled from an exponential distribution,
        # except we trim the undesirable long tails of the distribution
        remove_duration = np.clip(np.random.exponential(3), 0, 16)

        # we remove everything after a certain time, so compute the
        # start of that
        start_remove = np.random.uniform(0, 24 - remove_duration)

        # compute the index of the first and last elements to remove,
        # note that we provide 30 because heart rate and breath rate
        # is sampled every 2 minutes, so there are 30 samples per hour
        start_idx, end_idx = get_start_end(start_remove, remove_duration, 30)

        # Just slice and replace the middle part with a filler element,
        # which just contains None (this is what the API would return
        # when there is missing data). We do this for all the data types.
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

        # provide 4 because steps are sampled every 15 minutes,
        # so there are 4 samples per hour
        start_idx, end_idx = get_start_end(start_remove, remove_duration, 4)

        steps[day_idx] = steps[day_idx][:start_idx] + steps[day_idx][end_idx:]

    return dates, steps, hrs, brpms


def create_syn_data():
    """Returns a tuple of dates, steps, heart rates, and breath rates. The data
    format is as follows. Each element in the tuple is a list of length num_days.
    For each tuple:
    - dates: List of dates (each date is a separate day represented as a string)
    - steps: List of step data (each element is a list of dictionaries, each dictionary represents the step data for a 15-minute chunk of time in the day)
    - heart rates: List of heart rate data (each element is a dictionary)
    - breath rates: List of breathing rate data (each element is a dictionary)

    :return: A four-tuple of dates, steps, heart rates, and breath rates, each
        of which is just a list where each element represents a particular day.
    :rtype: Tuple[List[str], List[List[Dict]], List[Dict], List[Dict]]
    """

    # first get the dates as datetime objects
    synth_dates = [
        datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        for i in range(num_days)
    ]

    # process is to first get the steps, then the heart rate (since you can just compute the heart rate from the steps), then the
    # breathing rate (since you can just compute the breathing rate from the heart rate)
    synth_steps = get_steps()
    synth_hrs = get_hrs(synth_steps)
    synth_brpms = get_brpms(synth_hrs)

    # finally, we just iterate over the steps and
    # turn the start and end timestamps to strings
    for i, synth_steps_day in enumerate(synth_steps):
        for j in range(len(synth_steps_day)):
            synth_steps[i][j]["startGMT"] = datetime.strftime(
                synth_steps[i][j]["startGMT"], "%Y-%-m-%dT%H:%M:%S"
            )
            synth_steps[i][j]["endGMT"] = datetime.strftime(
                synth_steps[i][j]["endGMT"], "%Y-%-m-%dT%H:%M:%S"
            )

    # randomly delete stuff (to simulate missing data)
    synth_dates, synth_steps, synth_hrs, synth_brpms = delete_stuff(
        synth_dates, synth_steps, synth_hrs, synth_brpms
    )

    return synth_dates, synth_steps, synth_hrs, synth_brpms
