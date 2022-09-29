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

    if True:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            name=f"wearipedia.devices.{company}.{model}",  # note that ".test" is not a valid module name
            location=module_path,
        )

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        class_name = getattr(module, "class_name")
    ########################
    if False:
        import importlib.util
        import sys
        from pathlib import Path

        if Path(module_path).parent not in sys.path:
            sys.path.append(Path(module_path).parent)

        if Path(module_path).parent.parent not in sys.path:
            sys.path.append(Path(module_path).parent.parent)

        spec = importlib.util.spec_from_file_location(device_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[device_name] = module

        spec.loader.exec_module(module)
    #    foo.MyClass()

    if False:
        from .devices.whoop import whoop_4

        print(whoop_4)

        print(dir(whoop_4))

        class_name = getattr(whoop_4, "class_name")

        print(whoop_4.Whoop4())

    #####################
    if False:
        import importlib.machinery

        loader = importlib.machinery.SourceFileLoader(
            "wearipedia.devices.whoop.whoop_4", module_path
        )
        mod = loader.load_module()

    return getattr(module, class_name)


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
