from datetime import datetime, time, timedelta

from ...utils import bin_search, seed_everything
from ..device import BaseDevice
from .oura_ring3_authenticate import *
from .oura_ring3_fetch import *
from .oura_ring3_gen import *

class_name = "Oura_Ring_3"


class Oura_Ring_3(BaseDevice):
    """This device allows you to work with data from the `Oura Ring 3  <(https://ouraring.com/)>`_ device.
    Available datatypes for this device are:

    * `sleep`: sleep data
    * `daily_activity`: daily activity data
    * `activity`: activity data
    * `ideal_bedtime`: ideal bedtime data
    * `readiness`: readiness data
    * `heart_rate`: heart_rate

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    """

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
                "sleep",
                "daily_activity",
                "activity",
                "ideal_bedtime",
                "readiness",
                "heart_rate",
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
            "start_date": "2022-04-24",
            "end_date": "2022-04-28",
        }

        return params

    def _filter_synthetic(self, data, data_type, params):

        date_str_to_obj = lambda x: datetime.strptime(x, "%Y-%m-%d")
        datetime_str_to_obj = lambda x: datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["synthetic_start_date"])

        start_idx = (datetime_str_to_obj(params["start_date"]) - synthetic_start).days
        end_idx = (datetime_str_to_obj(params["end_date"]) - synthetic_start).days

        return data

    def _get_real(self, data_type, params):

        data = fetch_real_data(
            data_type,
            self.user,
            start_date=self.init_params["start_date"],
            end_date=self.init_params["end_date"],
        )
        return data

    def _gen_synthetic(self):

        syn_data = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )
        self.sleep = syn_data["sleep"]
        self.daily_activity = syn_data["daily_activity"]
        self.activity = syn_data["activity"]
        self.ideal_bedtime = syn_data["ideal_bedtime"]
        self.readiness = syn_data["readiness"]
        self.heart_rate = syn_data["heart_rate"]

    def _authenticate(self, email, password):

        login(email, password)
        self.user = oura_token()
