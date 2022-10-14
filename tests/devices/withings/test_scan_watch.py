# content of test_sample.py
import wearipedia

# def test_scanwatch_api():
#    device = wearipedia.get_device("withings/scanwatch")
#
#    email = input("client_id: ")
#    password = input("customer_secret: ")
#
#    device.authorize({"client_id": email, "customer_secret": password})
#
#    hrs = device.get_data("heart_rates")


def test_whoop_synthetic():
    device = wearipedia.get_device("whoop/whoop_4")

    device.gen_synthetic()

    hrs = device.get_data("health_metrics")
