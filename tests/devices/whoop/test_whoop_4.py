from datetime import datetime

import pandas as pd
import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
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


def check_collection(collection_type: str, collection: pd.DataFrame):

    if collection_type == "sleeps":
        assert set(collection.columns) == {
            "id",
            "user_id",
            "created_at",
            "updated_at",
            "start",
            "end",
            "timezone_offset",
            "nap",
            "score_state",
            "score",
        }, f"Sleeps data is not correct: {collection}"
    elif collection_type == "workouts":
        assert set(collection.columns) == {
            "id",
            "user_id",
            "created_at",
            "updated_at",
            "start",
            "end",
            "timezone_offset",
            "sport_id",
            "score_state",
            "score",
        }, f"Cycles data is not correct: {collection}"
    elif collection_type == "cycles":
        assert set(collection.columns) == {
            "id",
            "user_id",
            "created_at",
            "updated_at",
            "start",
            "end",
            "timezone_offset",
            "score_state",
            "score",
        }, f"Cycles data is not correct: {collection}"

    # checking that id is >=0
    for id in collection["id"]:
        assert id >= 0, f"ID is not in range: {id}"

    # checking start, end, created_at, and updated_at relationships

    for _, row in collection.iterrows():
        start_str = row["start"]
        end_str = row["end"]
        created_at_str = row["created_at"]
        updated_at_str = row["updated_at"]

        # Convert strings to datetime objects
        start = pd.to_datetime(start_str, errors="coerce")
        end = pd.to_datetime(end_str, errors="coerce")
        created_at = pd.to_datetime(created_at_str, errors="coerce")
        updated_at = pd.to_datetime(updated_at_str, errors="coerce")

        # Check start, end, created_at, and updated_at relationships if they are not NaT
        if (
            not pd.isnull(start)
            and not pd.isnull(end)
            and not pd.isnull(created_at)
            and not pd.isnull(updated_at)
        ):
            assert start < end, f"Start is not earlier than end: {start}, {end}"
            assert (
                end < created_at
            ), f"End is not earlier than created_at: {end}, {created_at}"
            assert (
                created_at < updated_at
            ), f"Created_at is not earlier than updated_at: {created_at}, {updated_at}"


def helper_test(device, start_synthetic, end_synthetic, real):

    cycles = device.get_data("cycles")
    workouts = device.get_data("workouts")
    sleeps = device.get_data("sleeps")

    if len(sleeps) != 0 or not real:
        check_collection("sleeps", sleeps)

    if len(workouts) != 0 or not real:
        check_collection("workouts", workouts)

    if len(cycles) != 0 or not real:
        check_collection("cycles", cycles)
