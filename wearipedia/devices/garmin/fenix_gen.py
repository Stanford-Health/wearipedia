from datetime import datetime, timedelta

import random
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
    :type start_remove: float
    :param remove_duration: point in time to stop removing data
    :type remove_duration: float
    :param mult: multiplier, meaning the number of chunks per hour
    :type mult: int
    :return: tuple of start and end indices
    :rtype: Tuple[int, int]
    """
    # we just multiply by `mult` and then round to the nearest integer
    return int(start_remove * mult), int((start_remove + remove_duration) * mult)


def get_steps(start_date, num_days):
    """Generate steps data for a given number of days.

    :return: steps data, a list of lists, where each list represents a single day, and each
        list contains a many steps values throughout the day marked by timestamp.
    :rtype: List[List]
    """
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
        # the transition probabilities were heuristically determined

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

        # convert to regular int, no need for np.int64
        synth_steps_day = [int(synth_step) for synth_step in sedentary_poi]

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


def get_hrs(start_date, num_days, steps_synth):
    """Get synthetic heart rate data for a given number of days, based on the steps data that
    has already been generated.

    :param steps_synth: step data outputted from get_steps()
    :type steps_synth: List[List[Dict]]
    :return: heart rate data, a list of dictionaries, where each dictionary represents a
        single day, and each dictionary contains a list of heart rate values throughout the day
        marked by timestamp.
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


