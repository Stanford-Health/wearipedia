from ...utils import seed_everything
from ..device import BaseDevice
from .qualtrics_fetch import *
from .qualtrics_gen import *

from QualtricsAPI.Setup import Credentials

class_name = "Qualtrics"

class Qualtrics(BaseDevice):
    """
    A class representing a Qualtrics survey device.

    This class is responsible for initializing the device with the necessary
    parameters, generating synthetic data, and fetching real data from Qualtrics 
    using the unofficial QualtricsAPI.
    """
    def __init__(self, seed=0, survey="your_survey_id_here"):
        """
        Initializes the Qualtrics device with the given seed and survey ID from Qualtrics.

        Parameters:
            seed (int, optional): The seed for random number generation. 
            survey (str, optional): The ID of the survey to be used. Retrieve this from Qualtrics.
        """
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
        """
        Returns the default parameters for the Qualtrics device.

        Returns:
            dict: A dictionary containing the default parameters.
        """
        return {
            "survey": self.init_params["synthetic_survey"],
        }

    def _get_real(self, data_type, params):
        """
        Fetches real data from Qualtrics based on the provided parameters.

        Parameters:
            data_type (str): The type of data to fetch.
            params (dict): A dictionary containing the parameters for fetching data.

        Returns:
            dict: A dictionary containing the fetched real data.
        """
        return fetch_real_data(
            params["survey"]
        )

    def _filter_synthetic(self, data, data_type, params):
        """
        Filters the synthetic data based on the provided parameters. This method is not implemented.

        Parameters:
            data (dict): The synthetic data to filter.
            data_type (str): The type of data being filtered.
            params (dict): A dictionary containing the parameters for filtering data.

        Returns:
            dict: The filtered synthetic data. This method returns the data as is.
        """
        return data

    def _gen_synthetic(self):
        """
        Generates synthetic survey data based on the initial parameters.

        This method sets the `responses` attribute with the generated synthetic data.
        """
        seed_everything(self.init_params["seed"])
        self.responses = create_syn_data(
            self.init_params["synthetic_survey"],
        )

    def _authenticate(self, auth_creds):
        """
        Authenticates the device using the provided credentials.

        Parameters:
            auth_creds (dict): A dictionary containing authentication credentials.
                - token (str): The API token for authentication.
                - data_center (str): The data center to connect to.
        """
        token = auth_creds["token"]
        data_center = auth_creds["data_center"]
        Credentials().qualtrics_api_credentials(token=token, data_center=data_center)
