from test_polar import *


@pytest.mark.parametrize("real", [True, False])
def test_verity_sense(real):
    test_polar(real)
