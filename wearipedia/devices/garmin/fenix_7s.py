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

    * `brpms`: a sibling list to `dates` that contains breath rate data for each day

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
            ["stats",
             "user_summary",
             "body_composition",
             "steps",
             "hr",
             "training_readiness",
             "body_battery",
             "blood_pressure",
             "daily_steps",
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
             "avail_badge_challenges",
             "activities",
             "devices",
             "device_settings",
             "active_goals",
             "future_goals",
             "past_goals",
             "alarms",
             "hrv",
             "weigh_ins",
             "weigh_ins_daily",
             "hill_score",
             "endurance_score",
             "dates"],
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

        return data[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        (self.dates,
         self.osteps,
         self.ohrs,
         self.obrpms,
         self.hrv,
         self.steps,
         self.stats,
         self.user_summary,
         self.body_composition,
         self.hr,
         self.training_readiness,
         self.blood_pressure,
         self.floors,
         self.training_status,
         self.rhr,
         self.hydration,
         self.sleep,
         self.earned_badges,
         self.stress,
         self.respiration,
         self.spo2,
         self.max_metrics,
         self.personal_record,
         self.activities,
         self.device_settings,
         self.active_goals,
         self.future_goals,
         self.past_goals,
         self.weigh_ins,
         self.weigh_ins_daily,
         self.hill_score,
         self.endurance_score
         ) = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

    def _authenticate(self, auth_creds):
        # check if we have cached credentials
        if self.init_params["use_cache"] and os.path.exists(CRED_CACHE_PATH):
            self.api = pickle.load(open(CRED_CACHE_PATH, "rb"))
        else:
            self.api = garth.Client(domain="garmin.com")
            self.api.login(auth_creds["email"], auth_creds["password"])
            pickle.dump(self.api, open(CRED_CACHE_PATH, "wb"))
