# perform additional test specific to Whoop 4 device

from datetime import datetime, timedelta

import pytest
from dateutil import parser

import wearipedia


def check_keys(d, expected_keys):
    assert (
        list(d.keys()) == expected_keys
    ), f"Expected keys to be {expected_keys}, but got {d.keys()}"


@pytest.mark.parametrize("real", [False])
def test_whoop_4_synthetic(real):
    start_dates = [datetime(2009, 11, 15), datetime(2021, 4, 1), datetime(2022, 6, 10)]
    end_dates = [datetime(2010, 2, 1), datetime(2021, 6, 20), datetime(2022, 8, 25)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "whoop/whoop_4",
            synthetic_start_date=datetime.strftime(start_date, "%Y-%m-%d"),
            synthetic_end_date=datetime.strftime(end_date, "%Y-%m-%d"),
        )

        if real:
            wearipedia._authenticate_device("whoop/whoop_4", device)

        # calling tests for each pair of start and end dates
        helper_test(device, start_date, end_date, real)


def helper_test(device, start_synthetic, end_synthetic, real):

    if real:
        # whoop limits to 192 hour intervals of difference
        end_synthetic = start_synthetic + timedelta(days=7)

    cycles = device.get_data(
        "cycles",
        params={
            "start": datetime.strftime(start_synthetic, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "end": datetime.strftime(end_synthetic, "%Y-%m-%dT%H:%M:%S.%fZ"),
        },
    )
    hr = device.get_data(
        "hr",
        params={
            "start": datetime.strftime(start_synthetic, "%Y-%m-%dT%H:%M:%S.%fZ"),
            "end": datetime.strftime(end_synthetic, "%Y-%m-%dT%H:%M:%S.%fZ"),
        },
    )

    assert (
        cycles["total_count"]
        == len(cycles["records"])
        <= (end_synthetic - start_synthetic).days
    ), (
        f"Expected all data to be the same length and to match or undercut the number of days between"
        f" {start_synthetic} and {end_synthetic}, but got {len(cycles)}"
    )

    # first make sure that the cycles dates are correct and consecutive
    get_day = lambda cycle: parser.parse(cycle["cycle"]["days"].split("'")[1])

    for cycle_1, cycle_2 in zip(cycles["records"][:-1], cycles["records"][1:]):

        c1, c2 = get_day(cycle_1), get_day(cycle_2)

        assert (
            c1 - c2
        ).days >= 1, f"Cycle dates are not consecutive: {cycle_1}, {cycle_2}"

    if len(cycles["records"]) > 0:
        first_record = cycles["records"][-1]
        assert (
            get_day(first_record) == start_synthetic
        ), f"First date is not correct: {get_day(first_record)}"

    # Now we make sure that the data in each dataframe (cycles, health_metrics, sleeps, and hr) is correct
    # checking for cycles data

    check_keys(cycles, ["total_count", "offset", "records"])

    for record in cycles["records"]:
        check_keys(record, ["cycle", "sleeps", "recovery", "workouts", "v2_activities"])
        check_keys(
            record["cycle"],
            [
                "id",
                "created_at",
                "updated_at",
                "scaled_strain",
                "during",
                "user_id",
                "sleep_need",
                "predicted_end",
                "timezone_offset",
                "days",
                "intensity_score",
                "data_state",
                "day_strain",
                "day_kilojoules",
                "day_avg_heart_rate",
                "day_max_heart_rate",
            ],
        )
        assert type(record["sleeps"]) == type(
            []
        ), f"expected sleeps to be a list, but got {type(record['sleeps'])}"
        check_keys(
            record["recovery"],
            [
                "during",
                "id",
                "created_at",
                "updated_at",
                "date",
                "user_id",
                "sleep_id",
                "survey_response_id",
                "cycle_id",
                "responded",
                "recovery_score",
                "resting_heart_rate",
                "hrv_rmssd",
                "state",
                "calibrating",
                "prob_covid",
                "hr_baseline",
                "skin_temp_celsius",
                "spo2",
                "algo_version",
                "rhr_component",
                "hrv_component",
                "history_size",
                "from_sws",
                "recovery_rate",
                "is_normal",
            ],
        )
        assert type(record["workouts"]) == type(
            []
        ), f"expected workouts to be a list, but got {type(record['workouts'])}"
        assert type(record["v2_activities"]) == type(
            []
        ), f"expected v2_activities to be a list, but got {type(record['v2_activities'])}"

    # TODO: check more stuff