def get_brpms(start_date, num_days, synth_hrs):
    """Generate synthetic breath rate per minute data.

    This function is fairly straightforward.

    :param synth_hrs: list of dicts, each dict is a day of heart rate data
    :type synth_hrs: List[Dict]
    :return: breath rate per minute data, a list of dictionaries, where each dictionary
        represents a single day, and each dictionary contains a list of breath rate per
        minute values throughout the day marked by timestamp.
    :rtype: List[Dict]
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

def get_hrv_data(start_date, num_days):
    """Generate synthetic heart rate variability (HRV) data for a specified date range.

    This function generates synthetic HRV data for a given date range. Each day's data
    is represented by a dictionary containing HRV readings, summary statistics, and
    timestamps.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which to generate HRV data.
    :type num_days: int
    :return: List of dictionaries, each representing a day's HRV data.
    :rtype: List[Dict]
    """
    hrv_data = []

    for _ in range(num_days):
        user_profile_pk = random.randint(10000000, 99999999)
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')
        weekly_avg = None
        last_night_avg = random.randint(10, 40)
        last_night_5min_high = random.randint(30, 60)
        baseline = None
        status = 'NONE'
        feedback_phrase = 'ONBOARDING_1'
        create_time_stamp = f"{calendar_date}T14:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.000"

        start_timestamp_gmt = f"{calendar_date}T06:00:00.0"
        end_timestamp_gmt = f"{calendar_date}T13:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.0"
        start_timestamp_local = f"{(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')}T23:00:00.0"
        end_timestamp_local = f"{calendar_date}T06:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.0"

        sleep_start_timestamp_gmt = None
        sleep_end_timestamp_gmt = None
        sleep_start_timestamp_local = None
        sleep_end_timestamp_local = None

        hrv_reading = []

        hrv_entry = {
            'userProfilePk': user_profile_pk,
            'hrvSummary': {
                'calendarDate': calendar_date,
                'weeklyAvg': weekly_avg,
                'lastNightAvg': last_night_avg,
                'lastNight5MinHigh': last_night_5min_high,
                'baseline': baseline,
                'status': status,
                'feedbackPhrase': feedback_phrase,
                'createTimeStamp': create_time_stamp
            },
            'hrvReadings': hrv_reading,
            'startTimestampGMT': start_timestamp_gmt,
            'endTimestampGMT': end_timestamp_gmt,
            'startTimestampLocal': start_timestamp_local,
            'endTimestampLocal': end_timestamp_local,
            'sleepStartTimestampGMT': sleep_start_timestamp_gmt,
            'sleepEndTimestampGMT': sleep_end_timestamp_gmt,
            'sleepStartTimestampLocal': sleep_start_timestamp_local,
            'sleepEndTimestampLocal': sleep_end_timestamp_local
        }

        hrv_data.append(hrv_entry)

    return hrv_data

def get_steps_data(start_date, num_days):
    """Generate synthetic step count data for a given date range.

    This function generates synthetic step count data for a specified number of days starting from
    the provided start date. The generated data includes daily step summaries and detailed step
    counts in 15-minute intervals for each day.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which to generate step count data.
    :type num_days: int
    :return: A list of dictionaries, where each dictionary represents step count data for a single day.
        Each dictionary includes daily step totals, status, and detailed step counts in 15-minute intervals.
    :rtype: List[Dict]
    """
    steps_data = []

    for _ in range(num_days):
        user_profile_pk = random.randint(10000000, 99999999)
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')
        create_time_stamp = f"{calendar_date}T14:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.000"
        start_timestamp_gmt = f"{calendar_date}T06:00:00.0"
        end_timestamp_gmt = f"{calendar_date}T13:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.0"
        start_timestamp_local = f"{(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')}T23:00:00.0"
        end_timestamp_local = f"{calendar_date}T06:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.0"

        steps_entry = {
            'userProfilePk': user_profile_pk,
            'stepsSummary': {
                'calendarDate': calendar_date,
                'dailyTotal': random.randint(1000, 15000),
                'status': 'COMPLETED',
                'createTimeStamp': create_time_stamp
            },
            'stepsDetails': [],
            'startTimestampGMT': start_timestamp_gmt,
            'endTimestampGMT': end_timestamp_gmt,
            'startTimestampLocal': start_timestamp_local,
            'endTimestampLocal': end_timestamp_local
        }

        # Generate step data for each interval within a day (e.g., 15-minute intervals)
        interval_start = datetime.strptime(start_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0")
        for i in range(96):  # 24 hours * 60 minutes / 15 minutes
            interval_end = interval_start + timedelta(minutes=15)
            steps = random.randint(0, 200)
            steps_entry['stepsDetails'].append({
                'startTimestampGMT': interval_start.strftime("%Y-%m-%dT%H:%M:%S.0"),
                'endTimestampGMT': interval_end.strftime("%Y-%m-%dT%H:%M:%S.0"),
                'steps': steps,
            })
            interval_start = interval_end

        steps_data.append(steps_entry)

    return steps_data

def get_stats_data(start_date, num_days):
    """Generate synthetic stats data for a specified date range.

    This function generates synthetic stats data for a given date range. The generated data includes
    various user-related metrics and information for each day within the specified range.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which to generate stats data.
    :type num_days: int
    :return: A list of dictionaries, where each dictionary represents user summary data for a single day.
        Each dictionary contains various user-related metrics and information.
    :rtype: List[Dict]
    """
    stats_data = []

    for _ in range(num_days):
        user_profile_id = random.randint(10000000, 99999999)
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')
        total_kilocalories = random.uniform(1500.0, 2500.0)
        active_kilocalories = random.uniform(400.0, 800.0)
        bmr_kilocalories = random.uniform(1000.0, 1500.0)
        wellness_kilocalories = total_kilocalories
        burned_kilocalories = None
        consumed_kilocalories = None
        remaining_kilocalories = total_kilocalories
        total_steps = random.randint(3000, 10000)
        net_calorie_goal = None
        total_distance_meters = random.randint(2000, 6000)
        wellness_distance_meters = total_distance_meters
        wellness_active_kilocalories = active_kilocalories
        net_remaining_kilocalories = active_kilocalories
        user_daily_summary_id = user_profile_id
        rule = {'typeId': 3, 'typeKey': 'subscribers'}
        uuid = 'e933a2a5aa214d3088bec955ea84c9bf'
        daily_step_goal = random.randint(1000, 5000)
        wellness_start_time_gmt = f"{calendar_date}T07:00:00.0"
        wellness_start_time_local = f"{calendar_date}T00:00:00.0"
        wellness_end_time_gmt = f"{(datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=_ + 1)).strftime('%Y-%m-%d')}T07:00:00.0"
        wellness_end_time_local = f"{(datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=_ + 1)).strftime('%Y-%m-%d')}T00:00:00.0"
        duration_in_milliseconds = 86400000
        wellness_description = None
        highly_active_seconds = random.randint(500, 1500)
        active_seconds = random.randint(4000, 7000)
        sedentary_seconds = random.randint(30000, 60000)
        sleeping_seconds = random.randint(20000, 40000)
        includes_wellness_data = True
        includes_activity_data = False
        includes_calorie_consumed_data = False
        privacy_protected = False
        moderate_intensity_minutes = random.randint(0, 60)
        vigorous_intensity_minutes = random.randint(0, 60)
        floors_ascended_in_meters = random.uniform(0.0, 30.0)
        floors_descended_in_meters = random.uniform(0.0, 20.0)
        floors_ascended = random.uniform(0.0, 10.0)
        floors_descended = random.uniform(0.0, 5.0)
        intensity_minutes_goal = random.randint(100, 200)
        user_floors_ascended_goal = random.randint(5, 15)
        min_heart_rate = random.randint(50, 70)
        max_heart_rate = random.randint(120, 150)
        resting_heart_rate = random.randint(60, 80)
        last_seven_days_avg_resting_heart_rate = resting_heart_rate
        source = 'GARMIN'
        average_stress_level = random.uniform(20.0, 60.0)
        max_stress_level = random.uniform(70.0, 100.0)
        stress_duration = random.randint(10000, 40000)
        rest_stress_duration = random.randint(9000, 35000)
        activity_stress_duration = random.randint(1000, 5000)
        uncategorized_stress_duration = random.randint(500, 2000)
        total_stress_duration = random.randint(10000, 40000)
        low_stress_duration = random.randint(4000, 15000)
        medium_stress_duration = random.randint(1000, 5000)
        high_stress_duration = random.randint(500, 3000)
        stress_percentage = random.uniform(10.0, 60.0)
        rest_stress_percentage = random.uniform(10.0, 50.0)
        activity_stress_percentage = random.uniform(5.0, 20.0)
        uncategorized_stress_percentage = random.uniform(2.0, 15.0)
        low_stress_percentage = random.uniform(5.0, 25.0)
        medium_stress_percentage = random.uniform(2.0, 15.0)
        high_stress_percentage = random.uniform(1.0, 10.0)
        stress_qualifier = 'BALANCED'
        measurable_awake_duration = random.randint(30000, 60000)
        measurable_asleep_duration = random.randint(20000, 40000)
        last_sync_timestamp_gmt = None
        min_avg_heart_rate = random.randint(50, 70)
        max_avg_heart_rate = random.randint(120, 150)
        body_battery_charged_value = random.randint(30, 60)
        body_battery_drained_value = random.randint(10, 40)
        body_battery_highest_value = random.randint(40, 70)
        body_battery_lowest_value = random.randint(0, 30)
        body_battery_most_recent_value = random.randint(10, 40)
        body_battery_during_sleep = None
        body_battery_version = 2.0
        abnormal_heart_rate_alerts_count = None
        average_spo2 = None
        lowest_spo2 = None
        latest_spo2 = None
        latest_spo2_reading_time_gmt = None
        latest_spo2_reading_time_local = None
        average_monitoring_environment_altitude = random.uniform(-200.0, 200.0)
        resting_calories_from_activity = None
        avg_waking_respiration_value = random.uniform(10.0, 20.0)
        highest_respiration_value = random.uniform(15.0, 25.0)
        lowest_respiration_value = random.uniform(5.0, 15.0)
        latest_respiration_value = random.uniform(15.0, 25.0)
        latest_respiration_time_gmt = wellness_end_time_gmt

        stats_entry = {
            'userProfileId': user_profile_id,
            'totalKilocalories': total_kilocalories,
            'activeKilocalories': active_kilocalories,
            'bmrKilocalories': bmr_kilocalories,
            'wellnessKilocalories': wellness_kilocalories,
            'burnedKilocalories': burned_kilocalories,
            'consumedKilocalories': consumed_kilocalories,
            'remainingKilocalories': remaining_kilocalories,
            'totalSteps': total_steps,
            'netCalorieGoal': net_calorie_goal,
            'totalDistanceMeters': total_distance_meters,
            'wellnessDistanceMeters': wellness_distance_meters,
            'wellnessActiveKilocalories': wellness_active_kilocalories,
            'netRemainingKilocalories': net_remaining_kilocalories,
            'userDailySummaryId': user_daily_summary_id,
            'calendarDate': calendar_date,
            'rule': rule,
            'uuid': uuid,
            'dailyStepGoal': daily_step_goal,
            'wellnessStartTimeGmt': wellness_start_time_gmt,
            'wellnessStartTimeLocal': wellness_start_time_local,
            'wellnessEndTimeGmt': wellness_end_time_gmt,
            'wellnessEndTimeLocal': wellness_end_time_local,
            'durationInMilliseconds': duration_in_milliseconds,
            'wellnessDescription': wellness_description,
            'highlyActiveSeconds': highly_active_seconds,
            'activeSeconds': active_seconds,
            'sedentarySeconds': sedentary_seconds,
            'sleepingSeconds': sleeping_seconds,
            'includesWellnessData': includes_wellness_data,
            'includesActivityData': includes_activity_data,
            'includesCalorieConsumedData': includes_calorie_consumed_data,
            'privacyProtected': privacy_protected,
            'moderateIntensityMinutes': moderate_intensity_minutes,
            'vigorousIntensityMinutes': vigorous_intensity_minutes,
            'floorsAscendedInMeters': floors_ascended_in_meters,
            'floorsDescendedInMeters': floors_descended_in_meters,
            'floorsAscended': floors_ascended,
            'floorsDescended': floors_descended,
            'intensityMinutesGoal': intensity_minutes_goal,
            'userFloorsAscendedGoal': user_floors_ascended_goal,
            'minHeartRate': min_heart_rate,
            'maxHeartRate': max_heart_rate,
            'restingHeartRate': resting_heart_rate,
            'lastSevenDaysAvgRestingHeartRate': last_seven_days_avg_resting_heart_rate,
            'source': source,
            'averageStressLevel': average_stress_level,
            'maxStressLevel': max_stress_level,
            'stressDuration': stress_duration,
            'restStressDuration': rest_stress_duration,
            'activityStressDuration': activity_stress_duration,
            'uncategorizedStressDuration': uncategorized_stress_duration,
            'totalStressDuration': total_stress_duration,
            'lowStressDuration': low_stress_duration,
            'mediumStressDuration': medium_stress_duration,
            'highStressDuration': high_stress_duration,
            'stressPercentage': stress_percentage,
            'restStressPercentage': rest_stress_percentage,
            'activityStressPercentage': activity_stress_percentage,
            'uncategorizedStressPercentage': uncategorized_stress_percentage,
            'lowStressPercentage': low_stress_percentage,
            'mediumStressPercentage': medium_stress_percentage,
            'highStressPercentage': high_stress_percentage,
            'stressQualifier': stress_qualifier,
            'measurableAwakeDuration': measurable_awake_duration,
            'measurableAsleepDuration': measurable_asleep_duration,
            'lastSyncTimestampGMT': last_sync_timestamp_gmt,
            'minAvgHeartRate': min_avg_heart_rate,
            'maxAvgHeartRate': max_avg_heart_rate,
            'bodyBatteryChargedValue': body_battery_charged_value,
            'bodyBatteryDrainedValue': body_battery_drained_value,
            'bodyBatteryHighestValue': body_battery_highest_value,
            'bodyBatteryLowestValue': body_battery_lowest_value,
            'bodyBatteryMostRecentValue': body_battery_most_recent_value,
            'bodyBatteryDuringSleep': body_battery_during_sleep,
            'bodyBatteryVersion': body_battery_version,
            'abnormalHeartRateAlertsCount': abnormal_heart_rate_alerts_count,
            'averageSpo2': average_spo2,
            'lowestSpo2': lowest_spo2,
            'latestSpo2': latest_spo2,
            'latestSpo2ReadingTimeGmt': latest_spo2_reading_time_gmt,
            'latestSpo2ReadingTimeLocal': latest_spo2_reading_time_local,
            'averageMonitoringEnvironmentAltitude': average_monitoring_environment_altitude,
            'restingCaloriesFromActivity': resting_calories_from_activity,
            'avgWakingRespirationValue': avg_waking_respiration_value,
            'highestRespirationValue': highest_respiration_value,
            'lowestRespirationValue': lowest_respiration_value,
            'latestRespirationValue': latest_respiration_value,
            'latestRespirationTimeGMT': latest_respiration_time_gmt
        }

        stats_data.append(stats_entry)

    return stats_data

def get_user_summary_data(start_date, num_days):
    """Generate synthetic user summary data for a specified date range.

    This function generates synthetic user summary data for a given date range. The generated data includes
    various user-related metrics and information for each day within the specified range.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which to generate user summary data.
    :type num_days: int
    :return: A list of dictionaries, where each dictionary represents user summary data for a single day.
        Each dictionary contains various user-related metrics and information.
    :rtype: List[Dict]
    """
    user_summary_data = []

    for _ in range(num_days):
        user_profile_id = random.randint(10000000, 99999999)
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')
        total_kilocalories = random.uniform(1500.0, 2500.0)
        active_kilocalories = random.uniform(400.0, 800.0)
        bmr_kilocalories = random.uniform(1000.0, 1500.0)
        wellness_kilocalories = total_kilocalories
        burned_kilocalories = None
        consumed_kilocalories = None
        remaining_kilocalories = total_kilocalories
        total_steps = random.randint(3000, 10000)
        net_calorie_goal = None
        total_distance_meters = random.randint(2000, 6000)
        wellness_distance_meters = total_distance_meters
        wellness_active_kilocalories = active_kilocalories
        net_remaining_kilocalories = active_kilocalories
        user_daily_summary_id = user_profile_id
        rule = {'typeId': 3, 'typeKey': 'subscribers'}
        uuid = 'e933a2a5aa214d3088bec955ea84c9bf'
        daily_step_goal = random.randint(1000, 5000)
        wellness_start_time_gmt = f"{calendar_date}T07:00:00.0"
        wellness_start_time_local = f"{calendar_date}T00:00:00.0"
        wellness_end_time_gmt = f"{(datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=_ + 1)).strftime('%Y-%m-%d')}T07:00:00.0"
        wellness_end_time_local = f"{(datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=_ + 1)).strftime('%Y-%m-%d')}T00:00:00.0"
        duration_in_milliseconds = 86400000
        wellness_description = None
        highly_active_seconds = random.randint(500, 1500)
        active_seconds = random.randint(4000, 7000)
        sedentary_seconds = random.randint(30000, 60000)
        sleeping_seconds = random.randint(20000, 40000)
        includes_wellness_data = True
        includes_activity_data = False
        includes_calorie_consumed_data = False
        privacy_protected = False
        moderate_intensity_minutes = random.randint(0, 60)
        vigorous_intensity_minutes = random.randint(0, 60)
        floors_ascended_in_meters = random.uniform(0.0, 30.0)
        floors_descended_in_meters = random.uniform(0.0, 20.0)
        floors_ascended = random.uniform(0.0, 10.0)
        floors_descended = random.uniform(0.0, 5.0)
        intensity_minutes_goal = random.randint(100, 200)
        user_floors_ascended_goal = random.randint(5, 15)
        min_heart_rate = random.randint(50, 70)
        max_heart_rate = random.randint(120, 150)
        resting_heart_rate = random.randint(60, 80)
        last_seven_days_avg_resting_heart_rate = resting_heart_rate
        source = 'GARMIN'
        average_stress_level = random.uniform(20.0, 60.0)
        max_stress_level = random.uniform(70.0, 100.0)
        stress_duration = random.randint(10000, 40000)
        rest_stress_duration = random.randint(9000, 35000)
        activity_stress_duration = random.randint(1000, 5000)
        uncategorized_stress_duration = random.randint(500, 2000)
        total_stress_duration = random.randint(10000, 40000)
        low_stress_duration = random.randint(4000, 15000)
        medium_stress_duration = random.randint(1000, 5000)
        high_stress_duration = random.randint(500, 3000)
        stress_percentage = random.uniform(10.0, 60.0)
        rest_stress_percentage = random.uniform(10.0, 50.0)
        activity_stress_percentage = random.uniform(5.0, 20.0)
        uncategorized_stress_percentage = random.uniform(2.0, 15.0)
        low_stress_percentage = random.uniform(5.0, 25.0)
        medium_stress_percentage = random.uniform(2.0, 15.0)
        high_stress_percentage = random.uniform(1.0, 10.0)
        stress_qualifier = 'BALANCED'
        measurable_awake_duration = random.randint(30000, 60000)
        measurable_asleep_duration = random.randint(20000, 40000)
        last_sync_timestamp_gmt = None
        min_avg_heart_rate = random.randint(50, 70)
        max_avg_heart_rate = random.randint(120, 150)
        body_battery_charged_value = random.randint(30, 60)
        body_battery_drained_value = random.randint(10, 40)
        body_battery_highest_value = random.randint(40, 70)
        body_battery_lowest_value = random.randint(0, 30)
        body_battery_most_recent_value = random.randint(10, 40)
        body_battery_during_sleep = None
        body_battery_version = 2.0
        abnormal_heart_rate_alerts_count = None
        average_spo2 = None
        lowest_spo2 = None
        latest_spo2 = None
        latest_spo2_reading_time_gmt = None
        latest_spo2_reading_time_local = None
        average_monitoring_environment_altitude = random.uniform(-200.0, 200.0)
        resting_calories_from_activity = None
        avg_waking_respiration_value = random.uniform(10.0, 20.0)
        highest_respiration_value = random.uniform(15.0, 25.0)
        lowest_respiration_value = random.uniform(5.0, 15.0)
        latest_respiration_value = random.uniform(15.0, 25.0)
        latest_respiration_time_gmt = wellness_end_time_gmt

        user_summary_entry = {
            'userProfileId': user_profile_id,
            'totalKilocalories': total_kilocalories,
            'activeKilocalories': active_kilocalories,
            'bmrKilocalories': bmr_kilocalories,
            'wellnessKilocalories': wellness_kilocalories,
            'burnedKilocalories': burned_kilocalories,
            'consumedKilocalories': consumed_kilocalories,
            'remainingKilocalories': remaining_kilocalories,
            'totalSteps': total_steps,
            'netCalorieGoal': net_calorie_goal,
            'totalDistanceMeters': total_distance_meters,
            'wellnessDistanceMeters': wellness_distance_meters,
            'wellnessActiveKilocalories': wellness_active_kilocalories,
            'netRemainingKilocalories': net_remaining_kilocalories,
            'userDailySummaryId': user_daily_summary_id,
            'calendarDate': calendar_date,
            'rule': rule,
            'uuid': uuid,
            'dailyStepGoal': daily_step_goal,
            'wellnessStartTimeGmt': wellness_start_time_gmt,
            'wellnessStartTimeLocal': wellness_start_time_local,
            'wellnessEndTimeGmt': wellness_end_time_gmt,
            'wellnessEndTimeLocal': wellness_end_time_local,
            'durationInMilliseconds': duration_in_milliseconds,
            'wellnessDescription': wellness_description,
            'highlyActiveSeconds': highly_active_seconds,
            'activeSeconds': active_seconds,
            'sedentarySeconds': sedentary_seconds,
            'sleepingSeconds': sleeping_seconds,
            'includesWellnessData': includes_wellness_data,
            'includesActivityData': includes_activity_data,
            'includesCalorieConsumedData': includes_calorie_consumed_data,
            'privacyProtected': privacy_protected,
            'moderateIntensityMinutes': moderate_intensity_minutes,
            'vigorousIntensityMinutes': vigorous_intensity_minutes,
            'floorsAscendedInMeters': floors_ascended_in_meters,
            'floorsDescendedInMeters': floors_descended_in_meters,
            'floorsAscended': floors_ascended,
            'floorsDescended': floors_descended,
            'intensityMinutesGoal': intensity_minutes_goal,
            'userFloorsAscendedGoal': user_floors_ascended_goal,
            'minHeartRate': min_heart_rate,
            'maxHeartRate': max_heart_rate,
            'restingHeartRate': resting_heart_rate,
            'lastSevenDaysAvgRestingHeartRate': last_seven_days_avg_resting_heart_rate,
            'source': source,
            'averageStressLevel': average_stress_level,
            'maxStressLevel': max_stress_level,
            'stressDuration': stress_duration,
            'restStressDuration': rest_stress_duration,
            'activityStressDuration': activity_stress_duration,
            'uncategorizedStressDuration': uncategorized_stress_duration,
            'totalStressDuration': total_stress_duration,
            'lowStressDuration': low_stress_duration,
            'mediumStressDuration': medium_stress_duration,
            'highStressDuration': high_stress_duration,
            'stressPercentage': stress_percentage,
            'restStressPercentage': rest_stress_percentage,
            'activityStressPercentage': activity_stress_percentage,
            'uncategorizedStressPercentage': uncategorized_stress_percentage,
            'lowStressPercentage': low_stress_percentage,
            'mediumStressPercentage': medium_stress_percentage,
            'highStressPercentage': high_stress_percentage,
            'stressQualifier': stress_qualifier,
            'measurableAwakeDuration': measurable_awake_duration,
            'measurableAsleepDuration': measurable_asleep_duration,
            'lastSyncTimestampGMT': last_sync_timestamp_gmt,
            'minAvgHeartRate': min_avg_heart_rate,
            'maxAvgHeartRate': max_avg_heart_rate,
            'bodyBatteryChargedValue': body_battery_charged_value,
            'bodyBatteryDrainedValue': body_battery_drained_value,
            'bodyBatteryHighestValue': body_battery_highest_value,
            'bodyBatteryLowestValue': body_battery_lowest_value,
            'bodyBatteryMostRecentValue': body_battery_most_recent_value,
            'bodyBatteryDuringSleep': body_battery_during_sleep,
            'bodyBatteryVersion': body_battery_version,
            'abnormalHeartRateAlertsCount': abnormal_heart_rate_alerts_count,
            'averageSpo2': average_spo2,
            'lowestSpo2': lowest_spo2,
            'latestSpo2': latest_spo2,
            'latestSpo2ReadingTimeGmt': latest_spo2_reading_time_gmt,
            'latestSpo2ReadingTimeLocal': latest_spo2_reading_time_local,
            'averageMonitoringEnvironmentAltitude': average_monitoring_environment_altitude,
            'restingCaloriesFromActivity': resting_calories_from_activity,
            'avgWakingRespirationValue': avg_waking_respiration_value,
            'highestRespirationValue': highest_respiration_value,
            'lowestRespirationValue': lowest_respiration_value,
            'latestRespirationValue': latest_respiration_value,
            'latestRespirationTimeGMT': latest_respiration_time_gmt
        }

        user_summary_data.append(user_summary_entry)

    return user_summary_data

def get_body_composition_data(start_date, num_days):
    """Generate synthetic body composition data for a specified date range.

    This function generates synthetic body composition data for a given date range. The generated data includes
    various body composition metrics such as weight, BMI, body fat percentage, and more.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which to generate body composition data.
    :type num_days: int
    :return: A dictionary containing body composition data for the specified date range, including weight, BMI,
        body fat percentage, and other metrics.
    :rtype: Dict
    """
    body_composition_data = {
        'startDate': start_date,
        'endDate': (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=num_days - 1)).strftime("%Y-%m-%d"),
        'dateWeightList': [],
        'totalAverage': {
            'from': datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000,
            'until': (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=num_days)).timestamp() * 1000,
            'weight': [],
            'bmi': [],
            'bodyFat': [],
            'bodyWater': [],
            'boneMass': [],
            'muscleMass': [],
            'physiqueRating': [],
            'visceralFat': [],
            'metabolicAge': [],
        }
    }

    for day in range(num_days):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day)).strftime("%Y-%m-%d")

        weight = random.uniform(50, 100)
        bmi = random.uniform(18, 30)
        body_fat = random.uniform(10, 25)
        body_water = random.uniform(45, 65)
        bone_mass = random.uniform(1, 3)
        muscle_mass = random.uniform(20, 50)
        physique_rating = random.randint(1, 5)
        visceral_fat = random.uniform(1, 15)
        metabolic_age = random.randint(18, 70)

        body_composition_data['dateWeightList'].append({
            'date': date,
            'weight': weight
        })

        body_composition_data['totalAverage']['weight'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': weight
        })

        body_composition_data['totalAverage']['bmi'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': bmi
        })

        body_composition_data['totalAverage']['bodyFat'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': body_fat
        })

        body_composition_data['totalAverage']['bodyWater'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': body_water
        })

        body_composition_data['totalAverage']['boneMass'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': bone_mass
        })

        body_composition_data['totalAverage']['muscleMass'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': muscle_mass
        })

        body_composition_data['totalAverage']['physiqueRating'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': physique_rating
        })

        body_composition_data['totalAverage']['visceralFat'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': visceral_fat
        })

        body_composition_data['totalAverage']['metabolicAge'].append({
            'timestamp': datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000,
            'value': metabolic_age
        })

    return body_composition_data


def get_heart_rate_data(start_date, num_days):
    """Generate synthetic heart rate data for a specified date range.

    This function generates synthetic heart rate data for a given date range, including various heart rate metrics
    such as resting heart rate, maximum heart rate, minimum heart rate, and additional descriptors and values.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which to generate heart rate data.
    :type num_days: int
    :return: A list of dictionaries, each containing heart rate data for a specific day, including resting heart rate,
        maximum and minimum heart rate, and additional heart rate descriptors and values.
    :rtype: List[Dict]
    """
    heart_rate_data = []

    for _ in range(num_days):
        user_profile_pk = random.randint(10000000, 99999999)
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')
        start_timestamp_gmt = f"{calendar_date}T07:00:00.0"
        end_timestamp_gmt = (datetime.strptime(start_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0") + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.0")
        start_timestamp_local = f"{calendar_date}T00:00:00.0"
        end_timestamp_local = (datetime.strptime(start_timestamp_local, "%Y-%m-%dT%H:%M:%S.0") + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.0")

        # Randomly generate resting heart rate within a reasonable range (e.g., 50-90)
        resting_heart_rate = random.randint(50, 90)

        # Generate max and min heart rates higher than resting heart rate
        max_heart_rate = random.randint(resting_heart_rate + 5, 120)
        min_heart_rate = random.randint(resting_heart_rate + 2, max_heart_rate - 1)

        # Slightly vary last seven days' average resting heart rate
        last_seven_days_avg = random.randint(resting_heart_rate - 2, resting_heart_rate + 2)

        # Generate some sample heart rate descriptors and values for demonstration
        heart_rate_descriptors = ['Descriptor1', 'Descriptor2', 'Descriptor3']
        heart_rate_values = [70, 80, 90]

        heart_rate_entry = {
            'userProfilePK': user_profile_pk,
            'calendarDate': calendar_date,
            'startTimestampGMT': start_timestamp_gmt,
            'endTimestampGMT': end_timestamp_gmt,
            'startTimestampLocal': start_timestamp_local,
            'endTimestampLocal': end_timestamp_local,
            'maxHeartRate': max_heart_rate,
            'minHeartRate': min_heart_rate,
            'restingHeartRate': resting_heart_rate,
            'lastSevenDaysAvgRestingHeartRate': last_seven_days_avg,
            'heartRateValueDescriptors': heart_rate_descriptors,
            'heartRateValues': heart_rate_values
        }

        heart_rate_data.append(heart_rate_entry)

    return heart_rate_data


def get_training_readiness_data(start_date, num_entries):
    """Generate synthetic training readiness data for a specified date range.

    This function generates synthetic training readiness data for a specified number of days, including various metrics
    related to an individual's readiness for training or physical activity. The data includes factors such as sleep score,
    recovery time, ACWR (Acute Chronic Workload Ratio), HRV (Heart Rate Variability), and additional feedback metrics.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_entries: The number of training readiness entries to generate.
    :type num_entries: int
    :return: A list of dictionaries, each containing training readiness data for a specific day, including metrics like
        sleep score, recovery time, ACWR factor, HRV factor, and associated feedback.
    :rtype: List[Dict]
    """
    training_readiness_data = []

    for _ in range(num_entries):
        user_profile_pk = random.randint(10000000, 99999999)
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')

        timestamp = f"{calendar_date}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}.0"
        timestamp_local = (datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.0") + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%S.0")

        deviceId = random.randint(1000000000, 9999999999)

        # Randomly select a level from a list of possible levels
        levels = ['LOW', 'MODERATE', 'HIGH', 'VERY_HIGH', 'MAXIMUM', 'NONE']
        level = random.choice(levels)

        # Set some consistent values for feedback
        feedback_long = 'UNKNOWN'
        feedback_short = 'UNKNOWN'

        # Randomize sleep score, sleep score factor, and associated feedback
        sleep_score = random.randint(50, 100)
        sleep_score_factor_percent = random.randint(0, 100)
        sleep_score_factor_feedback = level if sleep_score_factor_percent > 60 else 'NONE'

        # Randomize recovery time, recovery time factor, and associated feedback
        recovery_time = random.randint(1, 10)
        recovery_time_factor_percent = random.randint(0, 100)
        recovery_time_factor_feedback = level if recovery_time_factor_percent < 40 else 'NONE'

        # Randomize ACWR (Acute Chronic Workload Ratio) factor and feedback
        acwr_factor_percent = random.randint(0, 100)
        acwr_factor_feedback = level if acwr_factor_percent > 60 else 'NONE'

        # Randomize HRV (Heart Rate Variability) factor and feedback
        hrv_factor_percent = random.randint(0, 100)
        hrv_factor_feedback = level if hrv_factor_percent < 40 else 'NONE'

        # Randomize HRV weekly average
        hrv_weekly_average = random.randint(50, 100)

        # Randomize sleep history factor and feedback
        sleep_history_factor_percent = random.randint(0, 100)
        sleep_history_factor_feedback = level if sleep_history_factor_percent < 40 else 'NONE'

        # Set valid sleep to True
        valid_sleep = True

        # Set recovery time change phrase to None
        recovery_time_change_phrase = None

        entry = {
            'userProfilePK': user_profile_pk,
            'calendarDate': calendar_date,
            'timestamp': timestamp,
            'timestampLocal': timestamp_local,
            'deviceId': deviceId,
            'level': level,
            'feedbackLong': feedback_long,
            'feedbackShort': feedback_short,
            'sleepScore': sleep_score,
            'sleepScoreFactorPercent': sleep_score_factor_percent,
            'sleepScoreFactorFeedback': sleep_score_factor_feedback,
            'recoveryTime': recovery_time,
            'recoveryTimeFactorPercent': recovery_time_factor_percent,
            'recoveryTimeFactorFeedback': recovery_time_factor_feedback,
            'acwrFactorPercent': acwr_factor_percent,
            'acwrFactorFeedback': acwr_factor_feedback,
            'hrvFactorPercent': hrv_factor_percent,
            'hrvFactorFeedback': hrv_factor_feedback,
            'hrvWeeklyAverage': hrv_weekly_average,
            'sleepHistoryFactorPercent': sleep_history_factor_percent,
            'sleepHistoryFactorFeedback': sleep_history_factor_feedback,
            'validSleep': valid_sleep,
            'recoveryTimeChangePhrase': recovery_time_change_phrase,
        }

        training_readiness_data.append(entry)

    return training_readiness_data

def get_blood_pressure_data(start_date, end_date, num_summaries):
    """Generate synthetic blood pressure data for a specified date range.

    This function generates synthetic blood pressure data, including systolic, diastolic, and heart rate measurements
    for a specified date range. The generated data is structured as a dictionary.

    :param start_date: The starting date for the blood pressure data.
    :type start_date: str (in the format '%Y-%m-%d')

    :param end_date: The ending date for the blood pressure data.
    :type end_date: str (in the format '%Y-%m-%d')

    :param num_summaries: The number of daily blood pressure summaries to generate within the date range.
    :type num_summaries: int

    :return: A dictionary containing synthetic blood pressure data for the specified date range.
    :rtype: Dict
    """
    blood_pressure_data = {
        'from': start_date,
        'until': end_date,
        'measurementSummaries': [],
        'categoryStats': None
    }

    for _ in range(num_summaries):
        summary_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')
        systolic = random.randint(90, 160)
        diastolic = random.randint(60, 100)
        heart_rate = random.randint(60, 100)

        summary = {
            'date': summary_date,
            'systolic': systolic,
            'diastolic': diastolic,
            'heartRate': heart_rate
        }

        blood_pressure_data['measurementSummaries'].append(summary)

    return blood_pressure_data


def get_floors_data(start_date, end_date):
    """Generate synthetic floors climbed data for a specified date range.

    This function generates synthetic data for the number of floors climbed for each day within the specified date range.
    The data includes descriptors and floor values for each day, and the date range is determined by the start and end dates.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param end_date: The end date in the format 'YYYY-MM-DD'.
    :type end_date: str
    :return: A dictionary containing the start and end timestamps, a list of descriptors, and an array of floor values
        for each day within the specified date range.
    :rtype: Dict
    """
    floors_data = {
        'startTimestampGMT': f'{start_date}T07:00:00.0',
        'endTimestampGMT': f'{end_date}T07:00:00.0',
        'startTimestampLocal': f'{start_date}T00:00:00.0',
        'endTimestampLocal': f'{end_date}T00:00:00.0',
        'floorsValueDescriptorDTOList': [],
        'floorValuesArray': []
    }

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    while current_date <= datetime.strptime(end_date, "%Y-%m-%d"):
        descriptor = {
            'date': current_date.strftime('%Y-%m-%d'),
            'descriptor': f'Descriptor for {current_date.strftime("%Y-%m-%d")}',
        }

        floor_value = {
            'date': current_date.strftime('%Y-%m-%d'),
            'value': random.randint(0, 10),
        }

        floors_data['floorsValueDescriptorDTOList'].append(descriptor)
        floors_data['floorValuesArray'].append(floor_value)

        current_date += timedelta(days=1)

    return floors_data

def get_training_status_data(start_date, num_days):
    """Generate synthetic training status data for a specified date range.

    This function generates synthetic training status data for a specified number of days starting from the provided
    start date. Each day's data includes information about the user's training status, VO2 max, training load balance,
    and heat/altitude acclimation. The generated data is stored in a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which training status data is generated.
    :type num_days: int
    :return: A list of dictionaries, each containing user-specific training status information for a single day.
    :rtype: List[Dict]
    """
    training_status_data = []

    for _ in range(num_days):
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')
        entry = {
            'userId': random.randint(10000000, 99999999),
            'mostRecentVO2Max': None,
            'mostRecentTrainingLoadBalance': None,
            'mostRecentTrainingStatus': None,
            'heatAltitudeAcclimationDTO': None
        }
        training_status_data.append(entry)

    return training_status_data

def get_resting_hr_data(start_date, end_date):
    """Generate synthetic resting heart rate data for a specified date range.

    This function generates synthetic resting heart rate data for a specified date range, including the user's profile
    ID, the start and end dates, and the resting heart rate values for each day within the range. The generated data is
    structured as a dictionary.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param end_date: The end date in the format 'YYYY-MM-DD'.
    :type end_date: str
    :return: A dictionary containing user-specific resting heart rate data within the specified date range.
    :rtype: Dict
    """
    resting_hr_data = {
        'userProfileId': random.randint(10000000, 99999999),
        'statisticsStartDate': start_date,
        'statisticsEndDate': end_date,
        'allMetrics': {
            'metricsMap': []
        }
    }

    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_date:
        calendar_date = current_date.strftime('%Y-%m-%d')
        value = random.uniform(60.0, 75.0)  # You can adjust the range for resting heart rate values
        metric_entry = {
            'value': value,
            'calendarDate': calendar_date
        }
        resting_hr_data['allMetrics']['metricsMap'].append({
            'WELLNESS_RESTING_HEART_RATE': [metric_entry]
        })
        current_date += timedelta(days=1)

    return resting_hr_data

def get_hydration_data(start_date, num_days):
    """Generate synthetic hydration data for a specified number of days.

    This function generates synthetic hydration data for a specified number of days, including the user's ID,
    the calendar date, hydration values, goals, daily averages, and additional hydration-related metrics. The generated
    data is structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which hydration data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing user-specific hydration data for the specified number of days.
    :rtype: List[Dict]
    """
    hydration_data = []

    for _ in range(num_days):
        user_id = random.randint(10000000, 99999999)
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')
        value_in_ml = None  # You can randomize this value if needed
        goal_in_ml = random.uniform(1800.0, 2500.0)  # Random goal between 1800 mL and 2500 mL
        daily_average_in_ml = None  # You can randomize this value if needed
        last_entry_timestamp_local = None
        sweat_loss_in_ml = None  # You can randomize this value if needed
        activity_intake_in_ml = None  # You can randomize this value if needed

        hydration_entry = {
            'userId': user_id,
            'calendarDate': calendar_date,
            'valueInML': value_in_ml,
            'goalInML': goal_in_ml,
            'dailyAverageinML': daily_average_in_ml,
            'lastEntryTimestampLocal': last_entry_timestamp_local,
            'sweatLossInML': sweat_loss_in_ml,
            'activityIntakeInML': activity_intake_in_ml
        }

        hydration_data.append(hydration_entry)

    return hydration_data

def get_sleep_data(start_date, num_days):
    """Generate synthetic sleep data for a specified number of days.

    This function generates synthetic sleep data for a specified number of days, including details such as sleep duration,
    sleep stages (deep, light, REM), and sleep quality metrics. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which sleep data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing user-specific sleep data for the specified number of days.
    :rtype: List[Dict]
    """
    sleep_data = []

    for i in range(num_days):
        date = (datetime.strptime(start_date, "%Y-%m-%d")  + timedelta(days=i)).strftime('%Y-%m-%d')
        sleep_time_seconds = random.randint(18000, 32400)  # Random sleep time between 5 and 9 hours

        sleep_entry = {
            'dailySleepDTO': {
                'id': random.randint(1000000000000, 9999999999999),
                'userProfilePK': 85412302,
                'calendarDate': date,
                'sleepTimeSeconds': sleep_time_seconds,
                'napTimeSeconds': 0,  # No naps
                'sleepWindowConfirmed': True,
                'sleepWindowConfirmationType': 'enhanced_confirmed_final',
                'sleepStartTimestampGMT': 0,  # You can add the actual timestamps if needed
                'sleepEndTimestampGMT': 0,
                'sleepStartTimestampLocal': 0,
                'sleepEndTimestampLocal': 0,
                'autoSleepStartTimestampGMT': None,
                'autoSleepEndTimestampGMT': None,
                'sleepQualityTypePK': None,
                'sleepResultTypePK': None,
                'unmeasurableSleepSeconds': 0,
                'deepSleepSeconds': random.randint(6000, 9000),  # Random deep sleep between 1.5 and 2.5 hours
                'lightSleepSeconds': random.randint(12000, 20000),  # Random light sleep between 3 and 5 hours
                'remSleepSeconds': random.randint(1200, 3600),  # Random REM sleep between 20 and 60 minutes
                'awakeSleepSeconds': random.randint(1800, 4800),  # Random awake time between 30 minutes and 1 hour 20 minutes
                'deviceRemCapable': True,
                'retro': False,
                'sleepFromDevice': True,
                'averageRespirationValue': random.uniform(12.0, 23.0),  # Random respiration value between 12 and 23
                'lowestRespirationValue': random.uniform(12.0, 23.0),
                'highestRespirationValue': random.uniform(12.0, 23.0),
                'awakeCount': random.randint(0, 4),  # Random awake count between 0 and 4
                'avgSleepStress': random.uniform(0.0, 30.0),  # Random stress level between 0 and 30
                'ageGroup': 'ADULT',
                'sleepScoreFeedback': 'NEGATIVE_LONG_BUT_NOT_ENOUGH_REM',
                'sleepScoreInsight': 'NONE',
                'sleepScores': {
                    'totalDuration': {'qualifierKey': 'GOOD', 'optimalStart': 28800.0, 'optimalEnd': 28800.0},
                    'stress': {'qualifierKey': 'FAIR', 'optimalStart': 0.0, 'optimalEnd': 15.0},
                    'awakeCount': {'qualifierKey': 'POOR', 'optimalStart': 0.0, 'optimalEnd': 1.0},
                    'overall': {'value': random.randint(50, 90), 'qualifierKey': 'FAIR'},
                    'remPercentage': {'value': random.randint(5, 30), 'qualifierKey': 'POOR', 'optimalStart': 21.0, 'optimalEnd': 31.0, 'idealStartInSeconds': random.randint(4000, 8000), 'idealEndInSeconds': random.randint(6000, 8000)},
                    'restlessness': {'qualifierKey': 'FAIR', 'optimalStart': 0.0, 'optimalEnd': 5.0},
                    'lightPercentage': {'value': random.randint(30, 70), 'qualifierKey': 'GOOD', 'optimalStart': 30.0, 'optimalEnd': 64.0, 'idealStartInSeconds': random.randint(6000, 16000), 'idealEndInSeconds': random.randint(12000, 22000)},
                    'deepPercentage': {'value': random.randint(10, 40), 'qualifierKey': 'EXCELLENT', 'optimalStart': 16.0, 'optimalEnd': 33.0, 'idealStartInSeconds': random.randint(3000, 7000), 'idealEndInSeconds': random.randint(6000, 9000)},
                },
                'sleepVersion': 2,
            },
            'sleepMovement': None,
            'remSleepData': True,
            'sleepLevels': None,
            'restingHeartRate': 63,
        }

        sleep_data.append(sleep_entry)  # Append the generated sleep data

    return sleep_data

def get_earned_badges_data(start_date, num_days):
    """Generate synthetic earned badges data for a specified number of days.

    This function generates synthetic earned badges data for a specified number of days. It simulates users earning
    badges in various categories with random names. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which earned badges data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing information about badges earned by users for the specified number of days.
    :rtype: List[Dict]
    """
    earned_badges_data = []

    badge_categories = ['Category A', 'Category B', 'Category C']
    badge_names = ['Badge 1', 'Badge 2', 'Badge 3']

    for i in range(num_days):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime('%Y-%m-%m')
        num_badges = random.randint(0, 3)  # Random number of badges earned for each day (0 to 3)

        for _ in range(num_badges):
            badge_id = random.randint(1, 100)
            badge_category = random.choice(badge_categories)
            badge_name = random.choice(badge_names)
            badge_earned_date = date

            earned_badge_entry = {
                'badgeId': badge_id,
                'badgeCategory': badge_category,
                'badgeName': badge_name,
                'badgeEarnedDate': badge_earned_date,
            }

            earned_badges_data.append(earned_badge_entry)  # Append the generated earned badge data

    return earned_badges_data


def get_stress_data(start_date, num_days):
    """Generate synthetic stress data for a specified number of days.

    This function generates synthetic stress data for a specified number of days. It simulates stress levels of users
    with random values. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which stress data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing information about stress levels for the specified number of days.
    :rtype: List[Dict]
    """
    stress_data = []

    for i in range(num_days):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime('%Y-%m-%d')

        stress_entry = {
            'userProfilePK': 85412302,
            'calendarDate': date,
            'startTimestampGMT': f'{date}T07:00:00.0',
            'endTimestampGMT': f'{date}T07:00:00.0',
            'startTimestampLocal': f'{date}T00:00:00.0',
            'endTimestampLocal': f'{date}T00:00:00.0',
            'maxStressLevel': random.randint(70, 100),  # Random stress level between 70 and 100
            'avgStressLevel': random.randint(20, 50),  # Random average stress level between 20 and 50
            'stressChartValueOffset': 1,
            'stressChartYAxisOrigin': -1,
            'stressValueDescriptorsDTOList': [],
            'stressValuesArray': [],
        }

        stress_data.append(stress_entry)  # Append the generated stress data

    return stress_data

def get_respiration_data(start_date, num_days):
    """Generate synthetic respiration data for a specified number of days.

    This function generates synthetic respiration data for a specified number of days. It simulates respiration values of users
    with random values. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which respiration data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing information about respiration values for the specified number of days.
    :rtype: List[Dict]
    """
    respiration_data = []

    for i in range(num_days):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime('%Y-%m-%d')

        respiration_entry = {
            'userProfilePK': 85412302,
            'calendarDate': date,
            'startTimestampGMT': f'{date}T07:00:00.0',
            'endTimestampGMT': f'{date}T07:00:00.0',
            'startTimestampLocal': f'{date}T00:00:00.0',
            'endTimestampLocal': f'{date}T00:00:00.0',
            'sleepStartTimestampGMT': f'{date}T05:53:00.0',
            'sleepEndTimestampGMT': f'{date}T13:48:00.0',
            'sleepStartTimestampLocal': f'{date}T22:53:00.0',
            'sleepEndTimestampLocal': f'{date}T06:48:00.0',
            'tomorrowSleepStartTimestampGMT': f'{date}T05:39:00.0',
            'tomorrowSleepEndTimestampGMT': f'{date}T14:16:00.0',
            'tomorrowSleepStartTimestampLocal': f'{date}T22:39:00.0',
            'tomorrowSleepEndTimestampLocal': f'{date}T07:16:00.0',
            'lowestRespirationValue': random.uniform(10.0, 15.0),  # Random lowest respiration value between 10 and 15
            'highestRespirationValue': random.uniform(20.0, 25.0),  # Random highest respiration value between 20 and 25
            'avgWakingRespirationValue': random.uniform(12.0, 18.0),  # Random average waking respiration value between 12 and 18
            'avgSleepRespirationValue': random.uniform(16.0, 22.0),  # Random average sleep respiration value between 16 and 22
            'avgTomorrowSleepRespirationValue': random.uniform(16.0, 22.0),  # Random average respiration value for tomorrow's sleep
            'respirationValueDescriptorsDTOList': [],
            'respirationValuesArray': [],
        }

        respiration_data.append(respiration_entry)  # Append the generated respiration data

    return respiration_data

def get_spo2_data(start_date, num_days):
    """Generate synthetic SpO2 (Oxygen Saturation) data for a specified number of days.

    This function generates synthetic SpO2 data for a specified number of days. It simulates SpO2 values of users with random values.
    The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which SpO2 data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing information about SpO2 values for the specified number of days.
    :rtype: List[Dict]
    """
    spo2_data = []

    for i in range(num_days):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime('%Y-%m-%d')

        spo2_entry = {
            'userProfilePK': 85412302,
            'calendarDate': date,
            'startTimestampGMT': f'{date}T07:00:00.0',
            'endTimestampGMT': f'{date}T07:00:00.0',
            'startTimestampLocal': f'{date}T00:00:00.0',
            'endTimestampLocal': f'{date}T00:00:00.0',
            'sleepStartTimestampGMT': f'{date}T05:53:00.0',
            'sleepEndTimestampGMT': f'{date}T13:48:00.0',
            'sleepStartTimestampLocal': f'{date}T22:53:00.0',
            'sleepEndTimestampLocal': f'{date}T06:48:00.0',
            'tomorrowSleepStartTimestampGMT': f'{date}T05:39:00.0',
            'tomorrowSleepEndTimestampGMT': f'{date}T14:16:00.0',
            'tomorrowSleepStartTimestampLocal': f'{date}T22:39:00.0',
            'tomorrowSleepEndTimestampLocal': f'{date}T07:16:00.0',
            'averageSpO2': random.uniform(92, 99),  # Random average SpO2 value between 92 and 99
            'lowestSpO2': random.uniform(88, 91),  # Random lowest SpO2 value between 88 and 91
            'lastSevenDaysAvgSpO2': random.uniform(93, 97),  # Random average SpO2 for the last 7 days
            'latestSpO2': random.uniform(90, 95),  # Random latest SpO2 value
            'latestSpO2TimestampGMT': f'{date}T08:00:00.0',
            'latestSpO2TimestampLocal': f'{date}T01:00:00.0',
            'avgSleepSpO2': random.uniform(93, 97),  # Random average SpO2 during sleep
            'avgTomorrowSleepSpO2': random.uniform(93, 97),  # Random average SpO2 for tomorrow's sleep
            'spO2ValueDescriptorsDTOList': None,
            'spO2SingleValues': None,
            'continuousReadingDTOList': None,
            'spO2HourlyAverages': None,
        }

        spo2_data.append(spo2_entry)  # Append the generated SpO2 data

    return spo2_data

def get_metrics_data(start_date, num_days):
    """Generate synthetic "max_metrics" data for a specified number of days.

    This function generates synthetic "max_metrics" data for a specified number of days. It simulates various metrics like
    vo2MaxPreciseValue and vo2MaxValue for users with random values. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which "max_metrics" data should be generated.
    :type num_days: int
    :return: A list of dictionaries containing "max_metrics" data for the specified number of days.
    :rtype: List[Dict]
    """
    max_metrics_data = []

    for i in range(num_days):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime('%Y-%m-%d')

        # Generate mock "max_metrics" data for each day
        max_metrics_entry = {
            'userId': 85412302,
            'generic': {
                'calendarDate': date,
                'vo2MaxPreciseValue': round(random.uniform(35.0, 41.0), 1),  # Random vo2MaxPreciseValue
                'vo2MaxValue': round(random.uniform(35.0, 41.0), 1),  # Random vo2MaxValue
                'fitnessAge': None,
                'fitnessAgeDescription': None,
                'maxMetCategory': 0
            },
            'cycling': None,
            'heatAltitudeAcclimation': None
        }

        max_metrics_data.append(max_metrics_entry)  # Append the generated "max_metrics" data

    return max_metrics_data

def random_datetime(start_date, end_date):
    """
    Generate a random datetime within a specified date range.

    This function generates a random datetime within the specified start and end dates.

    :param start_date: The start date as a datetime object.
    :type start_date: datetime.datetime
    :param end_date: The end date as a datetime object.
    :type end_date: datetime.datetime
    :return: A random datetime between start_date (inclusive) and end_date (exclusive).
    :rtype: datetime.datetime
    """
    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()
    random_timestamp = start_timestamp + random.random() * (end_timestamp - start_timestamp)
    return datetime.fromtimestamp(random_timestamp)

def get_personal_record_data(start_date, end_date, num_entries):
    """Generate synthetic personal record (PR) data for a specified date range and number of entries.

    This function generates synthetic personal record (PR) data for a specified date range and number of entries. Each PR
    entry contains information about the type, value, and timestamps. The generated data is structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param end_date: The end date in the format 'YYYY-MM-DD'.
    :type end_date: str
    :param num_entries: The number of PR entries to generate.
    :type num_entries: int
    :return: A list of dictionaries containing personal record (PR) data for the specified date range and number of entries.
    :rtype: List[Dict]
    """
    personal_record_data = []

    for _ in range(num_entries):
        entry = {
            'id': random.randint(1000000000, 9999999999),
            'typeId': random.randint(1, 16),
            'activityId': 0,
            'activityName': None,
            'activityType': None,
            'activityStartDateTimeInGMT': None,
            'actStartDateTimeInGMTFormatted': None,
            'activityStartDateTimeLocal': None,
            'activityStartDateTimeLocalFormatted': None,
            'value': round(random.uniform(10, 1000000), 2),
            'prTypeLabelKey': None,
            'poolLengthUnit': None,
        }

        entry['prStartTimeGmt'] = int(
            random_datetime(start_date, end_date).timestamp() * 1000
        )
        entry['prStartTimeGmtFormatted'] = datetime.utcfromtimestamp(
            entry['prStartTimeGmt'] / 1000
        ).strftime('%Y-%m-%dT%H:%M:%S.0')

        entry['prStartTimeLocal'] = int(
            random_datetime(start_date, end_date).timestamp() * 1000
        )
        entry['prStartTimeLocalFormatted'] = datetime.fromtimestamp(
            entry['prStartTimeLocal'] / 1000
        ).strftime('%Y-%m-%dT%H:%M:%S.0')

        personal_record_data.append(entry)

    return personal_record_data


def get_activities_data(start_date, num_days):
    """Generate synthetic activity data for a specified date range and number of days.

    This function generates synthetic activity data for a specified date range and number of days. Each activity entry
    includes details such as activity type, duration in minutes, calories burned, and timestamps. The generated data is
    structured as a list of dictionaries.

    :param start_date: The start date in the format 'YYYY-MM-DD'.
    :type start_date: str
    :param num_days: The number of days for which to generate activity data.
    :type num_days: int
    :return: A list of dictionaries containing synthetic activity data for the specified date range and number of days.
    :rtype: List[Dict]
    """
    activities_data = []

    for _ in range(num_days):
        # Generate random activity type, duration, and calories burned
        activity_type = random.choice(['Running', 'Cycling', 'Walking', 'Swimming', 'Yoga'])
        duration_minutes = random.randint(15, 120)
        calories_burned = random.uniform(100, 600)

        # Create date based on the start_date and current day index
        calendar_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=_)).strftime('%Y-%m-%d')

        # Generate random user_profile_pk
        user_profile_pk = random.randint(10000000, 99999999)

        # Generate random timestamps
        start_timestamp_gmt = f"{calendar_date}T07:00:00.0"
        end_timestamp_gmt = (datetime.strptime(start_timestamp_gmt, "%Y-%m-%dT%H:%M:%S.0") + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.0")
        start_timestamp_local = f"{calendar_date}T00:00:00.0"
        end_timestamp_local = (datetime.strptime(start_timestamp_local, "%Y-%m-%dT%H:%M:%S.0") + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.0")

        activity_entry = {
            'userProfilePK': user_profile_pk,
            'calendarDate': calendar_date,
            'startTimestampGMT': start_timestamp_gmt,
            'endTimestampGMT': end_timestamp_gmt,
            'startTimestampLocal': start_timestamp_local,
            'endTimestampLocal': end_timestamp_local,
            'activityType': activity_type,
            'durationMinutes': duration_minutes,
            'caloriesBurned': calories_burned
        }

        activities_data.append(activity_entry)

    return activities_data

def get_device_settings_data(num_devices):
    """Generate synthetic device settings data for the specified number of devices.

    This function generates synthetic device settings data for the specified number of devices. Each device's settings
    include various configuration options such as time format, units of measurement, activity tracking settings, alarm modes,
    language preferences, and more. The generated data is structured as a list of dictionaries.

    :param num_devices: The number of devices for which to generate settings data.
    :type num_devices: int

    :return: A list of dictionaries containing synthetic device settings data for the specified number of devices.
    :rtype: List[Dict]
    """
    device_settings = []

    # Generate random data for two devices
    for _ in range(num_devices):
        device_data = {
            'deviceId': random.randint(1000000000, 9999999999),
            'timeFormat': random.choice(['time_twelve_hr', 'time_twenty_four_hr']),
            'dateFormat': 'date_month_day',
            'measurementUnits': random.choice(['statute_us', 'metric']),
            'allUnits': 'statute_us' if random.choice([True, False]) else 'metric',
            'visibleScreens': None,
            'enabledScreens': {},
            'screenLists': None,
            'isVivohubEnabled': None,
            'alarms': [],
            'supportedAlarmModes': ['ON', 'OFF', 'DAILY', 'WEEKDAYS', 'WEEKENDS', 'ONCE'],
            'multipleAlarmEnabled': True,
            'maxAlarm': random.randint(0, 10),
            'activityTracking': {
                'activityTrackingEnabled': True,
                'moveAlertEnabled': True,
                'moveBarEnabled': None,
                'pulseOxSleepTrackingEnabled': random.choice([True, False]),
                'spo2Threshold': None,
                'lowSpo2AlertEnabled': None,
                'highHrAlertEnabled': random.choice([True, False]),
                'highHrAlertThreshold': random.randint(80, 130),
                'pulseOxAcclimationEnabled': random.choice([True, False]),
                'lowHrAlertEnabled': random.choice([True, False]),
                'lowHrAlertThreshold': random.randint(30, 70),
                'bloodEfficiencySleepTrackingEnabled': None,
                'bloodEfficiencyAcclimationEnabled': None
            },
            'keyTonesEnabled': None,
            'keyVibrationEnabled': None,
            'alertTonesEnabled': None,
            'userNoticeTonesEnabled': None,
            'glonassEnabled': None,
            'turnPromptEnabled': None,
            'segmentPromptEnabled': None,
            'supportedLanguages': [
                {'id': i, 'name': 'lang_{i}'}
                for i in range(40)
            ],
            'language': random.randint(0, 39),
            'supportedAudioPromptDialects': [
                'AR_AE', 'CS_CZ', 'DA_DK', 'DE_DE', 'EL_GR', 'EN_AU', 'EN_GB', 'EN_US', 'ES_ES',
                'ES_MX', 'FI_FI', 'FR_CA', 'FR_FR', 'HE_IL', 'HR_HR', 'HU_HU', 'ID_ID', 'IT_IT',
                'JA_JP', 'KO_KR', 'MS_MY', 'NL_NL', 'NO_NO', 'PL_PL', 'PT_BR', 'RO_RO', 'RU_RU',
                'SK_SK', 'SV_SE', 'TH_TH', 'TR_TR', 'VI_VI', 'ZH_CN', 'ZH_TW'
            ],
            'defaultPage': None,
            'displayOrientation': None,
            'mountingSide': 'RIGHT',
            'backlightMode': 'AUTO_BRIGHTNESS',
            'backlightSetting': 'ON',
            'customWheelSize': None,
            'gestureMode': None,
            'goalAnimation': 'NOT_IN_ACTIVITY',
            'autoSyncStepsBeforeSync': 2000,
            'autoSyncMinutesBeforeSync': 240,
            'bandOrientation': None,
            'screenOrientation': None,
            'duringActivity': {
                'screens': None,
                'defaultScreen': None,
                'smartNotificationsStatus': 'SHOW_ALL',
                'smartNotificationsSound': None,
                'phoneNotificationPrivacyMode': None
            },
            'phoneVibrationEnabled': None,
            'connectIQ': {
                'autoUpdate': True
            },
            'opticalHeartRateEnabled': True,
            'autoUploadEnabled': True,
            'bleConnectionAlertEnabled': None,
            'phoneNotificationMode': None,
            'lactateThresholdAutoDetectEnabled': None,
            'wiFiAutoUploadEnabled': None,
            'blueToothEnabled': None,
            'smartNotificationsStatus': 'SHOW_ALL',
            'smartNotificationsSound': None,
            'dndEnabled': random.choice([True, False]),
            'distanceUnit': None,
            'paceSpeedUnit': None,
            'elevationUnit': None,
            'weightUnit': None,
            'heightUnit': None,
            'temperatureUnit': None,
            'runningFormat': None,
            'cyclingFormat': None,
            'hikingFormat': None,
            'strengthFormat': None,
            'cardioFormat': None,
            'xcSkiFormat': None,
            'otherFormat': None,
            'startOfWeek': 'SUNDAY',
            'dataRecording': 'SMART',
            'soundVibrationEnabled': None,
            'soundInAppOnlyEnabled': None,
            'backlightKeysAndAlertsEnabled': None,
            'backlightWristTurnEnabled': None,
            'backlightTimeout': 'MEDIUM',
            'supportedBacklightTimeouts': None,
            'screenTimeout': None,
            'colorTheme': None,
            'autoActivityDetect': {
                'autoActivityDetectEnabled': True,
                'autoActivityStartEnabled': False,
                'runningEnabled': True,
                'cyclingEnabled': True,
                'swimmingEnabled': True,
                'walkingEnabled': True,
                'ellipticalEnabled': True,
                'drivingEnabled': True
            },
            'sleep': None,
            'screenMode': None,
            'watchFace': None,
            'watchFaceItemList': None,
            'multipleSupportedWatchFace': {},
            'supportedScreenModes': None,
            'supportedWatchFaces': None,
            'supportedWatchFaceColors': None,
            'autoSyncFrequency': None,
            'supportedBacklightSettings': ['AUTO_INTERACTION_ONLY', 'AUTO_INTERACTION_GESTURE', 'OFF'],
            'supportedColorThemes': None,
            'disableLastEnabledScreen': None,
            'nickname': None,
            'avatar': None,
            'controlsMenuList': [
                {'id': 'POWER_OFF', 'index': 0, 'required': True},
                {'id': 'PAYMENTS', 'index': 1, 'required': None},
                {'id': 'MUSIC_CONTROLS', 'index': 2, 'required': None},
                {'id': 'FIND_MY_PHONE', 'index': 3, 'required': None},
                {'id': 'SAVE_LOCATION', 'index': 4, 'required': None},
                {'id': 'DO_NOT_DISTURB', 'index': 5, 'required': None},
                {'id': 'BLUETOOTH', 'index': 6, 'required': None},
                {'id': 'STOPWATCH', 'index': 7, 'required': None},
                {'id': 'BRIGHTNESS', 'index': 8, 'required': None},
                {'id': 'LOCK_DEVICE', 'index': 9, 'required': None},
                {'id': 'SYNC', 'index': None, 'required': None},
                {'id': 'SET_TIME', 'index': None, 'required': None},
                {'id': 'ALARMS', 'index': None, 'required': None},
                {'id': 'TIMER', 'index': None, 'required': None},
                {'id': 'FLASHLIGHT', 'index': None, 'required': None}
            ],
            'customUserText': None,
            'metricsFileTrueupEnabled': True,
            'relaxRemindersEnabled': True,
            'smartNotificationTimeout': 'MEDIUM',
            'intensityMinutesCalcMethod': 'AUTO',
            'moderateIntensityMinutesHrZone': 3,
            'vigorousIntensityMinutesHrZone': 4,
            'keepUserNamePrivate': None,
            'audioPromptLapEnabled': False,
            'audioPromptSpeedPaceEnabled': False,
            'audioPromptSpeedPaceType': 'AVERAGE',
            'audioPromptSpeedPaceFrequency': 'INVALID',
            'audioPromptSpeedPaceDuration': 180,
            'audioPromptHeartRateEnabled': False,
            'audioPromptHeartRateType': 'HEART_RATE',
            'audioPromptHeartRateFrequency': 'INVALID',
            'audioPromptHeartRateDuration': 180,
            'audioPromptDialectType': None,
            'audioPromptActivityAlertsEnabled': False,
            'audioPromptPowerEnabled': False,
            'audioPromptPowerType': 'AVERAGE',
            'audioPromptPowerFrequency': 'INVALID',
            'audioPromptPowerDuration': 180,
            'weightOnlyModeEnabled': None,
            'phoneNotificationPrivacyMode': 'OFF',
            'diveAlerts': None,
            'liveEventSharingEnabled': None,
            'liveTrackEnabled': None,
            'liveEventSharingEndTimestamp': None,
            'liveEventSharingMsgContents': None,
            'liveEventSharingTargetDistance': None,
            'liveEventSharingMsgTriggers': None,
            'liveEventSharingTriggerDistance': None,
            'liveEventSharingTriggerTime': None,
            'dbDrivenDefaults': None,
            'schoolMode': None,
            'customMeasurementDate': None,
            'customBodyFatPercent': None,
            'customMuscleMass': None,
            'customDeviceWeight': None,
            'customDeviceBodyFatPercent': None,
            'customDeviceMuscleMass': None,
            'vivohubEnabled': None
        }

        device_settings.append(device_data)

    return device_settings

def get_active_goals_data(start_date, num_days):
    """Generate synthetic active goals data for a range of days.

    This function generates synthetic active goals data for a specified number of days, starting from the given `start_date`
    and extending for `num_days` days. Active goals can include step goals, distance goals, calorie goals, or active minute goals.
    The generated data is structured as a list of dictionaries.

    :param start_date: The starting date for generating active goals.
    :type start_date: datetime.date

    :param num_days: The number of days for which active goals should be generated.
    :type num_days: int

    :return: A list of dictionaries containing synthetic active goals data for the specified date range.
    :rtype: List[Dict]
    """
    goal_types = ["step", "distance", "calories", "activeMinutes"]
    end_date = start_date + timedelta(days=num_days)

    active_goals = []

    while start_date <= end_date:
        active_goal = {
            "goalType": random.choice(goal_types),
            "goalValue": random.randint(1000, 10000),  # You can adjust the range as needed
            "startDate": start_date,
            "endDate": start_date
        }
        active_goals.append(active_goal)
        start_date += timedelta(days=1)

    return active_goals

def get_future_goals_data(start_date, num_days):
    """Generate synthetic future goals data for a range of days.

    This function generates synthetic future goals data for a specified number of days, starting from the given `start_date`
    and extending for `num_days` days. Future goals can include step goals, distance goals, calorie goals, or active minute goals.
    The generated data is structured as a list of dictionaries.

    :param start_date: The starting date for generating future goals.
    :type start_date: datetime.date

    :param num_days: The number of days for which future goals should be generated.
    :type num_days: int

    :return: A list of dictionaries containing synthetic future goals data for the specified date range.
    :rtype: List[Dict]
    """
    goal_types = ["step", "distance", "calories", "activeMinutes"]
    end_date = start_date + timedelta(days=num_days)

    future_goals = []

    while start_date <= end_date:
        future_goal = {
            "goalType": random.choice(goal_types),
            "goalValue": random.randint(1000, 10000),  # You can adjust the range as needed
            "startDate": start_date,
            "endDate": start_date
        }
        future_goals.append(future_goal)
        start_date += timedelta(days=1)

    return future_goals

def get_past_goals_data(start_date, num_days):
    """Generate synthetic past goals data for a range of days.

    This function generates synthetic past goals data for a specified number of days, starting from the given `start_date`
    and extending for `num_days` days. Past goals can include step goals, distance goals, calorie goals, or active minute goals.
    The generated data is structured as a list of dictionaries.

    :param start_date: The starting date for generating past goals.
    :type start_date: datetime.date

    :param num_days: The number of days for which past goals should be generated.
    :type num_days: int

    :return: A list of dictionaries containing synthetic past goals data for the specified date range.
    :rtype: List[Dict]
    """
    goal_types = ["step", "distance", "calories", "activeMinutes"]
    end_date = start_date + timedelta(days=num_days)

    past_goals = []

    while start_date <= end_date:
        past_goal = {
            "goalType": random.choice(goal_types),
            "goalValue": random.randint(1000, 10000),  # You can adjust the range as needed
            "startDate": start_date,
            "endDate": start_date
        }
        past_goals.append(past_goal)
        start_date += timedelta(days=1)

    return past_goals


def get_weigh_ins_data(start_date, num_days):
    """Generate synthetic weigh-in data for a range of days.

    This function generates synthetic weigh-in data, including daily weight summaries, total average values, and previous
    and next date weight information for a specified range of days. The generated data is structured as a dictionary.

    :param start_date: The starting date for generating weigh-in data.
    :type start_date: datetime.date

    :param num_days: The number of days for which weigh-in data should be generated.
    :type num_days: int

    :return: A dictionary containing synthetic weigh-in data for the specified date range.
    :rtype: Dict
    """
    end_date = start_date + timedelta(days=num_days)

    weigh_ins = {
        "dailyWeightSummaries": [],
        "totalAverage": {
            "from": start_date,
            "until": end_date,
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
        },
        "previousDateWeight": {
            "samplePk": None,
            "date": None,
            "calendarDate": None,
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
            "sourceType": None,
            "timestampGMT": None,
            "weightDelta": None,
        },
        "nextDateWeight": {
            "samplePk": None,
            "date": None,
            "calendarDate": None,
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
            "sourceType": None,
            "timestampGMT": None,
            "weightDelta": None,
        },
    }

    # Generate random weigh-in data for the total average
    weigh_ins["totalAverage"]["weight"] = round(random.uniform(60, 90), 2)
    weigh_ins["totalAverage"]["bmi"] = round(random.uniform(18, 30), 2)
    weigh_ins["totalAverage"]["bodyFat"] = round(random.uniform(10, 25), 2)
    weigh_ins["totalAverage"]["bodyWater"] = round(random.uniform(45, 65), 2)
    weigh_ins["totalAverage"]["boneMass"] = round(random.uniform(2, 5), 2)
    weigh_ins["totalAverage"]["muscleMass"] = round(random.uniform(30, 60), 2)
    weigh_ins["totalAverage"]["physiqueRating"] = random.choice(["Good", "Average", "Excellent"])
    weigh_ins["totalAverage"]["visceralFat"] = round(random.uniform(5, 15), 2)
    weigh_ins["totalAverage"]["metabolicAge"] = random.randint(20, 60)

    # Generate random weigh-in data for the previous and next date weights
    weigh_ins["previousDateWeight"]["date"] = start_date - timedelta(days=1)
    weigh_ins["previousDateWeight"]["weight"] = round(weigh_ins["totalAverage"]["weight"] - random.uniform(0, 2), 2)
    weigh_ins["nextDateWeight"]["date"] = end_date + timedelta(days=1)
    weigh_ins["nextDateWeight"]["weight"] = round(weigh_ins["totalAverage"]["weight"] + random.uniform(0, 2), 2)

    # Generate random daily weight summaries
    current_date = start_date
    while current_date <= end_date:
        summary = {
            "date": current_date,
            "calendarDate": current_date,
            "weight": round(random.uniform(weigh_ins["totalAverage"]["weight"] - 1, weigh_ins["totalAverage"]["weight"] + 1), 2),
        }
        weigh_ins["dailyWeightSummaries"].append(summary)
        current_date += timedelta(days=1)

    return weigh_ins


def get_weigh_ins_daily_data(start_date, num_days):
    """Generate synthetic daily weigh-in data for a specified date range.

    This function generates synthetic daily weigh-in data, including daily weight summaries and total average values for a
    specified date range. The generated data is structured as a dictionary.

    :param start_date: The starting date for generating daily weigh-in data.
    :type start_date: datetime.date

    :param num_days: The number of days for which daily weigh-in data should be generated.
    :type num_days: int

    :return: A dictionary containing synthetic daily weigh-in data for the specified date range.
    :rtype: Dict
    """
    end_date = start_date + timedelta(days=num_days)

    weigh_ins_daily = {
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "dateWeightList": [],
        "totalAverage": {
            "from": int(start_date.timestamp() * 1000),
            "until": int(end_date.timestamp() * 1000),
            "weight": None,
            "bmi": None,
            "bodyFat": None,
            "bodyWater": None,
            "boneMass": None,
            "muscleMass": None,
            "physiqueRating": None,
            "visceralFat": None,
            "metabolicAge": None,
        },
    }

    # Generate random weigh-in data for the total average
    weigh_ins_daily["totalAverage"]["weight"] = round(random.uniform(60, 90), 2)
    weigh_ins_daily["totalAverage"]["bmi"] = round(random.uniform(18, 30), 2)
    weigh_ins_daily["totalAverage"]["bodyFat"] = round(random.uniform(10, 25), 2)
    weigh_ins_daily["totalAverage"]["bodyWater"] = round(random.uniform(45, 65), 2)
    weigh_ins_daily["totalAverage"]["boneMass"] = round(random.uniform(2, 5), 2)
    weigh_ins_daily["totalAverage"]["muscleMass"] = round(random.uniform(30, 60), 2)
    weigh_ins_daily["totalAverage"]["physiqueRating"] = random.choice(["Good", "Average", "Excellent"])
    weigh_ins_daily["totalAverage"]["visceralFat"] = round(random.uniform(5, 15), 2)
    weigh_ins_daily["totalAverage"]["metabolicAge"] = random.randint(20, 60)

    # Generate random daily weight summaries
    current_date = start_date
    while current_date <= end_date:
        summary = {
            "date": current_date.strftime('%Y-%m-%d'),
            "weight": round(random.uniform(weigh_ins_daily["totalAverage"]["weight"] - 1, weigh_ins_daily["totalAverage"]["weight"] + 1), 2),
        }
        weigh_ins_daily["dateWeightList"].append(summary)
        current_date += timedelta(days=1)

    return weigh_ins_daily

def get_hill_score_data(start_date, end_date):
    """Generate synthetic hill score data for a specified date range.

    This function generates synthetic hill score data, including period average scores, maximum score, and a list of hill
    score DTOs for a specified date range. The generated data is structured as a dictionary.

    :param start_date: The starting date for the hill score data.
    :type start_date: datetime.date

    :param end_date: The ending date for the hill score data.
    :type end_date: datetime.date

    :return: A dictionary containing synthetic hill score data for the specified date range.
    :rtype: Dict
    """
    hill_score = {
        "userProfilePK": random.randint(80000000, 90000000),  # Generate a random user profile PK
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "periodAvgScore": {},
        "maxScore": None,
        "hillScoreDTOList": [],
    }

    # Generate random period average scores for each day in the date range
    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d')
        hill_score["periodAvgScore"][formatted_date] = round(random.uniform(0, 100), 2)
        current_date += timedelta(days=1)

    # Generate a random max score
    hill_score["maxScore"] = round(random.uniform(100, 200), 2)

    # Generate random hill score DTO list
    for _ in range(random.randint(0, 5)):  # Random number of hill score DTOs
        score_dto = {
            "date": random.choice(list(hill_score["periodAvgScore"].keys())),
            "score": round(random.uniform(0, 100), 2),
        }
        hill_score["hillScoreDTOList"].append(score_dto)

    return hill_score

def get_endurance_score_data(start_date, end_date):
    """Generate synthetic endurance score data for a specified date range.

    This function generates synthetic endurance score data, including average and maximum values, group data for each week,
    and endurance contributor DTOs for each group. The generated data is structured as a dictionary.

    :param start_date: The starting date for the endurance score data.
    :type start_date: datetime.date

    :param end_date: The ending date for the endurance score data.
    :type end_date: datetime.date

    :return: A dictionary containing synthetic endurance score data for the specified date range.
    :rtype: Dict
    """
    endurance_score = {
        "userProfilePK": random.randint(80000000, 90000000),  # Generate a random user profile PK
        "startDate": start_date.strftime('%Y-%m-%d'),
        "endDate": end_date.strftime('%Y-%m-%d'),
        "avg": None,
        "max": None,
        "groupMap": {},
        "enduranceScoreDTO": None,
    }

    # Generate random average and max values
    endurance_score["avg"] = round(random.uniform(0, 100), 2)
    endurance_score["max"] = round(random.uniform(100, 200), 2)

    # Generate random group data for each day in the date range
    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d')
        group_data = {
            "groupAverage": round(random.uniform(0, 100), 2),
            "groupMax": round(random.uniform(100, 200), 2),
            "enduranceContributorDTOList": [],
        }

        # Generate random endurance contributor DTOs
        for _ in range(random.randint(0, 5)):  # Random number of contributor DTOs
            contributor_dto = {
                "date": formatted_date,
                "score": round(random.uniform(0, 100), 2),
            }
            group_data["enduranceContributorDTOList"].append(contributor_dto)

        endurance_score["groupMap"][formatted_date] = group_data
        current_date += timedelta(days=7)

    return endurance_score

def delete_stuff(dates, steps, hrs, brpms):
    """Delete stuff randomly, since we want to simulate missing data.

    :param dates: List of dates (each date is a separate day represented as a string)
    :type dates: List[str]
    :param steps: List of step data (each element is a list of dictionaries, each dictionary
        represents the step data for a 15-minute chunk of time in the day)
    :type steps: List[List[Dict]]
    :param hrs: List of heart rate data (each element is a dictionary)
    :type hrs: List[Dict]
    :param brpms: List of breathing rate data (each element is a dictionary)
    :type brpms: List[Dict]
    :return: List of dates, List of step data, List of heart rate data, List of breathing rate data
    :rtype: Tuple[List[str], List[Dict], List[Dict], List[Dict]]
    """

    num_days = len(dates)  # we can just use the length of the dates list

    for day_idx in tqdm(range(num_days)):
        # the duration to remove (in hours) is sampled from an exponential distribution,
        # except we truncate the undesirable long tails of the distribution
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


def create_syn_data(start_date, end_date):
    """Returns a tuple of dates, steps, heart rates, and breath rates. The data
    format is as follows. Each element in the tuple is a list of length num_days.
    For each tuple:
    - dates: List of dates (each date is a separate day represented as a string)
    - steps: List of step data (each element is a list of dictionaries, each dictionary
        represents the step data for a 15-minute chunk of time in the day)
    - heart rates: List of heart rate data (each element is a dictionary)
    - breath rates: List of breathing rate data (each element is a dictionary)

    :param start_date: the start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: A four-tuple of dates, steps, heart rates, and breath rates, each
        of which is just a list where each element represents a particular day.
    :rtype: Tuple[List[str], List[List[Dict]], List[Dict], List[Dict]]
    """

    num_days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days

    # first get the dates as datetime objects
    synth_dates = [
        datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
        for i in range(num_days)
    ]

    # process is to first get the steps, then the heart rate (since you can just compute
    # the heart rate from the steps), then the breathing rate (since you can just compute
    # the breathing rate from the heart rate)
    synth_steps = get_steps(start_date, num_days)
    synth_hrs = get_hrs(start_date, num_days, synth_steps)
    synth_brpms = get_brpms(start_date, num_days, synth_hrs)

    synth_hrv_data = get_hrv_data(start_date, num_days)
    synth_steps_data = get_steps_data(start_date, num_days)
    synth_stats_data = get_stats_data(start_date, num_days)
    synth_user_summary_data = get_user_summary_data(start_date, num_days)
    synth_body_composition_data = get_body_composition_data(start_date, num_days)
    synth_heart_rate_data = get_heart_rate_data(start_date, num_days)
    synth_training_readiness_data = get_training_readiness_data(start_date, num_days)
    synth_blood_pressure_data = get_blood_pressure_data(start_date, end_date, num_days)
    synth_floors_data = get_floors_data(start_date, end_date)
    synth_training_status_data = get_training_status_data(start_date, num_days)
    synth_resting_hr_data = get_resting_hr_data(start_date, end_date)
    synth_hydration_data = get_hydration_data(start_date, num_days)
    synth_sleep_data = get_sleep_data(start_date, num_days)
    synth_earned_badges_data = get_earned_badges_data(start_date, num_days)
    synth_stress_data = get_stress_data(start_date, num_days)
    synth_respiration_data = get_respiration_data(start_date, num_days)
    synth_spo2_data = get_spo2_data(start_date, num_days)
    synth_metrics_data = get_metrics_data(start_date, num_days)
    synth_personal_record_data = get_personal_record_data(start_date, end_date, num_days)
    synth_activities_data = get_activities_data(start_date, num_days)
    synth_device_settings_data = get_device_settings_data(num_days)
    synth_active_goals_data = get_active_goals_data(start_date, num_days)
    synth_future_goals_data = get_future_goals_data(start_date, num_days)
    synth_past_goals_data = get_past_goals_data(start_date, num_days)
    synth_weigh_ins_data = get_weigh_ins_data(start_date, num_days)
    synth_weigh_ins_daily_data = get_weigh_ins_daily_data(start_date, num_days)
    synth_hill_score_data = get_hill_score_data(start_date, end_date)
    synth_endurance_score_data = get_endurance_score_data(start_date, end_date)


    # finally, we just iterate over the steps and
    # turn the start and end timestamps to strings
    for i, synth_steps_day in enumerate(synth_steps):
        for j in range(len(synth_steps_day)):
            synth_steps[i][j]["startGMT"] = datetime.strftime(
                synth_steps[i][j]["startGMT"], "%Y-%m-%dT%H:%M:%S"
            )
            synth_steps[i][j]["endGMT"] = datetime.strftime(
                synth_steps[i][j]["endGMT"], "%Y-%m-%dT%H:%M:%S"
            )

    # randomly delete stuff (to simulate missing data)
    synth_dates, synth_steps, synth_hrs, synth_brpms = delete_stuff(
        synth_dates, synth_steps, synth_hrs, synth_brpms
    )

    return (synth_dates,
            synth_steps,
            synth_hrs,
            synth_brpms,
            synth_hrv_data,
            synth_steps_data,
            synth_stats_data,
            synth_user_summary_data,
            synth_body_composition_data,
            synth_heart_rate_data,
            synth_training_readiness_data,
            synth_blood_pressure_data,
            synth_floors_data,
            synth_training_status_data,
            synth_resting_hr_data,
            synth_hydration_data,
            synth_sleep_data,
            synth_earned_badges_data,
            synth_stress_data,
            synth_respiration_data,
            synth_spo2_data,
            synth_metrics_data,
            synth_personal_record_data,
            synth_activities_data,
            synth_device_settings_data,
            synth_active_goals_data,
            synth_future_goals_data,
            synth_past_goals_data,
            synth_weigh_ins_data,
            synth_weigh_ins_daily_data,
            synth_hill_score_data,
            synth_endurance_score_data)
