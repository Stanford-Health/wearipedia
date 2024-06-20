import random
import re
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

__all__ = [
    "create_synthetic_cycle_collection_df",
    "create_synthetic_workout_collection_df",
    "create_synthetic_sleep_collection_df",
]

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


def check_date_format(start_date: str, end_date: str) -> tuple:
    """
    Checks and formats the input dates to ensure they are in the correct format.

    :param start_date: The start date of the range in 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS.mmmZ' format.
    :type start_date: str

    :param end_date: The end date of the range in 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS.mmmZ' format.
    :type end_date: str

    :return: A tuple containing the formatted start and end datetime objects.
    :rtype: Tuple[datetime, datetime]

    :raises ValueError: If the provided dates are not in the correct format or if the end date is before the start date.
    """
    long_pattern = re.compile(r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}\.\d{3}Z)?")
    short_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

    # Format dates as required
    if short_pattern.match(start_date):
        start_date = start_date + "T07:00:00.000Z"
    elif long_pattern.match(start_date):
        pass
    else:
        raise ValueError(
            "Start date is not in the correct format. Please use the format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS.mmmZ"
        )

    # Format dates as required
    if short_pattern.match(end_date):
        end_date = end_date + "T00:00:00.000Z"
    elif long_pattern.match(end_date):
        pass
    else:
        raise ValueError(
            "End date is not in the correct format. Please use the format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS.mmmZ"
        )

    # Convert to datetime objects
    start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Compare and raise an error if end date is before start date
    if end_datetime < start_datetime:
        raise ValueError("End date should not be before the start date.")

    return start_datetime, end_datetime


def make_created_at_updated_at_lists(end_list: list) -> tuple:
    """
    Generate lists of "created_at" and "updated_at" dates based on a given list of "end" dates.

    :param end_list: List of "end" dates in the format "%Y-%m-%dT%H:%M:%S.%fZ".
    :type end_list: list

    :return: A tuple containing two lists, where the first list is "created_at" dates and the second list is "updated_at" dates.
    :rtype: tuple
    """
    created_at_list = []  # List of "created_at" dates
    updated_at_list = []  # List of "updated_at" dates
    for i in range(len(end_list)):
        end = datetime.strptime(end_list[i], "%Y-%m-%dT%H:%M:%S.%fZ")
        created_at_datetime = end + timedelta(
            hours=np.random.randint(1, 3),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
        )
        updated_at_datetime = created_at_datetime + timedelta(
            hours=np.random.randint(1, 3),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
            milliseconds=np.random.randint(0, 1000),
        )

        created_at_str = created_at_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        updated_at_str = updated_at_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        created_at_list.append(created_at_str)
        updated_at_list.append(updated_at_str)

    return created_at_list, updated_at_list


