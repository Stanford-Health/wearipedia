__all__ = ["BaseDevice"]


class BaseDevice:
    def __init__(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def gen_synthetic_data(self):
        raise NotImplementedError

    def authorize(self, auth_creds):
        # authorize this device against API

        raise NotImplementedError

    def authorized(self):
        raise NotImplementedError
