## Data Transformation Library

### Description

The Data Transformation Library is a Python package designed to provide a set of functions for common data transformation tasks, such as transposing matrices, performing convolutions. This library aims to simplify data preprocessing and manipulation for machine learning and data analysis applications. There are three functions in the library:

- `transpose2d`: Switches the axes of a 2D tensor.
- `window1d`: Generates windows from a 1D time series array.
- `convolution2d`: Computes the cross-correlation of a 2D matrix with a kernel.

Library can be found: https://pypi.org/project/data-transformation-library-ingri/

#### Features

##### Transpose 2D Matrix

- **Signature**: `transpose2d(input_matrix: list[list[float]]) -> list`
- **Input**: A list of lists of real numbers representing a 2D matrix.
- **Output**: A transposed 2D matrix.
- **Implementation**: Implemented using only Python and its standard library.

##### Time Series Windowing

- **Signature**: `window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]`
- **Input**: A list or 1D Numpy array of real numbers, along with parameters for window size (length of the window), shift(step size between different windows), and stride (step size within each window).
- **Output**: A list of lists or 1D Numpy arrays of real numbers.
- **Implementation**: Implemented using Python, its standard library, and Numpy.

##### Cross-Correlation

- **Signature**: `convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray`
- **Input**: 2D Numpy arrays representing an input matrix and a kernel, along with a stride parameter.
- **Output**: A 2D Numpy array of real numbers.
- **Implementation**: Implemented using Python, its standard library, and Numpy.


#### Structure

- `functions.py`: contains the main three functions (transpose2d, window1d, convolution2d).
- `validate.py`: contains functions to check if the inputs for the functions in functions.py are coorect.


#### Installation

You can install the library using pip:

```bash
pip install data-transformation-library
```

#### Usage

To use the functions you have to install library and import the functions.

Example usage:

```python
import numpy as np
from functions import transpose2d, window1d, convolution2d

# Transpose:
input_matrix = [[3, 7, 9], [1, 5, 8]]
print(transpose2d(input_matrix))
# Output
[[3, 1], [7, 5], [9, 8]]


# Time Series Windowing:
input_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(window1d(input_array, size=3, shift=2, stride=1))
# Output
[[1, 2, 3], [3, 4, 5], [5, 6, 7], [7, 8, 9]]


# Cross-Correlation:
input_matrix = np.array([[1, 2, 3],
                          [4, 5, 6],
                          [7, 8, 9]])
kernel = np.array([[1, 0, -1],
                   [1, 0, -1],
                   [1, 0, -1]])
print(convolution2d(input_matrix, kernel, stride=1))
# Output
[[-6.]]
```
