from datetime import datetime, timedelta

from .fenix_gen_1 import (
    get_body_battery_data,
    get_heart_rate_data,
    get_hrv_data,
    get_steps_data,
)
from .fenix_gen_2 import (
    get_blood_pressure_data,
    get_floors_data,
    get_hydration_data,
    get_resting_hr_data,
)
from .fenix_gen_3 import (
    get_respiration_data,
    get_sleep_data,
    get_spo2_data,
    get_stress_data,
)

__all__ = ["create_syn_data"]


def create_syn_data(start_date, end_date):
    """
    Returns a dictionary of synthetic health and activity data for a specified date range.
    :param start_date: the start date (inclusive) as a string in the format "YYYY-MM-DD"
    :type start_date: str
    :param end_date: the end date (inclusive) as a string in the format "YYYY-MM-DD"
    :type end_date: str
    :return: A dictionary containing synthetic data for various health and activity metrics, each
        element is a list or dictionary representing data for a specific day.
    :rtype: Dict
    """

    num_days = (
        datetime.strptime(end_date, "%Y-%m-%d")
        - datetime.strptime(start_date, "%Y-%m-%d")
    ).days

    synth_data = {
        "dates": [
            datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)
            for i in range(num_days)
        ],
        "hrv": get_hrv_data(start_date, num_days),
        "steps": get_steps_data(start_date, num_days),
        "hr": None,
        "body_battery": get_body_battery_data(start_date, num_days),
        "blood_pressure": get_blood_pressure_data(start_date, end_date, 100),
        "floors": get_floors_data(start_date, num_days),
        "rhr": get_resting_hr_data(start_date, num_days),
        "hydration": get_hydration_data(start_date, num_days),
        "sleep": get_sleep_data(start_date, num_days),
        "stress": get_stress_data(start_date, num_days),
        "respiration": get_respiration_data(start_date, num_days),
        "spo2": get_spo2_data(start_date, num_days),
    }

    synth_data["hr"] = get_heart_rate_data(start_date, num_days, synth_data["steps"])

    return synth_data