def create_synthetic_cycle_collection_df(
    start_date="2017-08-09", end_date="2023-12-20"
) -> pd.DataFrame:
    """
    Generates a synthetic DataFrame representing a cycle collection.

    :param start_date: Start date in the format 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS.mmmZ'.
    :type start_date: str

    :param end_date: End date in the format 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS.mmmZ'.
    :type end_date: str

    :return: A synthetic DataFrame representing a cycle collection with the following columns:
      - 'user_id': User ID for the cycle collection.
      - 'id': Unique identifier for each cycle entry.
      - 'created_at': Date and time when the cycle entry was created.
      - 'updated_at': Date and time when the cycle entry was last updated.
      - 'start': Start date and time of the cycle.
      - 'end': End date and time of the cycle.
      - 'timezone_offset': Timezone offset for the cycle collection.
      - 'score_state': State of the cycle's score (constant value 'SCORED').
      - 'score': Dictionary containing synthetic scores for the cycle, including 'strain', 'kilojoule',
        'average_heart_rate', and 'max_heart_rate'.
    :rtype: pd.DataFrame
    """

    start_datetime, end_datetime = check_date_format(start_date, end_date)

    # Create the "start" and "end" dates
    start_list = []  # List of "start" dates
    end_list = []  # List of "end" dates
    curr_datetime = start_datetime
    while True:
        start_str = curr_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        new_datetime = curr_datetime + timedelta(
            hours=np.random.randint(18, 26),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
            milliseconds=np.random.randint(0, 1000),
        )
        new_str = new_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if new_datetime < end_datetime:
            start_list.append(start_str)
            end_list.append(new_str)
        else:
            break

        if new_datetime.date() == curr_datetime.date():
            curr_datetime = curr_datetime + relativedelta(
                days=1, hour=8, minute=0, second=0
            )
        else:
            curr_datetime = new_datetime

    # Create the "created_at" and "updated_at" dates
    created_at_list, updated_at_list = make_created_at_updated_at_lists(end_list)

    # Reverse the order of all dates
    start_list = start_list[::-1]
    end_list = end_list[::-1]
    created_at_list = created_at_list[::-1]
    updated_at_list = updated_at_list[::-1]

    num_days = len(created_at_list)

    # Assemble the dataframe
    syn_collection = pd.DataFrame()
    syn_collection["user_id"] = [np.random.randint(0, 20000)] * num_days
    syn_collection["id"] = np.random.randint(0, 100000000, size=(num_days,))
    syn_collection["created_at"] = created_at_list
    syn_collection["updated_at"] = updated_at_list
    syn_collection["start"] = start_list
    syn_collection["end"] = end_list
    syn_collection["timezone_offset"] = "-08:00"
    syn_collection["score_state"] = "SCORED"
    syn_collection["score"] = [{} for _ in range(num_days)]

    prob_distribution = [0.7, 0.1, 0.15, 0.05]
    ranges = [(10, 13.9), (0, 9.9), (14, 17.9), (18, 21)]

    for i in range(num_days):
        strain = get_strain(prob_distribution, ranges)
        if 0 <= strain <= 9.9:
            average_heart_rate = int(np.random.uniform(64, 69))
        elif 10 <= strain <= 13.9:
            average_heart_rate = int(np.random.uniform(69, 75))
        elif 14 <= strain <= 17.9:
            average_heart_rate = int(np.random.uniform(75, 78))
        else:
            average_heart_rate = int(np.random.uniform(78, 79))
        scores = {
            "strain": strain,
            "kilojoule": np.round(np.random.uniform(6000, 9000), 3),
            "average_heart_rate": average_heart_rate,
            "max_heart_rate": int(np.random.uniform(150, 180)),
        }
        syn_collection.at[i, "score"] = scores.copy()

    return syn_collection


