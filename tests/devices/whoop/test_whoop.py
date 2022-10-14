# content of test_sample.py
import wearipedia

# def test_whoop_api():
#    device = wearipedia.get_device("whoop/whoop_4")
#
#    email = input("email: ")
#    password = input("password: ")
#
#    device.authorize({"email": email, "password": password})
#
#    cycles_df = device.get_data("cycles")
#
#    metrics_df = device.get_data("health_metrics")


def test_whoop_synthetic():
    device = wearipedia.get_device("whoop/whoop_4")

    device.gen_synthetic()

    cycles_df = device.get_data("cycles")

    metrics_df = device.get_data("health_metrics")
