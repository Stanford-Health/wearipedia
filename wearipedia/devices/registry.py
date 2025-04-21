REGISTRY = {}


def register_device(cls):
    """
    Decorator to register a device class in the registry.

    Args:
        device_name (str): The device name in format "company/model"
    """

    REGISTRY[cls.name] = cls


def get_device_class(device_name):
    """
    Get the device class from the registry.

    Args:
        device_name (str): The device name in format "company/model"

    Returns:
        type: The device class

    Raises:
        KeyError: If the device is not registered
    """
    return REGISTRY[device_name]
