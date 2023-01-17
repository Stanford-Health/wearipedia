# type: ignore[attr-defined]
"""wearables in development"""

import importlib
import importlib.util
from importlib import import_module

try:
    from importlib import metadata as importlib_metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as importlib_metadata

from .constants import *
from .devices import *


def get_device(device_name, **kwargs):
    """Get a device object by name. This is the main entry point for the library.

    Keep in mind that the keyword arguments are device-specific!

    :param device_name: the name of the device to get, e.g. "garmin/fenix_7s"
    :type device_name: str
    :return: a device object
    :rtype: BaseDevice

    **Example**

    .. code-block:: python

        import wearipedia

        # Get a device object
        device = wearipedia.get_device("whoop/whoop_4")
        ...
    """
    company, model = device_name.split("/")

    module_path = f"{PACKAGE_PATH}/devices/{device_name}.py"

    spec = importlib.util.spec_from_file_location(
        name=f"wearipedia.devices.{company}.{model}",
        location=module_path,
    )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    class_name = getattr(module, "class_name")

    return getattr(module, class_name)(**kwargs)


def get_all_device_names():
    """Get a list of all device names.

    :return: a list of device names
    :rtype: List
    """

    return [
        "whoop/whoop_4",
        "withings/scanwatch",
        "withings/bodyplus",
        "withings/sleepmat",
        "dreem/headband_2",
        "dexcom/pro_cgm",
        "garmin/fenix_7s",
        "polar/verity_sense",
        "polar/vantage",
        "strava/strava",
        "cronometer/cronometer",
        "underarmour/myfitnesspal",
        "google/googlefit",
    ]


def get_version() -> str:
    """Get the version of the library.

    :return: the version of the library
    :rtype: str
    """
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
