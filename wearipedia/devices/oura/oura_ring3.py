from datetime import datetime, time, timedelta

from ...utils import bin_search, seed_everything
from ..device import BaseDevice
from .oura_ring3_authenticate import oura_token
from .oura_ring3_fetch import fetch_real_data
from .oura_ring3_gen import create_syn_data


class OuraRing3(BaseDevice):
    """This device allows you to work with data from the `Oura Ring 3  <(https://ouraring.com/)>`_ device.
    Available datatypes for this device are:

    * `heart_rate`: heart_rate
    * `personal_info`: personal information
    * `session`: data on user engagement with sessions in the Oura app
    * `enhanced_tag`: user tags on data
    * `workout`: workout sessions
    * `daily_activity`: daily activity data
    * `daily_sleep`: daily sleep data including scores per day
    * `sleep`: all logged sleep activities
    * `readiness`: readiness data
    * `ideal_sleep_time`: ideal bedtime data

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    """

    name = "oura/oura_ring3"

    def __init__(
        self,
        seed=0,
        synthetic_start_date="2022-03-01",
        synthetic_end_date="2022-06-17",
    ):

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
        }

        self._initialize_device_params(
            [
                "heart_rate",
                "personal_info",
                "session",
                "enhanced_tag",
                "workout",
                "daily_activity",
                "daily_sleep",
                "sleep",
                "readiness",
                "ideal_sleep_time",
            ],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
            },
        )

    def _default_params(self):
        params = {
            "seed": 0,
            "start_date": "2022-04-24",
            "end_date": "2022-04-28",
        }

        return params

    def _filter_synthetic(self, data, data_type, params):

        date_format = "%Y-%m-%d"
        date1 = datetime.strptime(self.init_params["synthetic_start_date"], date_format)
        date2 = datetime.strptime(params["start_date"], date_format)

        date3 = datetime.strptime(self.init_params["synthetic_end_date"], date_format)
        date4 = datetime.strptime(params["end_date"], date_format)

        delta1 = date2 - date1
        delta2 = date3 - date4

        num_days_start = delta1.days
        num_days_end = delta2.days

        return data[num_days_start : -num_days_end + 1]

    def _get_real(self, data_type, params):

        data = fetch_real_data(
            data_type,
            self.user,
            start_date=params["start_date"],
            end_date=params["end_date"],
        )
        return data

    def _gen_synthetic(self):

        syn_data = create_syn_data(
            self.init_params["seed"],
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )
        self.personal_info = []
        self.heart_rate = syn_data["heart_rate"]
        self.session = syn_data["session"]
        self.enhanced_tag = syn_data["enhanced_tag"]
        self.workout = syn_data["workout"]
        self.daily_activity = syn_data["daily_activity"]
        self.daily_sleep = syn_data["daily_sleep"]
        self.sleep = syn_data["sleep"]
        self.readiness = syn_data["readiness"]
        self.ideal_sleep_time = syn_data["ideal_sleep_time"]

    def _authenticate(self, token=""):
        if token == "":
            self.user = oura_token()
        else:
            self.user = token
