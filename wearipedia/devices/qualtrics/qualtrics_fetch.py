from QualtricsAPI.Setup import Credentials
from QualtricsAPI.Survey import Responses


def fetch_real_data(survey):
    """
    Fetches real survey data from Qualtrics.
    This function uses QualtricsAPI to fetch survey responses based on the given survey ID.
    The responses are retrieved with labels (actual user responses) instead of numeric codes.

    :param survey: the ID of the survey from which to fetch responses
    :type start_date: str

    :return: the survey responses fetched from the API
    :rtype: Pandas DataFrame
    """
    responses = Responses().get_survey_responses(survey=survey, useLabels=True)
    return responses
