# content of test_sample.py
import wearipedia


def test_whoop_synthetic():
    device = wearipedia.get_device("whoop/whoop_4")

    cycles_df = device.get_data("cycles")

    health_metrics_df = device.get_data("health_metrics")

    sleeps_df = device.get_data("sleeps")

    hr_df = device.get_data("hr")