def create_synthetic_workout_collection_df(
    start_date="2017-08-09", end_date="2023-12-20"
) -> pd.DataFrame:
    """
    Generates a synthetic DataFrame with workout collection data.

    :param start_date: Start date in the format YYYY-MM-DD (default: "2017-08-09").
    :type start_date: str

    :param end_date: End date in the format YYYY-MM-DD (default: "2023-12-20").
    :type end_date: str

    :return: Synthetic workout collection DataFrame with columns:
        - "user_id": Random user ID.
        - "id": Random workout ID.
        - "created_at": List of created_at dates.
        - "updated_at": List of updated_at dates.
        - "start": List of start dates.
        - "end": List of end dates.
        - "timezone_offset": Timezone offset.
        - "sport_id": List of randomly chosen workout IDs.
        - "score_state": Constant value "SCORED".
        - "score": List of dictionaries with synthetic workout scores.
    :rtype: pd.DataFrame
    """

    start_datetime, end_datetime = check_date_format(start_date, end_date)

    # Create the "start" and "end" dates
    start_list = []  # List of "start" dates
    end_list = []  # List of "end" dates
    curr_datetime = start_datetime
    while True:
        start_str = curr_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # Create random datetime for the activity
        random_start = curr_datetime + timedelta(days=np.random.randint(1, 6))
        random_start = random_start.replace(
            hour=np.random.randint(8, 16),
            minute=np.random.randint(0, 60),
            second=np.random.randint(0, 60),
            microsecond=np.random.randint(0, 1000) * 1000,
        )
        random_end = random_start + timedelta(
            hours=np.random.randint(1, 8),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
            milliseconds=np.random.randint(0, 1000),
        )

        random_start_str = random_start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        random_end_str = random_end.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if random_end < end_datetime:
            start_list.append(random_start_str)
            end_list.append(random_end_str)
        else:
            break

        curr_datetime = random_end

    created_at_list, updated_at_list = make_created_at_updated_at_lists(end_list)

    # Reverse the order of all dates
    start_list = start_list[::-1]
    end_list = end_list[::-1]
    created_at_list = created_at_list[::-1]
    updated_at_list = updated_at_list[::-1]

    num_days = len(created_at_list)

    # Assemble the dataframe
    syn_collection = pd.DataFrame()
    syn_collection["user_id"] = [np.random.randint(0, 20000)] * num_days
    syn_collection["id"] = np.random.randint(0, 100000, size=(num_days,))
    syn_collection["created_at"] = created_at_list
    syn_collection["updated_at"] = updated_at_list
    syn_collection["start"] = start_list
    syn_collection["end"] = end_list
    syn_collection["timezone_offset"] = "-08:00"
    syn_collection["sport_id"] = random.choices(workout_keys, k=num_days)
    syn_collection["score_state"] = "SCORED"
    syn_collection["score"] = [{} for _ in range(num_days)]

    for i in range(num_days):
        scores = {
            "strain": np.round(np.random.uniform(3, 13), 4),
            "average_heart_rate": int(np.random.uniform(50, 100)),
            "max_heart_rate": int(np.random.uniform(150, 180)),
            "kilojoule": np.round(np.random.uniform(6000, 9000), 4),
            "percent_recorded": int(np.random.uniform(90, 100)),
            "distance_meter": np.round(np.random.uniform(1000, 2000), 4),
            "altitude_gain_meter": np.round(np.random.uniform(0, 100), 4),
            "altitude_change_meter": np.round(np.random.uniform(-1, 1), 4),
            "zone_duration": {
                "zone_zero_milli": int(np.random.uniform(10000, 20000)),
                "zone_one_milli": int(np.random.uniform(300000, 400000)),
                "zone_two_milli": int(np.random.uniform(300000, 400000)),
                "zone_three_milli": int(np.random.uniform(50000, 80000)),
                "zone_four_milli": int(np.random.uniform(10000, 20000)),
                "zone_five_milli": int(np.random.uniform(10000, 20000)),
            },
        }
        syn_collection.at[i, "score"] = scores.copy()

    return syn_collection


