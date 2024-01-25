from typing import Optional

import re

import pandas as pd
import requests

##############################
# Workout ID data
##############################
workout_id = {
    -1: "Activity",
    0: "Running",
    1: "Cycling",
    16: "Baseball",
    17: "Basketball",
    18: "Rowing",
    19: "Fencing",
    20: "Field Hockey",
    21: "Football",
    22: "Golf",
    42: "Ice Hockey",
    25: "Lacrosse",
    27: "Rugby",
    28: "Sailing",
    29: "Skiing",
    30: "Soccer",
    31: "Softball",
    32: "Squash",
    33: "Swimming",
    34: "Tennis",
    35: "Track & Field",
    36: "Volleyball",
    37: "Water Polo",
    38: "Wrestling",
    39: "Boxing",
    42: "Dance",
    43: "Pilates",
    44: "Yoga",
    45: "Weightlifting",
    47: "Cross Country Skiing",
    48: "Functional Fitness",
    49: "Duathlon",
    51: "Gymnastics",
    52: "Hiking/Rucking",
    53: "Horseback Riding",
    55: "Kayaking",
    56: "Martial Arts",
    57: "Mountain Biking",
    59: "Powerlifting",
    60: "Rock Climbing",
    61: "Paddleboarding",
    62: "Triathlon",
    63: "Walking",
    64: "Surfing",
    65: "Elliptical",
    66: "Stairmaster",
    70: "Meditation",
    71: "Other",
    73: "Diving",
    74: "Operations - Tactical",
    75: "Operations - Medical",
    76: "Operations - Flying",
    77: "Operations - Water",
    82: "Ultimate",
    83: "Climber",
    84: "Jumping Rope",
    85: "Australian Football",
    86: "Skateboarding",
    87: "Coaching",
    88: "Ice Bath",
    89: "Commuting",
    90: "Gaming",
    91: "Snowboarding",
    92: "Motocross",
    93: "Caddying",
    94: "Obstacle Course Racing",
    95: "Motor Racing",
    96: "HIIT",
    97: "Spin",
    98: "Jiu Jitsu",
    99: "Manual Labor",
    100: "Cricket",
    101: "Pickleball",
    102: "Inline Skating",
    103: "Box Fitness",
    104: "Spikeball",
    105: "Wheelchair Pushing",
    106: "Paddle Tennis",
    107: "Barre",
    108: "Stage Performance",
    109: "High Stress Work",
    110: "Parkour",
    111: "Gaelic Football",
    112: "Hurling/Camogie",
    113: "Circus Arts",
    121: "Massage Therapy",
    125: "Watching Sports",
    126: "Assault Bike",
    127: "Kickboxing",
    128: "Stretching",
    230: "Table Tennis",
    231: "Badminton",
    232: "Netball",
    233: "Sauna",
    234: "Disc Golf",
    235: "Yard Work",
    236: "Air Compression",
    237: "Percussive Massage",
    238: "Paintball",
    239: "Ice Skating",
    240: "Handball",
}
workout_keys = list(workout_id.keys())

# def format_datetime(time_str: Optional[str]) -> Optional[str]:
#     """ Formats the datetime into "%Y-%m-%d %H:%M:%S Z"

#     Args:
#         time_str (str): datetime in the format "%Y-%m-%dT%H:%M:%S.%fZ".

#     Returns:
#         str or None: datetime in the desired format ("%Y-%m-%d %H:%M:%S Z").
#     """
#     if time_str is not None:
#         dt_object = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
#         formatted_str = dt_object.strftime("%Y-%m-%d %H:%M:%S Z")
#     else:
#         formatted_str = None

#     return formatted_str


