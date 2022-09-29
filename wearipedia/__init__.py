# type: ignore[attr-defined]
"""wearables in development"""

import sys
from importlib import metadata as importlib_metadata

from .devices import *


def get_device(device_name):
    company, model = device_name.split("/")

    module = importlib.import_module("devices/" + device_name + ".py")

    device_map = getattr(module, "device_map")

    return getattr(module, device_map[model])


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
