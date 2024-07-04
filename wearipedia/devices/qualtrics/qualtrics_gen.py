import os
import pandas as pd

def create_syn_data():
    """
    Creates synthetic survey data based on a sample survey CSV file.

    This function reads a sample survey CSV file located in the same directory as the script
    and returns its contents as a Pandas DataFrame. The function assumes that the sample survey
    CSV file is named "sample_survey.csv".

    :return: A DataFrame containing the synthetic survey data from the sample CSV file.
    :rtype: pd.DataFrame
    """
    script_dir = os.path.dirname(__file__)
    survey_file = os.path.join(script_dir, "sample_survey.csv")
    df = pd.read_csv(survey_file)
    return df
