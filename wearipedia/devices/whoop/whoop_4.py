from ...devices.device import BaseDevice
from ...utils import seed_everything
from .whoop_gen import *
from .whoop_user import *

class_name = "Whoop4"


class Whoop4(BaseDevice):
    def __init__(self):
        self._authorized = False
        self.data_types_methods_map = {
            "cycles": "get_cycles_df",
            "health_metrics": "get_health_metrics_df",
        }

    def _get_data(self, data_type, params=None):
        if params is None:
            start_str = "2000-01-01"
            end_str = "2100-02-03"
            # get cycle data from start to end
            params = {
                "start": start_str + "T00:00:00.000Z",
                "end": end_str + "T00:00:00.000Z",
            }

        return getattr(self.user, self.data_types_methods_map[data_type])(params=params)

    def gen_synthetic_data(self, seed=0):
        # generate random data according to seed
        if not hasattr(self, "user"):
            self.user = WhoopUser("", "")

        seed_everything(seed)

        self.user.cycles_df = create_fake_cycles_df()

        self.user.metrics_df = create_fake_metrics_df()

        self.user.sleeps_df = create_fake_sleeps_df()

        self.user.hr_df = create_fake_hr_df(self.user.sleeps_df)

    def authorize(self, auth_creds):
        # authorize this device against API

        self.auth_creds = auth_creds

        self.user = WhoopUser(auth_creds["email"], auth_creds["password"])

        self._authorized = True
