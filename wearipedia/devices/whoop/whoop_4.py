from ...devices.device import BaseDevice
from ...utils import seed_everything
from .whoop_gen import *
from .whoop_user import *

class_name = "Whoop4"


class Whoop4(BaseDevice):
    def __init__(self):
        self._authenticated = False
        self.data_types_methods_map = {
            "cycles": "get_cycles_df",
            "health_metrics": "get_health_metrics_df",
            "sleeps": "get_sleeps_df",
            "hr": "get_heart_rate_df",
        }
        self.valid_data_types = list(self.data_types_methods_map.keys())

    def _default_params(self):
        start_str = "2000-01-01"
        end_str = "2100-02-03"
        # get cycle data from start to end
        params = {
            "start": start_str + "T00:00:00.000Z",
            "end": end_str + "T00:00:00.000Z",
        }

        return params

    def _get_data(self, data_type, params):
        api_func = getattr(self.user, self.data_types_methods_map[data_type])
        return api_func(params=params)

    def _gen_synthetic(self, seed=0):
        # generate random data according to seed
        if not hasattr(self, "user"):
            self.user = WhoopUser("", "")

        seed_everything(seed)

        self.cycles = create_fake_cycles_df()

        self.health_metrics = create_fake_metrics_df()

        self.sleeps = create_fake_sleeps_df()

        self.hr = create_fake_hr_df(self.sleeps)

    def authenticate(self, auth_creds):
        # authenticate this device against API

        self.auth_creds = auth_creds

        self.user = WhoopUser(auth_creds["email"], auth_creds["password"])

        self._authenticated = True
