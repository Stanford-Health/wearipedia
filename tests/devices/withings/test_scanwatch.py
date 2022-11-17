# perform additional test specific to withings scanwatch device

import hashlib
from datetime import datetime

import wearipedia


def test_withings_scanwatch_synthetic():
    start_dates = [datetime(2009, 11, 15), datetime(2021, 4, 1), datetime(2022, 6, 10)]
    end_dates = [datetime(2010, 2, 1), datetime(2021, 6, 20), datetime(2022, 8, 25)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "withings/scanwatch",
            params={
                "synthetic_start_date": datetime.strftime(start_date, "%Y-%m-%d"),
                "synthetic_end_date": datetime.strftime(end_date, "%Y-%m-%d"),
            },
        )

        # calling tests for each pair of start and end dates
        helper_test(device, start_date, end_date)


def helper_test(device, start_synthetic, end_synthetic):

    sleeps = device.get_data("sleeps")
    heart_rates = device.get_data("heart_rates")

    # checking the columns of sleeps dataframe
    assert (
        sleeps.columns
        == [
            "id",
            "timezone",
            "model",
            "model_id",
            "hash_deviceid",
            "date",
            "startdate",
            "enddate",
            "data",
            "created",
            "modified",
        ]
    ).all(), f"Sleeps data is not correct: {sleeps}"

    # checking columns in sleeps dataframe

    # checking that id is in range of 0 to 100000000
    for id in sleeps["id"]:
        assert 0 <= id <= 100000000, f"ID is not in range: {id}"

    # checking that timezone is "America/Los_Angeles"
    for timezone in sleeps["timezone"]:
        assert timezone == "America/Los_Angeles", f"Timezone is not correct: {timezone}"

    # checking that model is 16
    for model in sleeps["model"]:
        assert model == 16, f"Model is not correct: {model}"

    # checking that model_id is 93
    for model_id in sleeps["model_id"]:
        assert model_id == 93, f"Model ID is not correct: {model_id}"

    # checking that hash_deviceid is d41d8cd98f00b204e9800998ecf8427e
    for hash_deviceid in sleeps["hash_deviceid"]:
        assert (
            hash_deviceid == "d41d8cd98f00b204e9800998ecf8427e"
        ), f"Hash Device ID is not correct: {hash_deviceid}"

    # checking the dates are consecutive
    # for date_1, date_2 in zip(sleeps["date"][:-1], sleeps["date"][1:]):
    #     assert (
    #         date_2 - date_1
    #     ).days == 1, f"Sleeps dates are not consecutive: {date_1}, {date_2}"

    # checking the Series sleeps["data"] which contains 18 attributes

    # checking wakeup duration
    for data_row in sleeps["data"]:

        # checking the wakeupduration is in range of 0 to 3000
        assert (
            0 <= data_row["wakeupduration"] <= 3000
        ), f"Wakeup duration is not in range: {data_row['wakeupduration']}"

        # checking the wakeupcount is non negative
        assert (
            data_row["wakeupcount"] >= 0
        ), f"Wakeup count is not correct: {data_row['wakeupcount']}"

        # checking the durationtosleep is in range of 120 to 180
        assert (
            120 <= data_row["durationtosleep"] <= 180
        ), f"Duration to sleep is not in correct range: {data_row['durationtosleep']}"

        # checking the durationtowakeup is in range of 0 to 700
        assert (
            0 <= data_row["durationtowakeup"] <= 700
        ), f"Duration to wakeup is not in correct range: {data_row['durationtowakeup']}"

        # checking the total_timeinbed is in range of 10000 to 50000
        assert (
            10000 <= data_row["total_timeinbed"] <= 50000
        ), f"Total time in bed is not in correct range: {data_row['total_timeinbed']}"

        # checking the total_sleep_time is in range of 10000 to 50000
        assert (
            10000 <= data_row["total_sleep_time"] <= 50000
        ), f"Total sleep is not in correct range: {data_row['total_sleep_time']}"

        # checking sleep_efficiency is in range of 0 to 1
        assert (
            0 <= data_row["sleep_efficiency"] <= 1
        ), f"Sleep efficiency is not in correct range: {data_row['sleep_efficiency']}"

        # checking sleep_latency is in range of 120 to 300
        assert (
            120 <= data_row["sleep_latency"] <= 300
        ), f"Sleep latency is not in correct range: {data_row['sleep_latency']}"

        # checking wakeup_latency is in range of 0 to 800
        assert (
            0 <= data_row["wakeup_latency"] <= 800
        ), f"Wakeup latency is not in correct range: {data_row['wakeup_latency']}"

        # checking waso is in range of 0 to 4000
        assert (
            0 <= data_row["waso"] <= 4000
        ), f"WASO is not in correct range: {data_row['waso']}"

        # checking nb_rem_episodes is non negative
        assert (
            data_row["nb_rem_episodes"] >= 0
        ), f"Number of REM episodes is not correct: {data_row['nb_rem_episodes']}"

        # checking out_of_bed_count is non negative
        assert (
            data_row["out_of_bed_count"] >= 0
        ), f"Out of bed episodes is not correct: {data_row['out_of_bed_count']}"

        # checking lightsleepduration is in range of 6000 to 35000
        assert (
            6000 <= data_row["lightsleepduration"] <= 35000
        ), f"Light sleep duration is not in correct range: {data_row['lightsleepduration']}"

        # checking deepsleepduration is in range of 3000 to 17000
        assert (
            3000 <= data_row["deepsleepduration"] <= 17000
        ), f"Deep sleep duration is not in correct range: {data_row['deepsleepduration']}"

        # checking hr_average is in range of 55 to 65
        assert (
            55 <= data_row["hr_average"] <= 65
        ), f"HR average is not in correct range: {data_row['hr_average']}"

        # checking hr_min is in range of 40 to 60
        assert (
            40 <= data_row["hr_min"] <= 60
        ), f"HR min is not in correct range: {data_row['hr_min']}"

        # checking hr_max is in range of 70 to 120
        assert (
            70 <= data_row["hr_max"] <= 120
        ), f"HR max is not in correct range: {data_row['hr_max']}"

        # checking sleep_score is in range 30 to 80
        assert (
            30 <= data_row["sleep_score"] <= 80
        ), f"Sleep score is not in correct range: {data_row['sleep_score']}"

    # checking the columns of heart_rates dataframe
    assert (
        heart_rates.columns
        == ["datetime", "heart_rate", "model", "model_id", "deviceid"]
    ).all(), f"Heart rates data is not correct: {heart_rates}"

    # checking columns in heart_rates dataframe

    # checking heart_rate is in range of 0 to 250
    for heart_rate in heart_rates["heart_rate"]:
        assert (
            0 <= heart_rate <= 250
        ), f"Heart rate is not in correct range: {heart_rate}"

    # checking model is "ScanWatch"
    for model in heart_rates["model"]:
        assert model == "ScanWatch", f"Model is not correct: {model}"

    # checking model_id is correct
    for model_id in heart_rates["model_id"]:
        assert model_id == 93, f"Model ID is not correct: {model_id}"

    # checking deviceid is correct hashcode
    for deviceid in heart_rates["deviceid"]:
        assert (
            deviceid == hashlib.md5(usedforsecurity=False).hexdigest()
        ), f"Device ID is not correct: {deviceid}"
