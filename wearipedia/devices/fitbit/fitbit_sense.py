from datetime import datetime, time, timedelta

from ...utils import bin_search, seed_everything
from ..device import BaseDevice
from .fitbit_authenticate import *
from .fitbit_sense_fetch import *
from .fitbit_sense_gen import *

class_name = "Fitbit_sense"


class Fitbit_sense(BaseDevice):
    """This device allows you to work with data from the `Fitbit Sense <(https://www.fitbit.com/global/us/products/smartwatches/sense)>`_ device.
    Available datatypes for this device are:

    * `sleep`: sleep data
    * `steps`: steps data
    * `minutesVeryActive`: number of minutes with high activity
    * `minutesLightlyActive`: number of minutes with light activity
    * `minutesFairlyActive`: number of minutes with fair activity
    * `distance`: in miles
    * `minutesSedentary`: number of minutes with no activity
    * `heart_rate_day`: heart rate data
    * `hrv`: heart rate variability data
    * `distance_day`: distance moved per day detailed by each minute

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
                "steps",
                "minutesVeryActive",
                "minutesLightlyActive",
                "minutesFairlyActive",
                "distance",
                "minutesSedentary",
                "heart_rate_day",
                "hrv",
                "distance_day",
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
            "start_date": "2022-06-30",
            "end_date": "2023-01-01",
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

        self.sleep = syn_data["sleep"]
        self.steps = syn_data["steps"]
        self.minutesVeryActive = syn_data["minutesVeryActive"]
        self.minutesFairlyActive = syn_data["minutesFairlyActive"]
        self.minutesLightlyActive = syn_data["minutesLightlyActive"]
        self.distance = syn_data["distance"]
        self.minutesSedentary = syn_data["minutesSedentary"]
        self.heart_rate_day = syn_data["heart_rate_day"]
        self.hrv = syn_data["hrv"]
        self.distance_day = syn_data["distance_day"]

    def _authenticate(self, client_id="", client_secret=""):
        # authenticate this device against API
        fitbit_application()
        if client_id == "":
            client_id = input("enter client id: ")
            client_secret = input("enter client secret: ")
        self.user = fitbit_token(client_id, client_secret)
