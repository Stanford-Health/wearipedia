"""
device.py
====================================
The core module of my example project
"""

__all__ = ["BaseDevice"]


class BaseDevice:
    def __init__(self):
        self._authorized = False

    def get_data(self):
        raise NotImplementedError

    def gen_synthetic_data(self):
        raise NotImplementedError

    def authorize(self, auth_creds):
        # authorize this device against API

        raise NotImplementedError

    @property
    def authorized(self):
        return self._authorized
