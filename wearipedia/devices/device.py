"""
device.py
====================================
The core module of my example project
"""

__all__ = ["BaseDevice"]


class BaseDevice:
    def __init__(self):
        """Initializes the device."""

        self._authenticated = False
        self.valid_data_types = []

    def _get_data(self, data_type, params):
        """Gets data from the API according to the data_type and params.

        :param data_type: a string describing the type of data to get.
        :type data_type: str
        :param params: dictionary containing parameters for API extraction
        :type params: Dict
        :raises NotImplementedError: for now, raises NotImplementedError, but should be implemented
            by child classes.
        """
        raise NotImplementedError

    def _default_params(self):
        """Returns default parameters for API extraction.

        :raises NotImplementedError: for now, raises NotImplementedError, but should be implemented
            by child classes.
        """
        raise NotImplementedError

    def get_data(self, data_type, params=None):
        """Gets data from the API according to the data_type and params.

        Follows the procedure of first checking if the data_type is valid, then setting
        default parameters if none are provided, then checking if the device is authenticated,
        and finally calling the _get_data method if the device is authenticated (otherwise
        fetching synthetic data).

        IF YOU ARE IMPLEMENTING A NEW DEVICE, YOU SHOULD NOT NEED TO OVERRIDE THIS METHOD.

        :param data_type: a string describing the type of data to get.
        :type data_type: str
        :param params: dictionary containing parameters for API extraction, defaults to None
        :type params: Dict, optional
        :raises ValueError: if data_type is not in valid_data_types
        :raises Exception: if the user has not called gen_synthetic() or authenticate() yet.
        :return: returns the data from the API (or synthetic data if gen_synthetic() has been called)
        :rtype: List or DataFrame or Series or Dict
        """
        if not data_type in self.valid_data_types:
            raise ValueError(f"data_type must be in {list(self.valid_data_types)}")

        if params is None:
            params = self._default_params()

        if self.authenticated:
            return self._get_data(data_type, params)
        else:
            if hasattr(self, data_type):
                return getattr(self, data_type)
            else:
                self._gen_synthetic()
                return getattr(self, data_type)

    def _gen_synthetic(self):
        """Generates synthetic data for the device. If you are implementing a new device,
        this method must save data from each datatype separately as member attributes such that
        `get_data()` will be able to find it with the `get_attr()` call.

        :raises NotImplementedError: for now, raises NotImplementedError, but should be implemented
            by child classes.
        """
        raise NotImplementedError

    def authenticate(self, auth_creds):
        """Authenticates the device against the API. For now, should be user-interactive, if
        the authentication protocol requires a step in which you get a code by visiting their
        website.

        :param auth_creds: a dictionary containing the authentication credentials.
        :type auth_creds: Dict
        :raises NotImplementedError: for now, raises NotImplementedError, but should be implemented
            by child classes.
        """

        raise NotImplementedError

    @property
    def authenticated(self):
        return self._authenticated
