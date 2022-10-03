"""
device.py
====================================
The core module of my example project
"""

__all__ = ["BaseDevice"]


class BaseDevice:
    def __init__(self):
        self._authorized = False
        self.data_types_methods_map = dict()

    def _get_data(self, data_type, params=None):
        raise NotImplementedError

    def get_data(self, data_type, params=None):
        if not data_type in self.data_types_methods_map:
            raise ValueError(
                f"data_type must be in {list(self.data_types_methods_map.keys())}"
            )

        return self._get_data(data_type, params=params)

    def gen_synthetic_data(self):
        raise NotImplementedError

    def authorize(self, auth_creds):
        # authorize this device against API

        raise NotImplementedError

    @property
    def authorized(self):
        return self._authorized
