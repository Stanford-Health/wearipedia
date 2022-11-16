# perform additional test specific to Whoop 4 device

from datetime import datetime

import wearipedia


def test_whoop_4_synthetic():
    start_dates = [datetime(2009, 11, 15), datetime(2021, 4, 1), datetime(2022, 6, 10)]
    end_dates = [datetime(2010, 2, 1), datetime(2021, 6, 20), datetime(2022, 8, 25)]

    for start_date, end_date in zip(start_dates, end_dates):
        device = wearipedia.get_device(
            "whoop/whoop_4",
            params={
                "synthetic_start_date": datetime.strftime(start_date, "%Y-%m-%d"),
                "synthetic_end_date": datetime.strftime(end_date, "%Y-%m-%d"),
            },
        )

        # calling tests for each pair of start and end dates
        helper_test(device, start_date, end_date)


def helper_test(device, start_synthetic, end_synthetic):

    cycles = device.get_data("cycles")
    health_metrics = device.get_data("health_metrics")
    sleeps = device.get_data("sleeps")
    hr = device.get_data("hr")

    # hr (heartrate) data is generated in 7 second interval instead of each day so length not compared with others
    assert (
        len(cycles)
        == len(health_metrics)
        == len(sleeps)
        == (end_synthetic - start_synthetic).days
    ), (
        f"Expected all data to be the same length and to match the number of days between"
        f" {start_synthetic} and {end_synthetic}, but got {len(cycles)}, {len(health_metrics)}, "
        f"{len(sleeps)}"
    )

    # first make sure that the cycles dates are correct and consecutive
    for cycle_1, cycle_2 in zip(cycles["day"][:-1], cycles["day"][1:]):
        assert (
            cycle_2 - cycle_1
        ).days == 1, f"Cycle dates are not consecutive: {cycle_1}, {cycle_2}"

    assert (
        cycles["day"][0] == start_synthetic
    ), f"First date is not correct: {cycles['day'][0]}"

    # we make sure that health_metrics data is correct and has days consecutive
    for health_metric_1, health_metric_2 in zip(
        health_metrics["day"][:-1], health_metrics["day"][1:]
    ):
        assert (
            health_metric_2 - health_metric_1
        ).days == 1, f"Health metrics dates are not consecutive: {health_metric_1}, {health_metric_2}"

    assert (
        health_metrics["day"][0] == start_synthetic
    ), f"First date is not correct: {health_metrics['day'][0]}"

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
    # checking heart rate is within the range of 0 to 500
    for resting_hr in cycles["resting_hr"]:
        assert (
            0 <= resting_hr <= 500
        ), f"Resting heart rate is not in correct range: {resting_hr}"

    for average_hr in cycles["avg_hr"]:
        assert (
            0 <= average_hr <= 500
        ), f"Average heart rate is not in correct range: {average_hr}"

    for max_hr in cycles["max_hr"]:
        assert (
            0 <= max_hr <= 500
        ), f"Maximum heart rate is not in correct range: {max_hr}"

    # checking number of naps are non negative
    for naps in cycles["n_naps"]:
        assert naps >= 0, f"Number of naps cannot be non negative: {naps}"

    # checking recovery score is within the range of 0 to 100
    for recovery_score in cycles["recovery_score"]:
        assert (
            0 <= recovery_score <= 100
        ), f"Recovery score is not in correct range: {recovery_score}"

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

    # checking for health_metrics data

    assert (
        health_metrics.columns
        == [
            "id",
            "day",
            "RESPIRATORY_RATE.current_value",
            "RESPIRATORY_RATE.current_deviation",
            "BLOOD_OXYGEN.current_value",
            "BLOOD_OXYGEN.current_deviation",
            "RHR.current_value",
            "RHR.current_deviation",
            "HRV.current_value",
            "HRV.current_deviation",
            "SKIN_TEMPERATURE_CELSIUS.current_value",
            "SKIN_TEMPERATURE_CELSIUS.current_deviation",
            "SKIN_TEMPERATURE_FAHRENHEIT.current_value",
            "SKIN_TEMPERATURE_FAHRENHEIT.current_deviation",
        ]
    ).all(), f"Health metrics data is not correct: {health_metrics}"

    # checking columns within health_metrics dataframe

    # checking respiratory rate is within the range of 0 to 100
    for respiratory_rate in health_metrics["RESPIRATORY_RATE.current_value"]:
        assert (
            0 <= respiratory_rate <= 100
        ), f"Respiratory rate is not in correct range: {respiratory_rate}"

    # checking that blood oxygen is within the range of 0 to 100
    for bo in health_metrics["BLOOD_OXYGEN.current_value"]:
        assert 0 <= bo <= 100, (
            f"Blood oxygen current value is not correct: {bo}"
            f"Expected a value between 0 and 100, but got {bo}"
        )

    # checking that resting heart rate is within the range of 0 to 500
    for rhr in health_metrics["RHR.current_value"]:
        assert (
            0 <= rhr <= 500
        ), f"Resting heart rate current value is not correct: {rhr}"

    for hr_value in health_metrics["HRV.current_value"]:
        assert (
            0 <= hr_value <= 500
        ), f"Current heart rate value is not correct: {hr_value}"

    for temperature in health_metrics["SKIN_TEMPERATURE_CELSIUS.current_value"]:
        assert (
            0 <= temperature <= 60
        ), f"Current celsius temperature value is not correct: {temperature}"

    for f_temperature in health_metrics["SKIN_TEMPERATURE_FAHRENHEIT.current_value"]:
        assert (
            32 <= f_temperature <= 140
        ), f"Current fahrenheit temperature value is not correct: {f_temperature}"

    # checking for sleeps data
    assert (
        sleeps.columns
        == [
            "cycle_id",
            "sleep_id",
            "cycles_count",
            "disturbance_count",
            "time_upper_bound",
            "time_lower_bound",
            "is_nap",
            "in_bed_duration",
            "light_sleep_duration",
            "latency_duration",
            "no_data_duration",
            "rem_sleep_duration",
            "respiratory_rate",
            "sleep_score",
            "sleep_efficiency",
            "sleep_consistency",
            "sws_duration",
            "wake_duration",
            "quality_duration",
        ]
    ).all(), f"Sleep data is not correct: {sleeps}"

    # checking columns within sleeps dataframe

    # checking respiratory rate is within the range of 0 to 100
    for respiratory_rate in sleeps["respiratory_rate"]:
        assert (
            0 <= respiratory_rate <= 100
        ), f"Respiratory rate is not in correct range: {respiratory_rate}"

    # checking sleep score is within the range of 0 to 100
    for sleep_score in sleeps["sleep_score"]:
        assert (
            0 <= sleep_score <= 100
        ), f"Sleep score is not in correct range: {sleep_score}"

    # checking sleep consistency is within the range of 0 to 1
    for sleep_consistency in sleeps["sleep_consistency"]:
        assert (
            0 <= sleep_consistency <= 1
        ), f"Sleep consistency is not in correct range: {sleep_consistency}"

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
