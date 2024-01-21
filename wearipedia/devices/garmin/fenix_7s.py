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

    * `steps`: a sibling list to `dates` that contains step data for each day

    * `hrs`: a sibling list to `dates` that contains heart rate data for each day

    * `hr`: a sibling list to `dates` that contains heart rate data for each day

    * `stats`: a sibling list to `dates` that contains general statistics data for each day

    * `user_summary`: a sibling list to `dates` that contains user summary data for each day

    * `body_composition`: a sibling list to `dates` that contains body composition data for each day

    * `training_readiness`: a sibling list to `dates` that contains training readiness data for each day

    * `blood_pressure`: a sibling list to `dates` that contains blood pressure data for each day

    * `floors`: a dictionary containing floors data for the specified date range

    * `training_status`: a sibling list to `dates` that contains training status data for each day

    * `resting_hr`: a sibling list to `dates` that contains resting heart rate data for each day

    * `hydration`: a sibling list to `dates` that contains hydration data for each day

    * `sleep`: a sibling list to `dates` that contains sleep data for each day

    * `earned_badges`: a sibling list to `dates` that contains earned badges data for each day

    * `stress`: a sibling list to `dates` that contains stress data for each day

    * `respiration`: a sibling list to `dates` that contains respiration data for each day

    * `spo2`: a sibling list to `dates` that contains blood oxygen saturation data for each day

    * `metrics`: a sibling list to `dates` that contains various metrics data for each day

    * `personal_record`: a sibling list to `dates` that contains personal record data for each day

    * `activities`: a sibling list to `dates` that contains activity data for each day

    * `device_settings`: a dictionary containing device settings data

    * `active_goals`: a sibling list to `dates` that contains active goals data for each day

    * `future_goals`: a sibling list to `dates` that contains future goals data for each day

    * `past_goals`: a sibling list to `dates` that contains past goals data for each day

    * `weigh_ins`: a sibling list to `dates` that contains weigh-ins data for each day

    * `weigh_ins_daily`: a sibling list to `dates` that contains daily weigh-ins data for each day

    * `hill_score`: a dictionary containing hill score data for the specified date range

    * `endurance_score`: a dictionary containing endurance score data for the specified date range

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
                "user_summary",
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
                "respiration",
                "spo2",
                "max_metrics",
                "personal_record",
                "earned_badges",
                "adhoc_challenges",
                "available_badges",
                "available_badge_challenges",
                "badge_challenges",
                "activities",
                "device_settings",
                "active_goals",
                "future_goals",
                "past_goals",
                "hrv",
                "weigh_ins",
                "weigh_ins_daily",
                "hill_score",
                "endurance_score",
                "dates",
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

        date_str_to_obj = lambda x: datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["synthetic_start_date"])

        start_idx = (date_str_to_obj(params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

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
        self.stats = synth_data["stats"]
        self.user_summary = synth_data["user_summary"]
        self.body_composition = synth_data["body_composition"]
        self.hr = synth_data["hr"]
        self.training_readiness = synth_data["training_readiness"]
        self.blood_pressure = synth_data["blood_pressure"]
        self.floors = synth_data["floors"]
        self.training_status = synth_data["training_status"]
        self.rhr = synth_data["rhr"]
        self.hydration = synth_data["hydration"]
        self.sleep = synth_data["sleep"]
        self.earned_badges = synth_data["earned_badges"]
        self.stress = synth_data["stress"]
        self.respiration = synth_data["respiration"]
        self.spo2 = synth_data["spo2"]
        self.max_metrics = synth_data["max_metrics"]
        self.personal_record = synth_data["personal_record"]
        self.activities = synth_data["activities"]
        self.device_settings = synth_data["device_settings"]
        self.active_goals = synth_data["active_goals"]
        self.future_goals = synth_data["future_goals"]
        self.past_goals = synth_data["past_goals"]
        self.weigh_ins = synth_data["weigh_ins"]
        self.weigh_ins_daily = synth_data["weigh_ins_daily"]
        self.hill_score = synth_data["hill_score"]
        self.endurance_score = synth_data["endurance_score"]

    def _authenticate(self, auth_creds):
        # check if we have cached credentials
        if self.init_params["use_cache"] and os.path.exists(CRED_CACHE_PATH):
            self.api = pickle.load(open(CRED_CACHE_PATH, "rb"))
        else:
            self.api = garth.Client(domain="garmin.com")
            self.api.login(auth_creds["email"], auth_creds["password"])
            pickle.dump(self.api, open(CRED_CACHE_PATH, "wb"))