def create_synthetic_sleep_collection_df(
    start_date="2017-08-09", end_date="2023-12-20"
) -> pd.DataFrame:
    """
    Generate a synthetic sleep collection DataFrame with random data.

    :param start_date: Start date of the collection period in the format "YYYY-MM-DD". Default is "2017-08-09".
    :type start_date: str

    :param end_date: End date of the collection period in the format "YYYY-MM-DD". Default is "2023-12-20".
    :type end_date: str

    :return: Synthetic sleep collection DataFrame with columns including user_id, id, created_at, updated_at, start,
      end, timezone_offset, nap, score_state, and score.

    The "score" column contains random sleep-related scores, including stage_summary, sleep_needed, respiratory_rate,
    sleep_performance_percentage, sleep_consistency_percentage, and sleep_efficiency_percentage.
    :rtype: pd.DataFrame
    """

    start_datetime, end_datetime = check_date_format(start_date, end_date)

    # Create the "start" and "end" dates
    start_list = []  # List of "start" dates
    end_list = []  # List of "end" dates
    curr_datetime = start_datetime
    while True:
        # Create random datetime for the activity
        random_start = curr_datetime
        random_start = random_start.replace(
            hour=np.random.randint(21, 23),
            minute=np.random.randint(0, 60),
            second=np.random.randint(0, 60),
            microsecond=np.random.randint(0, 1000) * 1000,
        )
        random_end = random_start + timedelta(
            hours=np.random.randint(5, 10),
            minutes=np.random.randint(0, 60),
            seconds=np.random.randint(0, 60),
            milliseconds=np.random.randint(0, 1000),
        )

        random_start_str = random_start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        random_end_str = random_end.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if random_end < end_datetime:
            start_list.append(random_start_str)
            end_list.append(random_end_str)
        else:
            break

        curr_datetime = random_end

    created_at_list, updated_at_list = make_created_at_updated_at_lists(end_list)

    # Reverse the order of all dates
    start_list = start_list[::-1]
    end_list = end_list[::-1]
    created_at_list = created_at_list[::-1]
    updated_at_list = updated_at_list[::-1]

    num_days = len(created_at_list)

    # Assemble the dataframe
    syn_collection = pd.DataFrame()
    syn_collection["user_id"] = [np.random.randint(0, 20000)] * num_days
    syn_collection["id"] = np.random.randint(0, 100000, size=(num_days,))
    syn_collection["created_at"] = created_at_list
    syn_collection["updated_at"] = updated_at_list
    syn_collection["start"] = start_list
    syn_collection["end"] = end_list
    syn_collection["timezone_offset"] = "-08:00"
    syn_collection["nap"] = [False] * num_days
    syn_collection["score_state"] = "SCORED"
    syn_collection["score"] = [{} for _ in range(num_days)]

    for i in range(num_days):
        # Initialize scores for the day
        total_sleep_time = int(np.random.normal(2.88e7, 3.6e6))
        light_sleep_proportion = np.random.normal(0.55, 0.05)
        slow_wave_sleep_proportion = np.random.normal(0.22, 0.05)
        rem_sleep_proportion = np.random.normal(0.23, 0.05)
        awake_proportion = np.random.normal(0.07, 0.01)

        # Normalize proportions to ensure they sum to 1
        total_proportion = (
            light_sleep_proportion
            + slow_wave_sleep_proportion
            + rem_sleep_proportion
            + awake_proportion
        )
        light_sleep_proportion /= total_proportion
        slow_wave_sleep_proportion /= total_proportion
        rem_sleep_proportion /= total_proportion
        awake_proportion /= total_proportion

        scores = {
            "stage_summary": {
                "total_in_bed_time_milli": total_sleep_time,
                "total_awake_time_milli": int(total_sleep_time * awake_proportion),
                "total_no_data_time_milli": 0,
                "total_light_sleep_time_milli": int(
                    total_sleep_time * light_sleep_proportion
                ),
                "total_slow_wave_sleep_time_milli": int(
                    total_sleep_time * slow_wave_sleep_proportion
                ),
                "total_rem_sleep_time_milli": int(
                    total_sleep_time * rem_sleep_proportion
                ),
                "sleep_cycle_count": int(np.random.normal(3, 0.5)),
                "disturbance_count": int(np.random.normal(5, 2)),
            },
            "sleep_needed": {
                "baseline_milli": int(np.random.normal(25000000, 500000)),
                "need_from_sleep_debt_milli": int(np.random.uniform(0, 500000)),
                "need_from_recent_strain_milli": int(np.random.uniform(0, 500000)),
                "need_from_recent_nap_milli": int(np.random.uniform(-50000, 0)),
            },
            "respiratory_rate": np.round(np.random.normal(15, 2), 2),
            "sleep_performance_percentage": int(spp(total_sleep_time)),
            "sleep_consistency_percentage": int(np.random.normal(90, 5)),
            "sleep_efficiency_percentage": np.round(np.random.normal(90, 5), 2),
        }

        # Set the scores for the day
        syn_collection.at[i, "score"] = scores

    return syn_collection


def spp(x):
    """
    Generates a sleep performance percentage based on a linear relation with total sleep time.
    :param x: total sleep time in miliseconds
    :type x: int
    """
    a = (90 - 78) / (2.88e7 - 1.80e7)
    b = 78 - a * 1.80e7
    y = a * x + b + int(np.random.uniform(-3.5, 3.5))
    return min(100, y)


def get_strain(prob_distribution, ranges):
    """
    Generates a strain value based on the provided probability distribution and ranges.

    :param prob_distribution: Probability distribution of the strain values.
    :type prob_distribution: list[float]
    :param ranges: Ranges for each probability distribution.
    :type ranges: list[tuple(float, float)]

    :return: Random strain value.
    :rtype: float
    """
    # Define the probability distribution
    prob_distribution = [0.7, 0.1, 0.15, 0.05]
    # Define the ranges for each probability distribution
    ranges = [(10, 13.9), (0, 9.9), (14, 17.9), (18, 21)]
    random_value = np.random.choice(len(prob_distribution), p=prob_distribution)
    return np.round(
        np.random.uniform(ranges[random_value][0], ranges[random_value][1]), 7
    )
