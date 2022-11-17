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

    # checking that respiratory rate deviation is within the range of -3 to 3
    for respiratory_rate_deviation in health_metrics[
        "RESPIRATORY_RATE.current_deviation"
    ]:
        assert (
            -3 <= respiratory_rate_deviation <= 3
        ), f"Respiratory rate deviation is not in correct range: {respiratory_rate_deviation}"

    # checking that blood oxygen is within the range of 0 to 100
    for bo in health_metrics["BLOOD_OXYGEN.current_value"]:
        assert 0 <= bo <= 100, (
            f"Blood oxygen current value is not correct: {bo}"
            f"Expected a value between 0 and 100, but got {bo}"
        )

    # checking that blood oxygen deviation is within the range of -3 to 3
    for bo_deviation in health_metrics["BLOOD_OXYGEN.current_deviation"]:
        assert (
            -3 <= bo_deviation <= 3
        ), f"Blood oxygen deviation is not in correct range: {bo_deviation}"

    # checking that resting heart rate is within the range of 0 to 500
    for rhr in health_metrics["RHR.current_value"]:
        assert (
            0 <= rhr <= 500
        ), f"Resting heart rate current value is not correct: {rhr}"

    # checking that resting heart rate deviation is within the range of -3 to 3
    for rhr_deviation in health_metrics["RHR.current_deviation"]:
        assert (
            -3 <= rhr_deviation <= 3
        ), f"Resting heart rate deviation is not in correct range: {rhr_deviation}"

    # checking that heart rate value is within the range of 0 to 100
    for hr_value in health_metrics["HRV.current_value"]:
        assert (
            0 <= hr_value <= 500
        ), f"Current heart rate value is not correct: {hr_value}"

    # checking that heart rate deviation is within the range of -3 to 3
    for hr_deviation in health_metrics["HRV.current_deviation"]:
        assert (
            -3 <= hr_deviation <= 3
        ), f"Current heart rate deviation is not correct: {hr_deviation}"

    # checking that celsius temperature  is within the range of 0 to 100
    for temperature in health_metrics["SKIN_TEMPERATURE_CELSIUS.current_value"]:
        assert (
            0 <= temperature <= 60
        ), f"Current celsius temperature value is not correct: {temperature}"

    # checking that celsius temperature deviation is within the range of -3 to 3
    for temperature_deviation in health_metrics[
        "SKIN_TEMPERATURE_CELSIUS.current_deviation"
    ]:
        assert (
            -3 <= temperature_deviation <= 3
        ), f"Current celsius temperature deviation is not correct: {temperature_deviation}"

    # checking that fahrenheit temperature  is within the range of 0 to 100
    for f_temperature in health_metrics["SKIN_TEMPERATURE_FAHRENHEIT.current_value"]:
        assert (
            32 <= f_temperature <= 140
        ), f"Current fahrenheit temperature value is not correct: {f_temperature}"

    # checking that fahrenheit temperature deviation is within the range of -3 to 3
    for f_temperature_deviation in health_metrics[
        "SKIN_TEMPERATURE_FAHRENHEIT.current_deviation"
    ]:
        assert (
            -3 <= f_temperature_deviation <= 3
        ), f"Current fahrenheit temperature deviation is not correct: {f_temperature_deviation}"

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

    # checking that cycles count is non negative
    for cycles_count in sleeps["cycles_count"]:
        assert cycles_count >= 0, f"Cycles count cannot be negative: {cycles_count}"

    # checking that disturbance count is non negative
    for disturbance_count in sleeps["disturbance_count"]:
        assert (
            disturbance_count >= 0
        ), f"Disturbance count cannot be negative: {disturbance_count}"

    # checking that is_nap is either True or False
    for is_nap in sleeps["is_nap"]:
        assert is_nap in [True, False], f"Is nap is not correct: {is_nap}"

    # checking that in_bed_duration is non negative
    for in_bed_duration in sleeps["in_bed_duration"]:
        assert (
            in_bed_duration >= 0
        ), f"In bed duration cannot be negative: {in_bed_duration}"

    # checking that light_sleep_duration is non negative
    for light_sleep_duration in sleeps["light_sleep_duration"]:
        assert (
            light_sleep_duration >= 0
        ), f"Light sleep duration cannot be negative: {light_sleep_duration}"

    # checking that latency_duration is non negative
    for latency_duration in sleeps["latency_duration"]:
        assert (
            latency_duration >= 0
        ), f"Latency duration cannot be negative: {latency_duration}"

    # checking that no_data_duration is non negative
    for no_data_duration in sleeps["no_data_duration"]:
        assert (
            no_data_duration >= 0
        ), f"No data duration cannot be negative: {no_data_duration}"

    # checking that rem_sleep_duration is non negative
    for rem_sleep_duration in sleeps["rem_sleep_duration"]:
        assert (
            rem_sleep_duration >= 0
        ), f"REM sleep duration cannot be negative: {rem_sleep_duration}"

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

    # checking sleep efficiency is within the range of 0 to 1
    for sleep_efficiency in sleeps["sleep_efficiency"]:
        assert (
            0 <= sleep_efficiency <= 1
        ), f"Sleep efficiency is not in correct range: {sleep_efficiency}"

    # checking sleep consistency is within the range of 0 to 1
    for sleep_consistency in sleeps["sleep_consistency"]:
        assert (
            0 <= sleep_consistency <= 1
        ), f"Sleep consistency is not in correct range: {sleep_consistency}"

    # checking that sws_duration is non negative
    for sws_duration in sleeps["sws_duration"]:
        assert sws_duration >= 0, f"SWS duration cannot be negative: {sws_duration}"

    # checking that wake_duration is non negative
    for wake_duration in sleeps["wake_duration"]:
        assert wake_duration >= 0, f"Wake duration cannot be negative: {wake_duration}"

    # checking that quality_duration is non negative
    for quality_duration in sleeps["quality_duration"]:
        assert (
            quality_duration >= 0
        ), f"Quality duration cannot be negative: {quality_duration}"

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
