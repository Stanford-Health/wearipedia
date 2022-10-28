"""
device.py
====================================
The core module for the wearipedia library.
"""

__all__ = ["BaseDevice"]

import wearipedia


class BaseDevice:
    """This class is a base class for all devices. It should not be instantiated directly.
    Instead, you should instantiate a child class of this class, which should be specific to
    a particular device. For example, the Fenix7S class is a child class of this class, and
    is specific to the Garmin Fenix7S device.

    The child class should implement the following methods:
    * __init__
    * _get_real
    * _get_synthetic
    * _gen_synthetic
    * _default_params
    * authenticate
    """

    def __init__(self, params):
        """Initializes the device.

        :param params: a dictionary containing parameters for the device. These are specific
            to each device, and should usually consist of parameters for synthetic data
            generation (for example, the start and end dates, persona, or random seed).
        :type params: Dict
        """

        default_init_params = {
            "seed": 0,
            "synthetic_start_date": "2022-03-01",
            "synthetic_end_date": "2022-06-17",
        }

        self._initialize_device_params([], params, default_init_params)

    def _initialize_device_params(self, valid_data_types, params, default_init_params):
        """Initializes the device parameters. This is called by the __init__ method.
        This method will set some member attributes and override the default_init_params
        with the params provided by the user.

        :param valid_data_types: a list of valid data types for the device.
        :type valid_data_types: List
        :param params: a dictionary containing parameters for the device. These are specific
            to each device, and should usually consist of parameters for synthetic data
            generation (for example, the start and end dates, persona, or random seed).
        :type params: Dict
        :param default_init_params: a dictionary containing default parameters for the device.
        :type default_init_params: Dict
        """

        # the following lines of code must be initialized in any child class,
        # but self.valid_data_types should be set to a list of actual valid data types
        self._authenticated = False
        self.valid_data_types = valid_data_types
        self._synthetic_has_been_generated = False
        self.init_params = default_init_params

        if params is None:
            params = dict()

        for key in self.init_params.keys():
            if key in params:
                self.init_params[key] = params[key]

    def _get_real(self, data_type, params):
        """Gets real data from the API according to the data_type and params.

        :param data_type: a string describing the type of data to get.
        :type data_type: str
        :param params: dictionary containing parameters for API extraction
        :type params: Dict
        :raises NotImplementedError: for now, raises NotImplementedError, but should be implemented
            by child classes.
        """
        raise NotImplementedError

    def _get_synthetic(self, data_type, params):
        """Gets synthetic data from the device. Should function in the same way as _get_real(),
        except that it should return synthetic data instead of real data. While it can be random,
        it should return the same data every time it is called with the same params.

        :param data_type: a string describing the type of data to get.
        :type data_type: str
        :param params: dictionary containing parameters for API extraction
        :type params: Dict
        :raises NotImplementedError: for now, raises NotImplementedError, but should be implemented
            by child classes.
        """
        raise NotImplementedError

    def _gen_synthetic(self):
        """Generates synthetic data for the device. This is automatically called by get_data().

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
            return self._get_real(data_type, params)
        else:
            if self.synthetic_has_been_generated:
                return self._get_synthetic(data_type, params)
            else:
                self._gen_synthetic()
                self._synthetic_has_been_generated = True
                return self._get_synthetic(data_type, params)

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

    @property
    def synthetic_has_been_generated(self):
        return self._synthetic_has_been_generated
