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
