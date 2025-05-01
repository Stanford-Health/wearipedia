import collections
from datetime import datetime, time, timedelta

from ...utils import bin_search, seed_everything
from ..device import BaseDevice
from .coros_pace_2_fetch import fetch_real_data
from .coros_pace_2_gen import create_syn_data


class CorosPace2(BaseDevice):
    """This device allows you to work with data from the `Fitbit charge  <(https://www.fitbit.com/global/au/products/trackers/charge4)>`_ device.
    Available datatypes for this device are:

    * `steps`: steps data
    * `exercise_time`: exercise time data
    * `heart_rate`: heart rate data
    * `sports`: sports data
    * `sleep`: sleep data
    * `active_energy`: active energy data

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    """

    name = "coros/coros_pace_2"

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
                "steps",
                "exercise_time",
                "heart_rate",
                "sports",
                "sleep",
                "active_energy",
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
            start_date=self.init_params["start_date"],
            end_date=self.init_params["end_date"],
        )
        return data

    def _gen_synthetic(self):

        syn_data = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )
        self.steps = syn_data["steps"]
        self.exercise_time = syn_data["exercise_time"]
        self.heart_rate = syn_data["heart_rate"]
        self.sports = syn_data["sports"]
        self.sleep = syn_data["sleep"]
        self.active_energy = syn_data["active_energy"]

    def _authenticate(self):
        # authenticate this device against API
        print(
            "Get the access token here: https://colab.research.google.com/drive/1cnVktqcPXPtGS6JcdHVVCqIC3nngfxhm?usp=sharing"
        )
        token = input("Enter your access token: ")
        self.user = token
