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


def sleeps_data_helper(data):
    # Series data has each row as a dictionary, we check the keys for each attribute
    for d in data:
        return (
            (lambda df, c: True if 0 <= df[c] <= 3000 else False)(d, "wakeupduration")
            and (lambda df, c: True if df[c] >= 0 else False)(d, "wakeupcount")
            and (lambda df, c: True if 120 <= df[c] <= 180 else False)(
                d, "durationtosleep"
            )
            and (lambda df, c: True if 0 <= df[c] <= 700 else False)(
                d, "durationtowakeup"
            )
            and (lambda df, c: True if 10000 <= df[c] <= 50000 else False)(
                d, "total_timeinbed"
            )
            and (lambda df, c: True if 10000 <= df[c] <= 50000 else False)(
                d, "total_sleep_time"
            )
            and (lambda df, c: True if 0 <= df[c] <= 1 else False)(
                d, "sleep_efficiency"
            )
            and (lambda df, c: True if 120 <= df[c] <= 300 else False)(
                d, "sleep_latency"
            )
            and (lambda df, c: True if 0 <= df[c] <= 800 else False)(
                d, "wakeup_latency"
            )
            and (lambda df, c: True if 0 <= df[c] <= 4000 else False)(d, "waso")
            and (lambda df, c: True if df[c] >= 0 else False)(d, "nb_rem_episodes")
            and (lambda df, c: True if df[c] >= 0 else False)(d, "out_of_bed_count")
            and (lambda df, c: True if 6000 <= df[c] <= 35000 else False)(
                d, "lightsleepduration"
            )
            and (lambda df, c: True if 3000 <= df[c] <= 17000 else False)(
                d, "deepsleepduration"
            )
            and (lambda df, c: True if 55 <= df[c] <= 65 else False)(d, "hr_average")
            and (lambda df, c: True if 40 <= df[c] <= 60 else False)(d, "hr_min")
            and (lambda df, c: True if 70 <= df[c] <= 120 else False)(d, "hr_max")
            and (lambda df, c: True if 30 <= df[c] <= 80 else False)(d, "sleep_score")
        )


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

    # checking the column sleeps["data"], a Series which contains 18 attributes
    # calling helper function to check each of the attributes
    assert (
        sleeps_data_helper(sleeps["data"]) == True
    ), f"Sleeps data is not correct: {sleeps['data']}"

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
