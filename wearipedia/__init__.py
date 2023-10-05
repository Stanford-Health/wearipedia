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
        "apple/healthkit",
        "cronometer/cronometer",
        "whoop/whoop_4",
        "withings/scanwatch",
        "withings/bodyplus",
        "withings/sleepmat",
        "dreem/headband_2",
        "dexcom/pro_cgm",
        "garmin/fenix_7s",
        "google/googlefit",
        "polar/h10",
        "polar/verity_sense",
        "nutrisense/cgm",
        "polar/vantage",
        "strava/strava",
        "underarmour/myfitnesspal",
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


def get_os(key):
    if key in os.environ.keys():
        return os.environ[key]
    else:
        return None


# this is only for testing purposes
_DEVICE_TO_AUTH_DICT = {
    "garmin/fenix_7s": {
        "email": get_os("GARMIN_FENIX_7S_EMAIL"),
        "password": get_os("GARMIN_FENIX_7S_PASSWORD"),
    },
    "whoop/whoop_4": {
        "email": get_os("WHOOP_4_EMAIL"),
        "password": get_os("WHOOP_4_PASSWORD"),
    },
    "withings/bodyplus": {
        "refresh_token_env_var": "WITHINGS_REFRESH_TOKEN",
        "client_id": get_os("WITHINGS_CLIENT_ID"),
        "client_secret": get_os("WITHINGS_CLIENT_SECRET"),
        "refresh_token": get_os("WITHINGS_REFRESH_TOKEN"),
    },
    "withings/scanwatch": {
        "refresh_token_env_var": "WITHINGS_REFRESH_TOKEN",
        "client_id": get_os("WITHINGS_CLIENT_ID"),
        "client_secret": get_os("WITHINGS_CLIENT_SECRET"),
        "refresh_token": get_os("WITHINGS_REFRESH_TOKEN"),
    },
    "dexcom/pro_cgm": {
        "refresh_token_env_var": "DEXCOM_REFRESH_TOKEN",
        "client_id": get_os("DEXCOM_CLIENT_ID"),
        "client_secret": get_os("DEXCOM_CLIENT_SECRET"),
        "refresh_token": get_os("DEXCOM_REFRESH_TOKEN"),
    },
    "polar/verity_sense": {
        "email": get_os("POLAR_EMAIL"),
        "password": get_os("POLAR_PASSWORD"),
    },
    "polar/vantage": {
        "email": get_os("POLAR_EMAIL"),
        "password": get_os("POLAR_PASSWORD"),
    },
}

_REFRESH_TOKEN_STORE = "/tmp/refresh_tokens.json"


def _read_token_from_json(device_name, is_access_token=False):
    try:
        d = json.load(open(_REFRESH_TOKEN_STORE))
        refresh_token_env_var = _DEVICE_TO_AUTH_DICT[device_name][
            "refresh_token_env_var"
        ]

        if is_access_token:
            refresh_token_env_var = refresh_token_env_var.replace("REFRESH", "ACCESS")

        return d[refresh_token_env_var]
    except:
        return None


def _dump_token_to_json(device_name, new_refresh_token, is_access_token=False):
    # pre-emptively fill it with nothing
    if not Path(_REFRESH_TOKEN_STORE).exists():
        json.dump({}, open(_REFRESH_TOKEN_STORE, "w"))
    else:
        with open(_REFRESH_TOKEN_STORE) as f:
            if len(f.read()) == 0:
                json.dump({}, open(_REFRESH_TOKEN_STORE, "w"))

    # we're running in GitHub Actions, so we can
    # update the refresh token
    refresh_token_env_var = _DEVICE_TO_AUTH_DICT[device_name]["refresh_token_env_var"]
    if is_access_token:
        refresh_token_env_var = refresh_token_env_var.replace("REFRESH", "ACCESS")

    # since we can't propagate environment variables up in Github
    # Actions, we just keep around a file /tmp/refresh_tokens.json
    refresh_tokens = json.load(open(_REFRESH_TOKEN_STORE))
    refresh_tokens[refresh_token_env_var] = new_refresh_token
    json.dump(refresh_tokens, open(_REFRESH_TOKEN_STORE, "w"))


def _authenticate_device(device_name, device):
    # not only authenticates device, but also manages
    # the temporary cache JSON file for running CI on
    # github actions

    auth_dict = _DEVICE_TO_AUTH_DICT[device_name]

    # replace with refresh token json on disk if possible
    disk_refresh_token = _read_token_from_json(device_name)
    if disk_refresh_token is not None:
        auth_dict["refresh_token"] = disk_refresh_token

    disk_access_token = _read_token_from_json(device_name, is_access_token=True)
    if disk_access_token is not None:
        auth_dict["access_token"] = disk_access_token

    print("AUTHENTICATING DEVICE", device_name)
    print("AUTHENTICATION DICTIONARY IS", auth_dict.keys())

    device.authenticate(auth_dict)

    if "refresh_token" in dir(device):
        _dump_token_to_json(device_name, device.refresh_token)

    if "access_token" in dir(device):
        _dump_token_to_json(device_name, device.access_token, is_access_token=True)
