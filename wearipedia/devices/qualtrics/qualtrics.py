from QualtricsAPI.Setup import Credentials

from ...utils import seed_everything
from ..device import BaseDevice
from .qualtrics_fetch import fetch_real_data
from .qualtrics_gen import create_syn_data


class Qualtrics(BaseDevice):
    """
    This device allows you to work with data from the Qualtrics survey platform.
    Available datatypes for this device are:

    * `responses`: a DataFrame of survey responses

    :param seed: random seed for synthetic data generation, defaults to 0
    :type seed: int, optional
    :param survey: ID of the survey, required
    :type survey: str
    """

    name = "qualtrics/qualtrics"

    def __init__(self, seed=0, survey="your_survey_id_here"):
        params = {
            "seed": seed,
            "survey": str(survey),
        }

        self._initialize_device_params(
            [
                "responses",
            ],
            params,
            {
                "seed": 0,
                "synthetic_survey": "your_survey_id_here",
            },
        )

    def _default_params(self):
        return {
            "survey": self.init_params["synthetic_survey"],
        }

    def _get_real(self, data_type, params):
        return fetch_real_data(params["survey"])

    def _filter_synthetic(self, data, data_type, params):
        return data

    def _gen_synthetic(self):
        seed_everything(self.init_params["seed"])
        self.responses = create_syn_data(
            self.init_params["synthetic_survey"],
        )

    def _authenticate(self, auth_creds):
        token = auth_creds["token"]
        data_center = auth_creds["data_center"]
        Credentials().qualtrics_api_credentials(token=token, data_center=data_center)
