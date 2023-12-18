import numpy as np
import pandas as pd
import polyline

# Generating synthetic data for Strava


def create_syn_data(start_date, end_date):
    """
    This function generates synthetic data for Strava.

    :param start_date: The start date for the data generation in the format "YYYY-MM-DD".
    :type start_date: str
    :param end_date: The end date for the data generation in the format "YYYY-MM-DD".
    :type end_date: str
    :return: A dataframe containing the generated data.
    :rtype: pandas.DataFrame
    """

    # Generating list of dates between start and end date
    dates = pd.date_range(start_date, end_date)

    # Generating name for run
    def name_generator(x):
        return (
            np.random.choice(
                [
                    "Morning",
                    "Post Lunch",
                    "Evening",
                    "Night",
                    "Late Night",
                    "Post Dinner",
                ]
            )
            + " Run"
        )

    # Generating 10 digit random id
    def id_generator(x):
        return np.random.randint(1000000000, 9999999999, dtype=np.int64)

    # Generating random distance with average run being 3000m and standard deviation of 750m
    def distance_generator(x):
        return np.round(np.random.normal(3000, 750), 1)

    # Generating random moving time with average run being 1200s and standard deviation of 300s
    def moving_time_generator(x):
        return int(np.random.normal(1200, 300))

    # Generating random elapsed time with average run being 1700s and standard deviation of 300s
    def elapsed_time_generator(x):
        return int(np.random.normal(1700, 300))

    # Generating random total elevation gain with average run being 20m and standard deviation of 30m
    def total_elevation_gain_generator(x):
        return max(0.0, np.round(np.random.normal(20, 30), 1))

    # Generating random average speed with average run being 2.5m/s and standard deviation of 1.5m/s
    def average_speed_generator(x):
        return max(0.0, np.round(np.random.normal(2.5, 1.5, 1)))

    # Generating random max speed with average run being 3.5m/s and standard deviation of 1.5m/s
    def max_speed_generator(x):
        return max(0.0, np.round(np.random.normal(3.5, 1.5, 1)))

    # Generating random average heartrate with average run being 130bpm and standard deviation of 20bpm
    def average_heartrate_generator(x):
        return np.round(np.random.normal(130, 20), 1)

    # Generating random max heartrate with average run being 155bpm and standard deviation of 20bpm
    def max_heartrate_generator(x):
        return np.round(np.random.normal(155, 20), 1)

    # We will use Stanford's coordinate as the benchmark coordinates to generate random runs based off
    coordinate = (37.4275, -122.1697)

    # Generating random elev_high with average run being 40m and standard deviation of 25m
    def elev_high_generator(x):
        return max(0.0, np.round(np.random.normal(40, 25), 1))

    # Generating random elev_low with average run being 20m and standard deviation of 20m
    def elev_low_generator(x):
        return max(0.0, np.round(np.random.normal(20, 20), 1))

    # Generating random average cadence with average run being 75rpm and standard deviation of 10rpm
    def avg_cadence_generator(x):
        return np.round(np.random.normal(75, 10), 1)

    # Generating random average watts with average run being 190w and standard deviation of 50w
    def avg_watt_generator(x):
        return np.round(np.random.normal(190, 50), 1)

    # Generating random kilojoules with average run being 0.0864kj/m
    def kilo_joule_gen(distance):
        return np.round(distance * 0.0864, 1)

    # Generating random map summary polyline
    def map_summary_polyline_generator(x):
        return polyline.encode(x)

    # Creating a dataframe to store all the generated data
    synthetic_df = pd.DataFrame(
        columns=[
            "name",
            "id",
            "start_date",
            "distance",
            "moving_time",
            "elapsed_time",
            "total_elevation_gain",
            "average_speed",
            "max_speed",
            "average_heartrate",
            "max_heartrate",
            "map.summary_polyline",
            "elev_high",
            "elev_low",
            "average_cadence",
            "average_watts",
            "kilojoules",
        ]
    )

    for d in dates:

        # Generating 12 different coordinates for each run
        coordinates = [
            (
                coordinate[0] + np.random.normal(-0.005, 0.005),
                coordinate[1] + np.random.normal(-0.005, 0.005),
            )
            for x in range(12)
        ]

        # Generating random run distance
        distance = distance_generator(d)

        # Generating entry of all synthetic data to be added to the dataframe
        entry = pd.DataFrame.from_dict(
            {
                "name": name_generator(d),
                "id": id_generator(d),
                "start_date": d.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "distance": distance,
                "moving_time": moving_time_generator(d),
                "elapsed_time": elapsed_time_generator(d),
                "total_elevation_gain": total_elevation_gain_generator(d),
                "average_speed": average_speed_generator(d),
                "max_speed": max_speed_generator(d),
                "average_heartrate": average_heartrate_generator(d),
                "max_heartrate": max_heartrate_generator(d),
                "map.summary_polyline": map_summary_polyline_generator(coordinates),
                "elev_high": elev_high_generator(d),
                "elev_low": elev_low_generator(d),
                "average_cadence": avg_cadence_generator(d),
                "average_watts": avg_watt_generator(d),
                "kilojoules": kilo_joule_gen(distance),
            }
        )
        synthetic_df = pd.concat([synthetic_df, entry], ignore_index=True)

    # Returning the synthetic dataframe
    return synthetic_df