# Fetch profile
def fetch_profile(access_token: str) -> pd.DataFrame:
    """
    Fetches the basic user profile data from the WHOOP API.

    :param str access_token: The access token for authentication.

    :raises Exception: Raised if the API request fails with a status code other than 200.

    :return: A pandas DataFrame containing the user profile data.
    :rtype: pd.DataFrame
    """
    response = requests.get(
        "https://api.prod.whoop.com/developer/v1/user/profile/basic",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    out = response.json()
    for key in out:
        if not isinstance(out[key], list):
            out[key] = [out[key]]
    df = pd.DataFrame.from_dict(out)
    return df


# Fetch body measurements
def fetch_body_measurements(access_token: str) -> pd.DataFrame:
    """
    Fetches body measurements data from the WHOOP API.

    :param str access_token: The access token for authentication.

    :raises Exception: Raised if the API request fails with a status code other than 200.

    :return: A pandas DataFrame containing body measurements data.
    :rtype: pd.DataFrame
    """
    response = requests.get(
        "https://api.prod.whoop.com/developer/v1/user/measurement/body",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    out = response.json()
    for key in out:
        if not isinstance(out[key], list):
            out[key] = [out[key]]
    df = pd.DataFrame.from_dict(out)

    return df


# Fetch collection
def fetch_collection(
    collection_type: str,
    access_token: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetches collection data from the WHOOP API.

    :param str collection_type: The type of collection to be fetched.
    :param str access_token: The access token for authentication.
    :param str start_date: The start date of the requested data in the format "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS.mmmZ". Defaults to None (not provided).
    :param str end_date: The end date of the requested data in the format "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS.mmmZ". Defaults to None (not provided).

    :raises ValueError: Raised if the provided start_date or end_date is not in the correct format.

    :return: A continuous pandas DataFrame containing all the fetched records.
    :rtype: pd.DataFrame
    """
    long_pattern = re.compile(r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}\.\d{3}Z)?")
    short_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

    if start_date is not None:  # Check if start_date is given
        # Format dates as required
        if short_pattern.match(start_date):
            start_date = start_date + "T00:00:00.000Z"
        elif long_pattern.match(start_date):
            pass
        else:
            raise ValueError(
                "Start date is not in the correct format. Please use the format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS.mmmZ"
            )

    if end_date is not None:  # Check if end_date is given
        # Format dates as required
        if short_pattern.match(end_date):
            end_date = end_date + "T00:00:00.000Z"
        elif long_pattern.match(end_date):
            pass
        else:
            raise ValueError(
                "End date is not in the correct format. Please use the format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS.mmmZ"
            )

    next_page = True
    next_token = None

    # print(collection_type + " Collection")
    dfs = []
    while next_page:
        # Make the request
        if collection_type == "Cycle":
            query = "https://api.prod.whoop.com/developer/v1/cycle?limit=20&"
        elif collection_type == "Workout":
            query = "https://api.prod.whoop.com/developer/v1/activity/workout?limit=20&"
        elif collection_type == "Sleep":
            query = "https://api.prod.whoop.com/developer/v1/activity/sleep?limit=20&"
        elif collection_type == "Recovery":
            query = "https://api.prod.whoop.com/developer/v1/recovery?limit=20&"
        else:
            raise ValueError(
                'type of collection must either be "Cycle", "Workout", or "Sleep".'
            )
        if start_date is not None:
            query += f"start={start_date}&"
        if end_date is not None:
            query += f"end={end_date}&"
        if next_token is not None:
            query += f"nextToken={next_token}&"
        query = query[:-1]

        response = requests.get(
            query,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )

        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        # Process the output
        out = response.json()
        out_next_token, out_records_list = out["next_token"], out["records"]

        # if collection_type == "Cycle":
        #     for record in out_records_list:
        #         if record['score'] is not None:
        #             record['strain'] = record['score']['strain']
        #             record['kilojoule'] = record['score']['kilojoule']
        #             record['average_heart_rate'] = record['score']['average_heart_rate']
        #             record['max_heart_rate'] = record['score']['max_heart_rate']

        #     record_dict = {key: [d[key] for d in out_records_list] for key in out_records_list[0]}
        #     new_start = []
        #     new_end = []
        #     for i in range(len(record_dict['score_state'])):
        #         record_dict['score_state'][i] = "Yes" if (record_dict['score_state'][i] == "SCORED") else "No"
        #         new_start.append(format_datetime(record_dict['start'][i]))
        #         new_end.append(format_datetime(record_dict['end'][i]))

        #     record_dict['start'] = new_start
        #     record_dict['end'] = new_end

        # elif collection_type == "Workout":
        #     for record in out_records_list:
        #         if record['score'] is not None:
        #             record['strain'] = record['score']['strain']
        #             record['kilojoule'] = record['score']['kilojoule']
        #             record['average_heart_rate'] = record['score']['average_heart_rate']
        #             record['max_heart_rate'] = record['score']['max_heart_rate']
        #             record['percent_recorded'] = record['score']['percent_recorded']
        #             record['distance_meter'] = record['score']['distance_meter']
        #             record['altitude_gain_meter'] = record['score']['altitude_gain_meter']
        #             record['altitude_change_meter'] = record['score']['altitude_change_meter']

        #     record_dict = {key: [d[key] for d in out_records_list] for key in out_records_list[0]}

        #     new_start = []
        #     new_end = []
        #     for i in range(len(record_dict["sport_id"])):
        #         record_dict["sport_id"][i] = workout_id[record_dict["sport_id"][i]]
        #         record_dict['score_state'][i] = "Yes" if (record_dict['score_state'][i] == "SCORED") else "No"
        #         new_start.append(format_datetime(record_dict['start'][i]))
        #         new_end.append(format_datetime(record_dict['end'][i]))

        #     record_dict['start'] = new_start
        #     record_dict['end'] = new_end

        # elif collection_type == "Sleep":
        # for record in out_records_list:
        #     if record['score'] is not None:
        #         record['respiratory_rate'] = record['score']['respiratory_rate']
        #         record['sleep_performance_percentage'] = record['score']['sleep_performance_percentage']
        #         record['sleep_consistency_percentage'] = record['score']['sleep_consistency_percentage']
        #         record['sleep_efficiency_percentage'] = record['score']['sleep_efficiency_percentage']
        #         del record['score']['stage_summary'], record['score']['sleep_needed']

        # record_dict = {key: [d[key] for d in out_records_list] for key in out_records_list[0]}
        # new_start = []
        # new_end = []
        # for i in range(len(record_dict['score_state'])):
        #     record_dict['score_state'][i] = "Yes" if (record_dict['score_state'][i] == "SCORED") else "No"
        #     new_start.append(format_datetime(record_dict['start'][i]))
        #     new_end.append(format_datetime(record_dict['end'][i]))

        # record_dict['start'] = new_start
        # record_dict['end'] = new_end

        # record_dict['score_available'] = record_dict['score_state']
        # record_dict['cycle_id'] = record_dict['id']
        # del record_dict['created_at'], record_dict['updated_at'], record_dict['score'], record_dict['score_state'], record_dict['id'], record_dict['user_id']

        record_dict = {
            key: [d[key] for d in out_records_list] for key in out_records_list[0]
        }

        df = pd.DataFrame.from_dict(record_dict)
        dfs.append(df)

        if out_next_token is None:
            next_page = False
            break

        next_token = out_next_token
    #     print("Next page:")

    # print("----------------------------")
    result_df = pd.concat(dfs, ignore_index=True)

    return result_df


# Fetch cycle collection
def fetch_cycle_collection(
    access_token: str, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> pd.DataFrame:
    """Fetches cycle collection data from the WHOOP API."""
    return fetch_collection(
        collection_type="Cycle",
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
    )


# Fetch workout collection
def fetch_workout_collection(
    access_token: str, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> pd.DataFrame:
    """Fetches workout collection data from the WHOOP API."""
    return fetch_collection(
        collection_type="Workout",
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
    )


# Fetch sleep collection
def fetch_sleep_collection(
    access_token: str, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> pd.DataFrame:
    """Fetches sleep collection data from the WHOOP API."""
    return fetch_collection(
        collection_type="Sleep",
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
    )


# Fetch recovery collection
def fetch_recovery_collection(
    access_token: str, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> pd.DataFrame:
    """Fetches recovery collection data from the WHOOP API."""
    return fetch_collection(
        collection_type="Recovery",
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
    )
