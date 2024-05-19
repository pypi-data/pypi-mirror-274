from typing import List, Union
import numpy as np
from data_transformation_library_ingri.validate import is_list_or_1d_numpy_array, is_2d_numpy_array, is_positive_integer


def transpose2d(input_matrix: List[List[float]]) -> List[List[float]]:
    """
    Transpose a 2D matrix.

    Args:
    input_matrix (list[list[float]]): Input 2D matrix.

    Returns:
    list[list[float]]: Transposed 2D matrix.
    """
    # Convert input_matrix to a NumPy array
    np_array = np.array(input_matrix)

    # Check input_array
    if not is_2d_numpy_array(np_array):
        raise ValueError("Input matrix is not a 2D NumPy array of real numbers.")
    
    # Get the dimensions of the input matrix
    rows, cols = np_array.shape

    transposed_matrix = []

    # Iterate over columns of input_matrix
    for j in range(cols):
        transposed_row = []
        for i in range(rows):
            transposed_row.append(input_matrix[i][j])
        transposed_matrix.append(transposed_row)

    return transposed_matrix


def window1d(input_array: Union[List[float], np.ndarray], size: int, shift: int = 1, stride: int = 1) -> List[Union[List[float], np.ndarray]]:
    """
    Generate sliding windows over a 1D array.

    Args:
    input_array (Union[List[float], np.ndarray]): Input 1D array.
    size (int): Size of the window.
    shift (int): Shift between windows.
    stride (int): Stride within each window.

    Returns:
    List[Union[List[float], np.ndarray]]: List of windows.
    """
    # Check input_array
    if not is_list_or_1d_numpy_array(input_array):
        raise ValueError("Input array is not a list or 1D NumPy array of real numbers.")
    
    # Check size, shift, and stride
    if not is_positive_integer(size):
        raise ValueError("Size must be a positive integer.")
    if not is_positive_integer(shift):
        raise ValueError("Shift must be a positive integer.")
    if not is_positive_integer(stride):
        raise ValueError("Stride must be a positive integer.")
    
    windows = []
    for i in range(0, len(input_array) - size + 1, shift):
        window = input_array[i:i+size]
        if stride > 1:
            window = window[::stride]
        windows.append(window)
    return windows


def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    """
    Perform 2D cross-correlation.

    Args:
    input_matrix (np.ndarray): Input 2D matrix.
    kernel (np.ndarray): Kernel for cross-correlation.
    stride (int): Stride for convolution.

    Returns:
    np.ndarray: Result of cross-correlation.
    """
    # Check input_matrix and kernel
    if not is_2d_numpy_array(input_matrix):
        raise ValueError("Input matrix is not a 2D NumPy array of real numbers.")
    if not is_2d_numpy_array(kernel):
        raise ValueError("Kernel is not a 2D NumPy array of real numbers.")
    
    # Check stride
    if not is_positive_integer(stride):
        raise ValueError("Stride must be a positive integer.")
    
    # Get the dimensions of the input matrix and kernel
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape

    # Calculate the output dimensions
    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1
    
    # Initialize the output matrix
    output_matrix = np.zeros((output_height, output_width))

    # Perform cross-correlation
    for i in range(0, output_height):
        for j in range(0, output_width):
            patch = input_matrix[i*stride:i*stride+kernel_height, j*stride:j*stride+kernel_width]
            output_matrix[i, j] = np.sum(patch * kernel)

    return output_matrix