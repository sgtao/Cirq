# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility methods for checking properties of matrices."""

import numpy as np

from cirq.linalg.tolerance import Tolerance


def is_diagonal(
        matrix: np.matrix,
        tolerance: Tolerance = Tolerance.DEFAULT
) -> bool:
    """Determines if a matrix is a approximately diagonal.

    A matrix is diagonal if i!=j implies m[i,j]==0.

    Args:
        matrix: The matrix to check.
        tolerance: The per-matrix-entry tolerance on equality.

    Returns:
        Whether the matrix is diagonal within the given tolerance.
    """
    diag = np.matrix(matrix)
    for i in range(min(diag.shape)):
        diag[i, i] = 0
    return tolerance.all_near_zero(diag)


def is_hermitian(
        matrix: np.matrix,
        tolerance: Tolerance = Tolerance.DEFAULT
) -> bool:
    """Determines if a matrix is approximately Hermitian.

    A matrix is Hermitian if it's square and equal to its adjoint.

    Args:
        matrix: The matrix to check.
        tolerance: The per-matrix-entry tolerance on equality.

    Returns:
        Whether the matrix is Hermitian within the given tolerance.
    """
    return (matrix.shape[0] == matrix.shape[1] and
            tolerance.all_close(matrix, matrix.H))


def is_orthogonal(
        matrix: np.matrix,
        tolerance: Tolerance = Tolerance.DEFAULT
) -> bool:
    """Determines if a matrix is approximately orthogonal.

    A matrix is orthogonal if it's square and real and its transpose is its
    inverse.

    Args:
        matrix: The matrix to check.
        tolerance: The per-matrix-entry tolerance on equality.

    Returns:
        Whether the matrix is orthogonal within the given tolerance.
    """
    return (matrix.shape[0] == matrix.shape[1] and
            np.all(np.imag(matrix) == 0) and
            tolerance.all_close(matrix.dot(matrix.T), np.eye(matrix.shape[0])))


def is_special_orthogonal(
        matrix: np.matrix,
        tolerance: Tolerance = Tolerance.DEFAULT
) -> bool:
    """Determines if a matrix is approximately special orthogonal.

    A matrix is special orthogonal if it is square and real and its transpose
    is its inverse and its determinant is one.

    Args:
        matrix: The matrix to check.
        tolerance: The per-matrix-entry tolerance on equality.

    Returns:
        Whether the matrix is special orthogonal within the given tolerance.
    """
    return (is_orthogonal(matrix, tolerance) and
            (matrix.shape[0] == 0 or
             tolerance.all_close(np.linalg.det(matrix), 1)))


def is_unitary(
        matrix: np.matrix,
        tolerance: Tolerance = Tolerance.DEFAULT
) -> bool:
    """Determines if a matrix is approximately unitary.

    A matrix is unitary if it's square and its adjoint is its inverse.

    Args:
        matrix: The matrix to check.
        tolerance: The per-matrix-entry tolerance on equality.

    Returns:
        Whether the matrix is unitary within the given tolerance.
    """
    return (matrix.shape[0] == matrix.shape[1] and
            tolerance.all_close(matrix.dot(matrix.H), np.eye(matrix.shape[0])))


def is_special_unitary(
        matrix: np.matrix,
        tolerance: Tolerance = Tolerance.DEFAULT
) -> bool:
    """Determines if a matrix is approximately unitary with unit determinant.

    A matrix is special-unitary if it is square and its adjoint is its inverse
    and its determinant is one.

    Args:
        matrix: The matrix to check.
        tolerance: The per-matrix-entry tolerance on equality.

    Returns:
        Whether the matrix is unitary with unit determinant within the given
        tolerance.
    """
    return (is_unitary(matrix, tolerance) and
            (matrix.shape[0] == 0 or
             tolerance.all_close(np.linalg.det(matrix), 1)))


def commutes(
        m1: np.matrix,
        m2: np.matrix,
        tolerance: Tolerance = Tolerance.DEFAULT
) -> bool:
    """Determines if two matrices approximately commute.

    Two matrices A and B commute if they are square and have the same size and
    AB = BA.

    Args:
        m1: One of the matrices.
        m2: The other matrix.
        tolerance: The per-matrix-entry tolerance on equality.

    Returns:
        Whether the two matrices have compatible sizes and a commutator equal
        to zero within tolerance.
  """
    return (m1.shape[0] == m1.shape[1] and
            m1.shape == m2.shape and
            tolerance.all_close(m1.dot(m2), m2.dot(m1)))
