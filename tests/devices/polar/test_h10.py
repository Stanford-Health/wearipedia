from test_polar import *


# the polar h10 uses the same data as the verity sense, so we can just run the same tests
@pytest.mark.parametrize("real", [True, False])
def test_h10(real):
    test_polar(real)
