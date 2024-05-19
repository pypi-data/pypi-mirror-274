import numpy as np
from typing import Union, List

def is_positive_integer(num: int) -> bool:
    """
    Check if a number is an integer greater than 0.

    Args:
    num (int): Input number.

    Returns:
    bool: True if the number is an integer greater than 0, False otherwise.
    """
    return isinstance(num, int) and num > 0

def is_2d_numpy_array(input_array: np.ndarray) -> bool:
    """
    Check if a number is a 2D NumPy array of real numbers.

    Args:
    input_array (numpy.ndarray): Input array.

    Returns:
    bool: True if the input is a 2D NumPy array of real numbers, False otherwise.
    """
    return isinstance(input_array, np.ndarray) and input_array.ndim == 2 and np.issubdtype(input_array.dtype, np.number)

def is_list_or_1d_numpy_array(input_array: Union[List[float], np.ndarray]) -> bool:
    """
    Check if a number is a list or 1D NumPy array of real numbers.

    Args:
    input_array (list or numpy.ndarray): Input array.

    Returns:
    bool: True if the input is a list or 1D NumPy array of real numbers, False otherwise.
    """
    if isinstance(input_array, list):
        return all(isinstance(elem, (int, float)) for elem in input_array)
    elif isinstance(input_array, np.ndarray):
        return input_array.ndim == 1 and np.issubdtype(input_array.dtype, np.number)
    else:
        return False