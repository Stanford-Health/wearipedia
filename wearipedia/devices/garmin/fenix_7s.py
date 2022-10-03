from ...devices.device import BaseDevice
from ...utils import seed_everything
from .fenix_gen import *

class_name = "Fenix7S"


class Fenix7S(BaseDevice):
    def __init__(self):
        self._authorized = False

    def get_data(self, data_type=None, params=None):
        if params is None:
            params = dict()

        if data_type is None:
            raise ValueError(
                f"data_type must be in {list(self.data_types_methods_map.keys())}"
            )

        return getattr(self.user, self.data_types_methods_map[data_type])(params=params)

    def gen_synthetic_data(self, seed=0):
        # generate random data according to seed
        seed_everything(seed)

    def authorize(self, auth_creds):
        # authorize this device against API

        self.auth_creds = auth_creds

        self._authorized = True

    def authorized(self):
        return self._authorized
