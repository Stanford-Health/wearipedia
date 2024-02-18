import os
import pickle
from datetime import datetime

import garth
from garminconnect import Garmin

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .fenix_fetch import *
from .fenix_gen import *

class_name = "Fenix7S"

# todo: change this to better path
CRED_CACHE_PATH = "/tmp/wearipedia_fenix_data.pkl"


class Fenix7S(BaseDevice):
    """This device allows you to work with data from the `Garmin Fenix 7S <https://www.garmin.com/en-US/p/735542>`_ device.
    Available datatypes for this device are:

    * `dates`: a list of consecutive dates
    * `stats`: a sibling list to `dates` that contains general statistics data for each day
    * `body_composition`: a sibling list to `dates` that contains body composition data for each day
    * `body_composition_aggregated`: a sibling list to `dates` that contains aggregated body composition data for each day
    * `stats_and_body_aggregated`: a sibling list to `dates` that contains aggregated statistics and body composition data for each day
    * `steps`: a sibling list to `dates` that contains step data for each day
    * `daily_steps`: a sibling list to `dates` that contains daily step data for each day
    * `body_battery`: a sibling list to `dates` that contains body battery data for each day
    * `hr`: a sibling list to `dates` that contains heart rate data for each day
    * `training_readiness`: a sibling list to `dates` that contains training readiness data for each day
    * `blood_pressure`: a sibling list to `dates` that contains blood pressure data for each day
    * `floors`: a sibling list to `dates` that contains floors data for each day
    * `training_status`: a sibling list to `dates` that contains training status data for each day
    * `rhr`: a sibling list to `dates` that contains resting heart rate data for each day
    * `hydration`: a sibling list to `dates` that contains hydration data for each day
    * `sleep`: a sibling list to `dates` that contains sleep data for each day
    * `stress`: a sibling list to `dates` that contains stress data for each day
    * `day_stress_aggregated`: a sibling list to `dates` that contains day stress aggregated data for each day
    * `respiration`: a sibling list to `dates` that contains respiration data for each day
    * `race_prediction`: a sibling list to `dates` that contains race prediction data for each day
    * `spo2`: a sibling list to `dates` that contains blood oxygen saturation data for each day
    * `max_metrics`: a sibling list to `dates` that contains maximum metrics data for each day
    * `personal_record`: a sibling list to `dates` that contains personal record data for each day
    * `earned_badges`: a sibling list to `dates` that contains earned badges data for each day
    * `adhoc_challenges`: a sibling list to `dates` that contains adhoc challenges data for each day
    * `available_badges`: a sibling list to `dates` that contains available badges data for each day
    * `available_badge_challenges`: a sibling list to `dates` that contains available badge challenges data for each day
    * `badge_challenges`: a sibling list to `dates` that contains badge challenges data for each day
    * `non_completed_badge_challenges`: a sibling list to `dates` that contains non-completed badge challenges data for each day
    * `activities`: a sibling list to `dates` that contains activity data for each day
    * `activities_date`: a sibling list to `dates` that contains activity date data for each day
    * `activities_fordate_aggregated`: a sibling list to `dates` that contains activities for date aggregated data for each day
    * `devices`: a sibling list to `dates` that contains device data for each day
    * `device_last_used`: a sibling list to `dates` that contains device last used data for each day
    * `device_settings`: a sibling list to `dates` that contains device settings data for each day
    * `device_alarms`: a sibling list to `dates` that contains device alarms data for each day
    * `active_goals`: a sibling list to `dates` that contains active goals data for each day
    * `future_goals`: a sibling list to `dates` that contains future goals data for each day
    * `past_goals`: a sibling list to `dates` that contains past goals data for each day
    * `hrv`: a sibling list to `dates` that contains heart rate variability data for each day
    * `weigh_ins`: a sibling list to `dates` that contains weigh-ins data for each day
    * `weigh_ins_daily`: a sibling list to `dates` that contains daily weigh-ins data for each day
    * `hill_score`: a sibling list to `dates` that contains hill score data for each day
    * `endurance_score`: a sibling list to `dates` that contains endurance score data for each day
    * `inprogress_virtual_challenges`: a sibling list to `dates` that contains in-progress virtual challenges data for each day



    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param use_cache: decide whether to cache the credentials, defaults to True
    :type use_cache: bool, optional
    """

    def __init__(
        self,
        seed=0,
        synthetic_start_date="2022-03-01",
        synthetic_end_date="2022-06-17",
        use_cache=True,
    ):
        # use_cache just means that we'll use the cached credentials
        # as opposed to re-authenticating every time (the API tends to
        # rate-limit a lot, see this GitHub issue:
        # https://github.com/cyberjunky/python-garminconnect/issues/85

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
            "use_cache": use_cache,
        }

        self._initialize_device_params(
            [
                "stats",
                "body_composition",
                "body_composition_aggregated",
                "stats_and_body_aggregated",
                "steps",
                "daily_steps",
                "body_battery",
                "hr",
                "training_readiness",
                "blood_pressure",
                "floors",
                "training_status",
                "rhr",
                "hydration",
                "sleep",
                "stress",
                "day_stress_aggregated",
                "respiration",
                "race_prediction",
                "spo2",
                "max_metrics",
                "personal_record",
                "earned_badges",
                "adhoc_challenges",
                "available_badges",
                "available_badge_challenges",
                "badge_challenges",
                "non_completed_badge_challenges",
                "activities",
                "activities_date",
                "activities_fordate_aggregated",
                "devices",
                "device_last_used",
                "device_settings",
                "device_alarms",
                "active_goals",
                "future_goals",
                "past_goals",
                "hrv",
                "weigh_ins",
                "weigh_ins_daily",
                "hill_score",
                "endurance_score",
                "dates",
                "inprogress_virtual_challenges",
            ],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
                "use_cache": True,
            },
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start_date"],
            "end_date": self.init_params["synthetic_end_date"],
        }

    def _get_real(self, data_type, params):
        return fetch_real_data(
            params["start_date"], params["end_date"], data_type, self.api
        )

    def _filter_synthetic(self, data, data_type, params):
        # Here we just return the data we've already generated,
        # but index into it based on the params. Specifically, we
        # want to return the data between the start and end dates.

        # Data also contains Dicts along with lists, so we can't slice directly
        # As data is already filtered, we just return the data
        return data

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])
        # and based on start and end dates

        synth_data = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )
        self.dates = synth_data["dates"]
        self.hrv = synth_data["hrv"]
        self.steps = synth_data["steps"]
        self.daily_steps = synth_data["daily_steps"]
        self.stats = synth_data["stats"]
        self.body_composition = synth_data["body_composition"]
        self.body_composition_aggregated = synth_data["body_composition_aggregated"]
        self.stats_and_body_aggregated = synth_data["stats_and_body_aggregated"]
        self.hr = synth_data["hr"]
        self.body_battery = synth_data["body_battery"]
        self.training_readiness = synth_data["training_readiness"]
        self.blood_pressure = synth_data["blood_pressure"]
        self.floors = synth_data["floors"]
        self.training_status = synth_data["training_status"]
        self.rhr = synth_data["rhr"]
        self.hydration = synth_data["hydration"]
        self.sleep = synth_data["sleep"]
        self.earned_badges = synth_data["earned_badges"]
        self.stress = synth_data["stress"]
        self.day_stress_aggregated = synth_data["day_stress_aggregated"]
        self.respiration = synth_data["respiration"]
        self.spo2 = synth_data["spo2"]
        self.max_metrics = synth_data["max_metrics"]
        self.personal_record = synth_data["personal_record"]
        self.activities = synth_data["activities"]
        self.activities_date = synth_data["activities_date"]
        self.activities_fordate_aggregated = synth_data["activities_fordate_aggregated"]
        self.devices = synth_data["devices"]
        self.device_last_used = synth_data["device_last_used"]
        self.device_settings = synth_data["device_settings"]
        self.device_alarms = synth_data["device_alarms"]
        self.active_goals = synth_data["active_goals"]
        self.future_goals = synth_data["future_goals"]
        self.past_goals = synth_data["past_goals"]
        self.weigh_ins = synth_data["weigh_ins"]
        self.weigh_ins_daily = synth_data["weigh_ins_daily"]
        self.hill_score = synth_data["hill_score"]
        self.endurance_score = synth_data["endurance_score"]
        self.adhoc_challenges = synth_data["adhoc_challenges"]
        self.available_badges = synth_data["available_badges"]
        self.available_badge_challenges = synth_data["available_badge_challenges"]
        self.badge_challenges = synth_data["badge_challenges"]
        self.non_completed_badge_challenges = synth_data[
            "non_completed_badge_challenges"
        ]
        self.race_prediction = synth_data["race_prediction"]
        self.inprogress_virtual_challenges = synth_data["inprogress_virtual_challenges"]

    def _authenticate(self, auth_creds):
        # check if we have cached credentials
        if self.init_params["use_cache"] and os.path.exists(CRED_CACHE_PATH):
            self.api = pickle.load(open(CRED_CACHE_PATH, "rb"))
        else:
            self.api = garth.Client(domain="garmin.com")
            self.api.login(auth_creds["email"], auth_creds["password"])
            pickle.dump(self.api, open(CRED_CACHE_PATH, "wb"))
