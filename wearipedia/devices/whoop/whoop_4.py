from ...devices.device import BaseDevice
from .whoop_utils import *

class_name = "Whoop4"


class Whoop4(BaseDevice):
    def __init__(self):
        self._authorized = False

    def get_data(self, params=None):
        if params is None:
            startStr = "2000-01-01"  # @param {type:"string"}
            endStr = "2100-02-03"  # @param {type:"string"}
            # get cycle data from start to end
            params = {
                "start": startStr + "T00:00:00.000Z",
                "end": endStr + "T00:00:00.000Z",
            }

        # show information for sleep cycles of interest
        cycles_df = user.get_cycles_df(params=params)

        # gives summary statistics for various metrics
        metrics_df = user.get_health_metrics_df(params=params)

    def gen_synthetic_data(self, seed=0):
        # generate random data according to seed
        if not hasattr(self, "user"):
            self.user = WhoopUser("", "")

        self.user.cycles_df = self.user.create_fake_cycles_df()

        self.user.metrics_df = self.user.create_fake_metrics_df()

        self.user.sleeps_df = self.user.create_fake_sleeps_df()

        self.user.sleeps_df = self.user.create_fake_sleeps_df()

        self.user.hr_df = self.user.create_fake_hr_df()

    def authorize(self, auth_creds):
        # authorize this device against API

        self.auth_creds = auth_creds

        self.user = WhoopUser(auth_creds["email"], auth_creds["password"])

        self._authorized = True

    def authorized(self):
        # authorized
        return self._authorized
