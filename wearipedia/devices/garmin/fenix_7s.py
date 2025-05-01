import os
import pickle
import tempfile
from datetime import datetime

from garminconnect import Garmin

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .fenix_fetch import fetch_real_data
from .fenix_gen import create_syn_data


def user_identifier():
    if "getuid" in dir(os):
        return os.getuid()

    if "getlogin" in dir(os):
        return os.getlogin()

    return "unknown"


CRED_CACHE_PATH = os.path.join(
    tempfile.gettempdir(), f"wearipedia_fenix_data_{user_identifier()}.pkl"
)


class Fenix7S(BaseDevice):
    """This device allows you to work with data from the `Garmin Fenix 7S <https://www.garmin.com/en-US/p/735542>`_ device.
    Available datatypes for this device are:

    * `dates`: a list of consecutive dates
    * `steps`: a sibling list to `dates` that contains step data for each day
    * `body_battery`: a sibling list to `dates` that contains body battery data for each day
    * `hr`: a sibling list to `dates` that contains heart rate data for each day
    * `blood_pressure`: a sibling list to `dates` that contains blood pressure data for each day
    * `floors`: a sibling list to `dates` that contains floors data for each day
    * `rhr`: a sibling list to `dates` that contains resting heart rate data for each day
    * `hydration`: a sibling list to `dates` that contains hydration data for each day
    * `sleep`: a sibling list to `dates` that contains sleep data for each day
    * `stress`: a sibling list to `dates` that contains stress data for each day
    * `respiration`: a sibling list to `dates` that contains respiration data for each day
    * `spo2`: a sibling list to `dates` that contains blood oxygen saturation data for each day
    * `hrv`: a sibling list to `dates` that contains heart rate variability data for each day


    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param use_cache: decide whether to cache the credentials, defaults to True
    :type use_cache: bool, optional
    """

    name = "garmin/fenix_7s"

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
                "steps",
                "body_battery",
                "hr",
                "blood_pressure",
                "floors",
                "rhr",
                "hydration",
                "sleep",
                "stress",
                "respiration",
                "spo2",
                "dates",
                "hrv",
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
        self.hr = synth_data["hr"]
        self.body_battery = synth_data["body_battery"]
        self.blood_pressure = synth_data["blood_pressure"]
        self.floors = synth_data["floors"]
        self.rhr = synth_data["rhr"]
        self.hydration = synth_data["hydration"]
        self.sleep = synth_data["sleep"]
        self.stress = synth_data["stress"]
        self.respiration = synth_data["respiration"]
        self.spo2 = synth_data["spo2"]

    def _authenticate(self, auth_creds):
        # check if we have cached credentials
        if self.init_params["use_cache"] and os.path.exists(CRED_CACHE_PATH):
            try:
                self.api = pickle.load(open(CRED_CACHE_PATH, "rb"))
                return
            except:
                print("Could not load cached credentials. Re-authenticating...")
                pass

        self.api = Garmin(auth_creds["email"], auth_creds["password"])
        self.api.login()

        if self.init_params["use_cache"]:
            with open(
                os.open(
                    CRED_CACHE_PATH,
                    flags=os.O_CREAT | os.O_TRUNC | os.O_WRONLY,
                    mode=0o600,
                ),
                mode="wb",
            ) as cred_cache_file:
                pickle.dump(self.api, cred_cache_file)
