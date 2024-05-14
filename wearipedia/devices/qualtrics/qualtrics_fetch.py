from QualtricsAPI.Survey import Responses
from QualtricsAPI.Setup import Credentials

def fetch_real_data(survey):
    responses = Responses().get_survey_responses(survey=survey, useLabels=True)
    return responses
