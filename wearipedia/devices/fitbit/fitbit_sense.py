from ...utils import bin_search, seed_everything
from datetime import datetime, time, timedelta
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

        self._initialize_device_params(
            list(self.data_types_methods_map.keys()),
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

    def _filter_synthetic(self, data, data_type, params):

        date_str_to_obj = lambda x: datetime.strptime(x, "%Y-%m-%d")
        datetime_str_to_obj = lambda x: datetime.strptime(
            x, "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(self.init_params["synthetic_start_date"])

        start_idx = (datetime_str_to_obj(params["start"]) - synthetic_start).days
        end_idx = (datetime_str_to_obj(params["end"]) - synthetic_start).days

        cycles = {
            "total_count": end_idx - start_idx,
            "offset": end_idx - start_idx,
            "records": data["records"][start_idx:end_idx],
        }

        return cycles

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

        dictionary = create_syn_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
        )

        return dictionary

    def _authenticate(self):
        # authenticate this device against API
        fitbit_application()
        client_id = input("enter client id: ")
        client_secret = input("enter client secret: ")
        self.user = fitbit_token(client_id, client_secret)