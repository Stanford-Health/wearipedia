from datetime import datetime, time, timedelta

import numpy as np

from ...utils import bin_search, seed_everything
from ..device import BaseDevice
from .fitbit_authenticate import fitbit_application
from .fitbit_sense_fetch import fetch_real_data
from .fitbit_sense_gen import create_syn_data


class GooglePixelWatch(BaseDevice):
    """This device allows you to work with data from the `Google Pixel Watch`_ device.
    Available datatypes for this device are:

    * `intraday_breath_rate`: collected per stage of sleep
    * `intraday_active_zone_minute`: collected per minute
    * `intraday_heart_rate`: collected per second
    * `intraday_hrv`: rmssd, lf and hf and collected during sleep
    * `intraday_spo2`: in percentage collected during sleep
    * `sleep`: sleep data
    * `steps`: steps data
    * `minutesVeryActive`: number of minutes with high activity
    * `minutesLightlyActive`: number of minutes with light activity
    * `minutesFairlyActive`: number of minutes with fair activity
    * `distance`: in miles
    * `minutesSedentary`: number of minutes with no activity

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param synthetic_start_date: start date for synthetic data generation, defaults to "2024-04-01"
    :type synthetic_start_date: str, optional
    :param synthetic_end_date: end date for synthetic data generation, defaults to "2024-05-13"
    :type synthetic_end_date: str, optional
    """

    name = "fitbit/google_pixel_watch"

    def __init__(
        self,
        seed=0,
        synthetic_start_date="2024-01-01",
        synthetic_end_date="2024-01-31",
    ):

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
        }

        self._initialize_device_params(
            [
                "intraday_breath_rate",
                "intraday_active_zone_minute",
                "intraday_heart_rate",
                "intraday_hrv",
                "intraday_spo2",
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
                "synthetic_start_date": "2024-01-01",
                "synthetic_end_date": "2024-01-31",
            },
        )

    def _default_params(self):
        return {
            "start_date": "2022-04-24",
            "end_date": "2022-04-28",
        }

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

        return data[num_days_start : -num_days_end - 1]

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

        self.intraday_breath_rate = syn_data["intraday_breath_rate"]
        self.intraday_active_zone_minute = syn_data["intraday_active_zone_minute"]
        self.intraday_heart_rate = syn_data["intraday_heart_rate"]
        self.intraday_hrv = syn_data["intraday_hrv"]
        self.intraday_spo2 = syn_data["intraday_spo2"]
        self.sleep = syn_data["sleep"]
        self.steps = syn_data["steps"]
        self.minutesVeryActive = syn_data["minutesVeryActive"]
        self.minutesFairlyActive = syn_data["minutesFairlyActive"]
        self.minutesLightlyActive = syn_data["minutesLightlyActive"]
        self.distance = syn_data["distance"]
        self.minutesSedentary = syn_data["minutesSedentary"]

    def _authenticate(self, auth_creds):
        client_id = auth_creds["client_id"]
        client_secret = auth_creds["client_secret"]
        self.user = fitbit_token(client_id, client_secret)
