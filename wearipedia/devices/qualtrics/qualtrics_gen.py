import os
import pandas as pd

def create_syn_data(survey):
    script_dir = os.path.dirname(__file__)
    survey_file = os.path.join(script_dir, "sample_survey.csv")
    df = pd.read_csv(survey_file)
    return df
