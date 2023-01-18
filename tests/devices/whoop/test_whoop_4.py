# perform additional test specific to Whoop 4 device

from datetime import datetime

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
        helper_test(device, start_date, end_date)


def helper_test(device, start_synthetic, end_synthetic):

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

    # hr (heartrate) data is generated in 7 second interval instead of each day so length not compared with others
    assert len(cycles) == (end_synthetic - start_synthetic).days, (
        f"Expected all data to be the same length and to match the number of days between"
        f" {start_synthetic} and {end_synthetic}, but got {len(cycles)}"
    )

    # first make sure that the cycles dates are correct and consecutive
    for cycle_1, cycle_2 in zip(cycles["day"][:-1], cycles["day"][1:]):
        assert (
            cycle_2 - cycle_1
        ).days == 1, f"Cycle dates are not consecutive: {cycle_1}, {cycle_2}"

    assert (
        cycles["day"][0] == start_synthetic
    ), f"First date is not correct: {cycles['day'][0]}"

    # Now we make sure that the data in each dataframe (cycles, health_metrics, sleeps, and hr) is correct
    # checking for cycles data

    assert (
        cycles.columns
        == [
            "id",
            "day",
            "rMSSD",
            "resting_hr",
            "recovery_score",
            "n_naps",
            "sleep_need_baseline",
            "sleep_debt",
            "sleep_need_strain",
            "sleep_need_total",
            "sleep_quality_duration",
            "avg_hr",
            "kilojoules",
            "max_hr",
            "strain_score",
        ]
    ).all(), f"Cycles data is not correct: {cycles}"

    # checking columns within cycles dataframe

    # checking that rMMSD is within the range of 0 to 0.2
    for rMSSD in cycles["rMSSD"]:
        assert 0 <= rMSSD <= 0.2, f"rMSSD is not in correct range: {rMSSD}"

    # checking heart rate is within the range of 0 to 500
    for resting_hr in cycles["resting_hr"]:
        assert (
            0 <= resting_hr <= 500
        ), f"Resting heart rate is not in correct range: {resting_hr}"

    # checking recovery score is within the range of 0 to 100
    for recovery_score in cycles["recovery_score"]:
        assert (
            0 <= recovery_score <= 100
        ), f"Recovery score is not in correct range: {recovery_score}"

    # checking number of naps are non negative
    for naps in cycles["n_naps"]:
        assert naps >= 0, f"Number of naps cannot be negative: {naps}"

    # checking that sleep need baseline is non negative
    for sleep_need_baseline in cycles["sleep_need_baseline"]:
        assert (
            sleep_need_baseline >= 0
        ), f"Sleep need baseline cannot be negative: {sleep_need_baseline}"

    # checking that sleep debt is non negative
    for sleep_debt in cycles["sleep_debt"]:
        assert sleep_debt >= 0, f"Sleep debt cannot be negative: {sleep_debt}"

    # checking that sleep need strain is non negative
    for sleep_need_strain in cycles["sleep_need_strain"]:
        assert (
            sleep_need_strain >= 0
        ), f"Sleep need strain cannot be negative: {sleep_need_strain}"

    # checking that sleep need total is non negative
    for sleep_need_total in cycles["sleep_need_total"]:
        assert (
            sleep_need_total >= 0
        ), f"Sleep need total cannot be negative: {sleep_need_total}"

    # checking that sleep quality duration is non negative
    for sleep_quality_duration in cycles["sleep_quality_duration"]:
        assert (
            sleep_quality_duration >= 0
        ), f"Sleep quality duration cannot be negative: {sleep_quality_duration}"

    # checking that average heart rate is within the range of 0 to 500
    for average_hr in cycles["avg_hr"]:
        assert (
            0 <= average_hr <= 500
        ), f"Average heart rate is not in correct range: {average_hr}"

    for max_hr in cycles["max_hr"]:
        assert (
            0 <= max_hr <= 500
        ), f"Maximum heart rate is not in correct range: {max_hr}"

    # checking strain score is within the range of 0 to 21
    for strain_score in cycles["strain_score"]:
        assert (
            0 <= strain_score <= 21
        ), f"Strain score is not in correct range: {strain_score}"

    # checking kilojoules is within the range of 0 to 20000
    for kilojoules in cycles["kilojoules"]:
        assert (
            0 <= kilojoules <= 20000
        ), f"Kilojoules is not in correct range: {kilojoules}"

    # checking for hr data
    assert (
        hr.columns == ["heart_rate", "timestamp"]
    ).all(), f"Heart rate data is not correct: {hr}"

    # checking columns within hr dataframe

    # make sure heart rate is within the range of 0 to 500
    # for heart_rate in hr["heart_rate"]:
    #     assert (
    #         0 <= heart_rate <= 500
    #     ), f"Heart rate is not in correct range: {heart_rate}"

    # make sure timestamps are at 7s intervals
    for timestamp1, timestamp2 in zip(hr["timestamp"][:-1], hr["timestamp"][1:]):
        assert (
            int((timestamp2 - timestamp1).total_seconds()) == 7
        ), f"Timestamps are not at 7s intervals: {timestamp1}, {timestamp2}"
