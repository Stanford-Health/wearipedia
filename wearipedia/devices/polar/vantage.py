from datetime import datetime
import requests
import re

from ..device import BaseDevice
from ...utils import seed_everything

from .vantage_fetch import *
from .vantage_synthetic import *

class_name = "PolarVantage"


class PolarVantage(BaseDevice):

    """This device allows you to work with data from the `Polar Vantage <https://www.polar.com/us-en/vantage/v2>`_ device.
    Available datatypes for this device are:

    * `sleep`: a list that contains sleep data for each day

    * `training_history`: a list that contains training history data for each day

    * `training_by_id`: a list that contains training data for a given training session

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
        start_date="2022-03-01",
        end_date="2022-06-17"
    ):
        params = {
            "seed": seed,
            "start_date": str(start_date),
            "end_date": str(end_date)
        }

        self._initialize_device_params(
            ['sleep', 'training_history', 'training_by_id'],
            params,
            {
                "seed": 0,
                "start_date": "2022-03-01",
                "end_date": "2022-06-17"
            },
        )

    def _default_params(self):
        return {
            "training_id": None,
            "start_date": self.init_params["start_date"],
            "end_date": self.init_params["end_date"]
        }

    def _get_real(self, data_type, params):
        if 'training_id' in params:
            return fetch_real_data(
                self.session, self.USERID, self.email, self.password, params[
                    "start_date"], params["end_date"], data_type, params['training_id']
            )
        else:
            return fetch_real_data(
                self.session, self.USERID, self.email, self.password, params[
                    "start_date"], params["end_date"], data_type, ''
            )

    def _filter_synthetic(self, data, data_type, params):
        # Here we just return the data we've already generated,
        # but index into it based on the params. Specifically, we
        # want to return the data between the start and end dates.

        # convert the dates to datetime objects
        def date_str_to_obj(x): return datetime.strptime(x, "%Y-%m-%d")

        # get the indices by subtracting against the start of the synthetic data
        synthetic_start = date_str_to_obj(
            self.init_params["start_date"])

        start_idx = (date_str_to_obj(
            params["start_date"]) - synthetic_start).days
        end_idx = (date_str_to_obj(params["end_date"]) - synthetic_start).days

        return data[start_idx:end_idx]

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        self.training_history, self.sleep, self.training_by_id = create_syn_data(
            self.init_params["start_date"],
            self.init_params["end_date"],
        )

    def _authenticate(self, auth_creds):

        # check if all the credentials are provided
        if 'email' not in auth_creds:
            print('No email provided')
            return
        if 'password' not in auth_creds:
            print('No password provided')
            return

        # set the credentials
        self.email = auth_creds['email']
        self.password = auth_creds['password']

        # setting the initial user id to 0
        self.USERID = 0

        # login details are sent as payload
        payload = {
            "email": auth_creds['email'],
            "password": auth_creds['password'],
        }

        # login to polar flow
        with requests.Session() as session:
            post = session.post('https://flow.polar.com/login', data=payload)

            # using regular expressions, we can search for the userId in the session response
            result = re.search('AppGlobal.init((.*))', post.text)

            # if the userId is not found, the login failed
            if result == None:
                print('Login failed, please check your credentials')
                return

            res = str(result.group(1)).split('"')
            self.USERID = int(res[1])

            print('Login successful, user id is: ' + str(self.USERID))
            self.session = session
