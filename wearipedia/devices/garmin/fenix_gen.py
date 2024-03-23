from datetime import datetime, timedelta

from .fenix_gen_1 import *
from .fenix_gen_2 import *
from .fenix_gen_3 import *
from .fenix_gen_4 import *
from .fenix_gen_5 import *
from .fenix_gen_6 import *
from .fenix_gen_7 import *

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
        "daily_steps": get_daily_steps_data(start_date, num_days),
        "stats": get_stats_data(start_date, num_days),
        "body_composition": get_body_composition_data(start_date, num_days),
        "body_composition_aggregated": get_body_composition_aggregated_data(
            start_date, num_days
        ),
        "stats_and_body_aggregated": get_stats_and_body_aggregated_data(
            start_date, num_days
        ),
        "hr": None,
        "body_battery": get_body_battery_data(start_date, num_days),
        "training_readiness": get_training_readiness_data(start_date, num_days),
        "blood_pressure": get_blood_pressure_data(start_date, end_date, 100),
        "floors": get_floors_data(start_date, num_days),
        "training_status": get_training_status_data(start_date, num_days),
        "rhr": get_resting_hr_data(start_date, num_days),
        "hydration": get_hydration_data(start_date, num_days),
        "sleep": get_sleep_data(start_date, num_days),
        "earned_badges": get_earned_badges_data(start_date, num_days),
        "stress": get_stress_data(start_date, num_days),
        "day_stress_aggregated": get_day_stress_aggregated_data(start_date, num_days),
        "respiration": get_respiration_data(start_date, num_days),
        "spo2": get_spo2_data(start_date, num_days),
        "max_metrics": get_metrics_data(start_date, num_days),
        "personal_record": get_personal_record_data(start_date, end_date, num_days),
        "activities": get_activities_data(start_date, num_days),
        "activities_date": get_activities_date_data(start_date, num_days),
        "activities_fordate_aggregated": get_activities_fordate_aggregated_data(
            start_date, num_days
        ),
        "devices": get_devices_data(start_date, num_days),
        "device_last_used": get_device_last_used_data(start_date, num_days),
        "device_settings": get_device_settings_data(3),
        "device_alarms": get_device_alarms_data(start_date, num_days),
        "active_goals": get_active_goals_data(start_date, num_days),
        "future_goals": get_future_goals_data(start_date, num_days),
        "past_goals": get_past_goals_data(start_date, num_days),
        "weigh_ins": get_weigh_ins_data(start_date, num_days),
        "weigh_ins_daily": get_weigh_ins_daily_data(start_date, num_days),
        "hill_score": get_hill_score_data(
            start_date,
            end_date,
        ),
        "endurance_score": get_endurance_score_data(
            start_date,
            end_date,
        ),
        "adhoc_challenges": get_adhoc_challenges_data(start_date, num_days),
        "available_badges": get_available_badges_data(start_date, num_days),
        "available_badge_challenges": get_available_badge_challenges_data(
            start_date, num_days
        ),
        "badge_challenges": get_badge_challenges_data(start_date, num_days),
        "non_completed_badge_challenges": get_non_completed_badge_challenges_data(
            start_date, num_days
        ),
        "race_prediction": get_race_prediction_data(start_date, num_days),
        "inprogress_virtual_challenges": get_inprogress_virtual_challenges_data(
            start_date, num_days
        ),
    }

    synth_data["hr"] = get_heart_rate_data(start_date, num_days, synth_data["steps"])

    return synth_data
