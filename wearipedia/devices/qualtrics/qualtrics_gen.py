import os

import pandas as pd


def create_syn_data(synthetic_survey):
    """
    Creates synthetic survey data based on a sample survey CSV file.

    This function reads a sample patient intake CSV file located in the same directory as the script
    and returns its contents as a Pandas DataFrame. The function assumes that this sample survey
    CSV file is named "patient_intake.csv".

    :param synthetic_survey: Dummy variable that is not used in this function.
    :type synthetic_survey: str
    :return: A DataFrame containing the synthetic survey data from the sample CSV file.
    :rtype: pd.DataFrame
    """
    script_dir = os.path.dirname(__file__)
    survey_file = os.path.join(script_dir, "patient_intake.csv")
    df = pd.read_csv(survey_file)
    return df
