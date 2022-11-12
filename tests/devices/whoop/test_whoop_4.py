# perform additional test specific to Whoop 4 device

from datetime import datetime

import wearipedia


def test_whoop_4_synthetic():
    # first testing with default params

    start_synthetic = datetime(2021, 1, 1)
    end_synthetic = datetime(2021, 3, 18)

    device = wearipedia.get_device(
        "whoop/whoop_4",
        params={
            "synthetic_start_date": datetime.strftime(start_synthetic, "%Y-%m-%d"),
            "synthetic_end_date": datetime.strftime(end_synthetic, "%Y-%m-%d"),
        },
    )

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

    # Now we make sure that each dataframes [cycles, health_metrics, sleeps and hr ] data are correct
    # checking for cycles data

    assert (
        (cycles.columns)
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
            resting_hr >= 0 and resting_hr <= 500
        ), f"Resting heart rate is not in correct range: {resting_hr}"

    for average_hr in cycles["avg_hr"]:
        assert (
            average_hr >= 0 and average_hr <= 500
        ), f"Average heart rate is not in correct range: {average_hr}"

    # checking for health_metrics data

    assert (
        (health_metrics.columns)
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
    # checking that blood oxygen is within the range of 0 to 100
    for bo in health_metrics["BLOOD_OXYGEN.current_value"]:
        assert bo >= 0 and bo <= 100, (
            f"Blood oxygen current value is not correct: {bo}"
            f"Expected a value between 0 to 100, but got {bo}"
        )

    for hr_value in health_metrics["HRV.current_value"]:
        assert (
            hr_value >= 0 and hr_value <= 500
        ), f"Current heart rate value is not correct: {hr_value}"

    for temperature in health_metrics["SKIN_TEMPERATURE_CELSIUS.current_value"]:
        assert (
            temperature >= 0 and temperature <= 60
        ), f"Current celsius temperature value is not correct: {temperature}"

    for f_temperature in health_metrics["SKIN_TEMPERATURE_FAHRENHEIT.current_value"]:
        assert (
            f_temperature >= 32 and f_temperature <= 140
        ), f"Current fahrenheit temperature value is not correct: {f_temperature}"

    # checking for sleeps data
    assert (
        (sleeps.columns)
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

    # checking for hr data
    assert (
        (hr.columns) == ["heart_rate", "timestamp"]
    ).all(), f"Heart rate data is not correct: {hr}"
