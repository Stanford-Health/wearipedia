import pytest
import pandas as pd
import wearipedia

@pytest.mark.parametrize("real", [True, False])
def test_qualtrics(real):

    synthetic_survey = "your_survey_id_here"

    device = wearipedia.get_device(
        "qualtrics/qualtrics",
        survey=synthetic_survey,
    )

    if real:
        wearipedia._authenticate_device("qualtrics", device)

    data = device.get_data('responses')

    # Check that the data is a pandas DataFrame
    assert isinstance(data, pd.DataFrame), f"Data is not a pandas DataFrame"
