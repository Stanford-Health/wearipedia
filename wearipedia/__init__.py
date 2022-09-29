# type: ignore[attr-defined]
"""wearables in development"""

import importlib
import sys
from importlib import import_module
from importlib import metadata as importlib_metadata

from .constants import *
from .devices import *


def get_device(device_name):
    company, model = device_name.split("/")

    module_path = f"{PACKAGE_PATH}/devices/{device_name}.py"

    import importlib.util

    spec = importlib.util.spec_from_file_location(
        name=f"wearipedia.devices.{company}.{model}",  # note that ".test" is not a valid module name
        location=module_path,
    )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    class_name = getattr(module, "class_name")

    return getattr(module, class_name)


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
