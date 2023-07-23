# test_evo.py

from datetime import datetime

import pytest

import wearipedia


@pytest.mark.parametrize("real", [True, False])
def test_evo(real):
    start_synthetic = datetime(2023, 6, 5)
    end_synthetic = datetime(2023, 6, 20)

    device = wearipedia.get_device(
        "biostrap/evo",
        start_date=datetime.strftime(start_synthetic, "%Y-%m-%d"),
        end_date=datetime.strftime(end_synthetic, "%Y-%m-%d"),
    )
    if real:
        wearipedia._authenticate_device("evo", device)

    steps = device.get_data("steps")
    dates = list(steps.keys())  # extracting dates from steps data
    bpm = device.get_data("bpm")
    brpm = device.get_data("brpm")
    spo2 = device.get_data("spo2")

    assert len(dates) == len(steps) == (end_synthetic - start_synthetic).days + 1, (
        f"Expected dates and steps data to be the same length and to match the number of days between"
        f" {start_synthetic} and {end_synthetic}, but got {len(dates)}, {len(steps)}"
    )

    # first make sure that the dates are correct
    for date_1, date_2 in zip(dates[:-1], dates[1:]):
        assert (
            date_2 - date_1
        ).days == 1, f"Dates are not consecutive: {date_1}, {date_2}"

    assert dates[0] == start_synthetic, f"First date is not correct: {dates[0]}"

    # Now make sure that the steps are correct.
    for step in steps.values():
        assert isinstance(step, int), f"Step data is not correct: {step}"

    # Now make sure that the bpm, brpm and spo2 are correct.
    for hr in bpm.values():
        assert isinstance(hr, float), f"BPM data is not correct: {hr}"

    for br in brpm.values():
        assert isinstance(br, float), f"BRPM data is not correct: {br}"

    for s in spo2.values():
        assert isinstance(s, float), f"SPO2 data is not correct: {s}"
