import random

import numpy as np

__all__ = ["is_notebook", "seed_everything"]


def is_notebook() -> bool:
    """Check if we are running in a notebook.

    :return: `True` if we are running in a notebook, `False` otherwise.
    :rtype: bool
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def seed_everything(seed):
    """Set random seed for reproducibility.

    :param seed: the seed to use
    :type seed: int
    """
    np.random.seed(seed)
    random.seed(seed)


def bin_search_aux(data, start, end, target):
    """Binary search for a target in a sorted array.
    This is a helper function for `bin_search`.

    :param data: the sorted array
    :type data: list
    :param start: the start index
    :type start: int
    :param end: the end index
    :type end: int
    :param target: the target to search for
    :type target: int
    :return: the index of the target
    :rtype: int
    """
    if start >= end:
        return start

    mid = (start + end) // 2
    if data[mid] == target:
        return mid
    elif data[mid] < target:
        return bin_search_aux(data, mid + 1, end, target)
    else:
        return bin_search_aux(data, start, mid - 1, target)


def bin_search(data, target):
    """Binary search for a target in a sorted array.

    :param data: the sorted array
    :type data: list
    :param target: the target to search for
    :type target: int
    :return: the index of the target
    :rtype: int
    """

    return bin_search_aux(data, 0, len(data) - 1, target)
