import importlib
import importlib.util
import os
from importlib import import_module
from importlib import metadata as importlib_metadata

TEST_PATH = os.path.dirname(__file__)


def get_device_checker(device_name, data_type):
    """Get a device checker for the given device and data type.

    :param device_name: the name of the device to get, e.g. "garmin/fenix_7s"
    :type device_name: str
    :param data_type: the type of data to get, e.g. "heart_rates"
    :type data_type: str
    :return: a device checker
    :rtype: Callable
    """

    company, model = device_name.split("/")

    module_path = f"{TEST_PATH}/{device_name}_checker.py"

    spec = importlib.util.spec_from_file_location(
        name=f"devices.{company}.{model}_checker",
        location=module_path,
    )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return getattr(module, f"check_{data_type}")


def check(device_name, data_type, data):
    """Check that the data obtained from a device is valid.

    :param device_name: the name of the device
    :type device_name: str
    :param data_type: the type of data
    :type data_type: str
    :param data: the actual data obtained
    :type data: Any
    """

    if data is None:
        raise ValueError("Data is None")

    # an eventual TODO is to make sure that all data that
    # is returned is a Pandas DataFrame, but for now we
    # just check that the data is not None and let the
    # more specific checks be done in the device-specific
    # checkers

    # do the same thing as in the root __init__.py file
    # and fetch the checker for the given device, and check
    # it with the given data type and data
    checker = get_device_checker(device_name, data_type)

    checker(data)
