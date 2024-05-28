from QualtricsAPI.Survey import Responses
from QualtricsAPI.Setup import Credentials

def fetch_real_data(survey):
    """
    Fetches real survey data from Qualtrics.

    This function uses QualtricsAPI to fetch survey responses based on the given survey ID.
    The responses are retrieved with labels (actual user responses) instead of numeric codes.

    Parameters:
        survey (str): The ID of the survey from which to fetch responses.

    Returns:
        dict: A dictionary containing the survey responses.
    """
    responses = Responses().get_survey_responses(survey=survey, useLabels=True)
    return responses
