from datetime import datetime, timedelta

import requests
import urllib3

from ...devices.device import BaseDevice
from ...utils import seed_everything
from .cgm_fetch import fetch_real_data
from .cgm_gen import gen_data


class NutrisenseCGM(BaseDevice):
    """This device allows you to work with data from the `Nutrisense CGM <https://www.nutrisense.io/>`_ device.
    Available datatypes for this device are:

    * `continuous`: contains the continuous glucose data

    * `summary`: contains summary statistics of the continuous glucose data

    * `scores`: contains glucose scores

    * `statistics`: contains further statistics about the continuous glucose data

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param start_date: start date for synthetic data generation, defaults to "2022-03-01"
    :type start_date: str, optional
    :param end_date: end date for synthetic data generation, defaults to "2022-06-17"
    :type end_date: str, optional
    """

    name = "nutrisense/cgm"

    def __init__(
        self,
        seed=0,
        synthetic_start_date="2022-03-01",
        synthetic_end_date="2022-06-17",
        use_cache=False,
    ):

        params = {
            "seed": seed,
            "synthetic_start_date": synthetic_start_date,
            "synthetic_end_date": synthetic_end_date,
            "use_cache": use_cache,
        }

        self._initialize_device_params(
            ["continuous", "summary", "scores", "statistics"],
            params,
            {
                "seed": 0,
                "synthetic_start_date": "2022-03-01",
                "synthetic_end_date": "2022-06-17",
                "use_cache": False,
            },
        )

    def _default_params(self):
        return {
            "start_date": self.init_params["synthetic_start_date"],
            "end_date": self.init_params["synthetic_end_date"],
        }

    def _get_real(self, data_type, params):
        return fetch_real_data(
            params["start_date"], params["end_date"], data_type, self.headers
        )

    def _filter_synthetic(self, data, data_type, params):
        # choose only the dates between start and end
        result = []
        str_to_date = lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S-08:00")
        start = datetime.strptime(params["start_date"], "%Y-%m-%d")
        end = datetime.strptime(params["end_date"], "%Y-%m-%d")
        end = end + timedelta(days=1)
        if data_type == "continuous":
            for e in data:
                d = str_to_date(e["x"])
                if d > start and d < end:
                    result.append(e)
            return result
        else:
            return data

    def _gen_synthetic(self):
        # generate random data according to seed
        seed_everything(self.init_params["seed"])

        # and based on start and end dates
        self.scores, self.continuous, self.summary, self.statistics = gen_data(
            self.init_params["synthetic_start_date"],
            self.init_params["synthetic_end_date"],
            self.init_params["seed"],
        )

    def _authenticate(self, auth_creds):

        urllib3.disable_warnings()

        self.headers = {
            "Host": "api-production.nutrisense.io",
            "Accept": "*/*",
            "Build_number": "1074",
            "Client_version": "2.5.0",
            "App_scheme": "nutrisense-production",
            "X-Datadog-Origin": "rum",
            "X-Datadog-Sampling-Priority": "0",
            "Content-Type": "application/json",
            # 'Content-Length': '943',
            # 'Accept-Encoding': 'gzip, deflate',
            "User-Agent": "okhttp/4.9.3",
        }

        json_data = {
            "operationName": "signinUser",
            "variables": {
                "email": auth_creds["email"],
                "password": auth_creds["password"],
            },
            "query": "fragment CoreUserFields on User {\n  id\n  email\n  fullName\n  firstName\n  lastName\n  phoneNumber\n  avatar\n  active\n  biteId\n  biteToken\n  timeZone\n  intercomDigest\n  signUpState\n  role\n  onboardingStatus\n  paymentFailedProviderErrorMessage\n  __typename\n}\n\nmutation signinUser($email: String!, $password: String!, $impersonate: String) {\n  signinUser(\n    email: {email: $email, password: $password, impersonate: $impersonate}\n  ) {\n    token\n    success\n    user {\n      ...CoreUserFields\n      address {\n        name\n        street\n        street2\n        city\n        state\n        zipCode\n        __typename\n      }\n      paymentMethod {\n        stripeId\n        cardType\n        last4\n        expirationDate\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
        }

        response = requests.post(
            "https://api-production.nutrisense.io/graphql",
            headers=self.headers,
            json=json_data,
            verify=False,
        )
        res = response.json()
        bearer = f"Bearer {res['data']['signinUser']['token']}"

        # save the token to the header for future requests
        self.headers["Authorization"] = bearer
