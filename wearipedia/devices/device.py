"""
device.py
====================================
The core module of my example project
"""

__all__ = ["BaseDevice"]


class BaseDevice:
    def __init__(self):
        self._authenticated = False
        self.valid_data_types = []

    def _get_data(self, data_type, params=None):
        raise NotImplementedError

    def get_data(self, data_type, params=None):
        if not data_type in self.valid_data_types:
            raise ValueError(f"data_type must be in {list(self.valid_data_types)}")

        return self._get_data(data_type, params=params)

    def gen_synthetic(self):
        raise NotImplementedError

    def authenticate(self, auth_creds):
        # authenticate this device against API

        raise NotImplementedError

    @property
    def authenticated(self):
        return self._authenticated
