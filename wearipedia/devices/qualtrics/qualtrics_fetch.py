import QualtricsAPI

from QualtricsAPI.Setup import Credentials
from QualtricsAPI.Survey import Responses

def fetch_real_data(token, data_center, survey):
    """
    Fetches real data from the Qualtrics API.
    """
    Credentials().qualtrics_api_credentials(token=token,data_center=data_center)
    table = Responses().get_survey_responses(survey=survey, useLabels=True)
    return table
