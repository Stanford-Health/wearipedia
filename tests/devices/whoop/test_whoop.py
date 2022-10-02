# content of test_sample.py
import wearipedia


def test_whoop():
    device = wearipedia.get_device("whoop/whoop_4")

    device.gen_synthetic_data()

    cycles_df = device.get_data("cycles")

    metrics_df = device.get_data("metrics")


def test_answer():
    assert func(3) == 5
