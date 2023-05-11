from ...utils import bin_search, seed_everything
from ..device import BaseDevice
from .fitbit_authenticate import *
from .fitbit_sense_fetch import *
from .fitbit_sense_gen import *

class_name = "Fitbit_charge_4"


class Fitbit_charge_4(BaseDevice):
    """This device allows you to work with data from the `Fitbit charge  <(https://www.fitbit.com/global/au/products/trackers/charge4)>`_ device.
    Available datatypes for this device are:

    * `sleep`: sleep data
    * `steps`: steps data
    * `minutesVeryActive`: number of minutes with high activity
    * `minutesLightlyActive`: number of minutes with light activity
    * `minutesFairlyActive`: number of minutes with fair activity
    * `distance`: in miles
    * `minutesSedentary`: number of minutes with no activity

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type synthetic_end_date: str, optional
    :param single_day: end date for real data data fetching, defaults to "2022-09-19"
    :type single_day: str, optional
    """

    def __init__(
        self,
        seed=0,
        synthetic_start_date="2022-03-01",
        synthetic_end_date="2022-06-17",
        single_day="2022-09-19",
    ):

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
            "single_day": single_day,
        }

        # self.data_types_methods_map = {
        #     "sleep": "get_sleep_json",
        #     "steps": "get_steps_json",
        #     "minutesVeryActive": "get_minutesVeryActive_json",
        #     "minutesLightlyActive": "get_minutesLightlyActive_json",
        #     "minutesFairlyActive": "get_minutesFairlyActive_json",
        #     "distance": "get_distance_json",
        #     "minutesSedentary": "get_minutesSedentary_json",
        # }

        self._initialize_device_params(
            [
                "sleep",
                "steps",
                "minutesVeryActive",
                "minutesLightlyActive",
                "minutesFairlyActive",
                "distance",
                "minutesSedentary",
            ],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
                "single_day": "2022-09-19",
            },
        )

    def _default_params(self):
        params = {
            "start": "2022-04-24",
            "end": "2022-04-28",
            "single_date": "2022-09-19",
        }

        return params

    def _get_real(self, data_type, params):

        data = fetch_real_data(
            data_type,
            self.user,
            start_date=self.init_params["synthetic_start_date"],
            end_date=self.init_params["synthetic_end_date"],
            single_date=self.init_params["single_day"],
        )
        return data

    def _gen_synthetic(self):

        syn_data = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )
        self.sleep = syn_data["sleep"]
        self.steps = syn_data["steps"]
        self.minutesVeryActive = syn_data["minutesVeryActive"]
        self.minutesFairlyActive = syn_data["minutesFairlyActive"]
        self.minutesLightlyActive = syn_data["minutesLightlyActive"]
        self.distance = syn_data["distance"]
        self.minutesSedentary = syn_data["minutesSedentary"]

    def _authenticate(self):
        # authenticate this device against API
        fitbit_application()
        client_id = input("enter client id: ")
        client_secret = input("enter client secret: ")
        self.user = fitbit_token(client_id, client_secret)
