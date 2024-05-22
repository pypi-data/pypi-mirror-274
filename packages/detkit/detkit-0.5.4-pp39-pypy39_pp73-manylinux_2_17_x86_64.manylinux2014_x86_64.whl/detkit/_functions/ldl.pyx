# SPDX-FileCopyrightText: Copyright 2022, Siavash Ameli <sameli@berkeley.edu>
# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileType: SOURCE
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the license found in the LICENSE.txt file in the root directory
# of this source tree.


# =======
# Imports
# =======

import numpy
# from scipy.linalg.cython_lapack cimport ssytrf, dsytrf
from libc.stdlib cimport malloc, free

__all__ = ['ldl']

# TEST
def ldl():
    pass


# ===
# ldl
# ===

# cpdef ldl(A, lower=True, overwrite_a=False):
#     """
#     LDL decomposition.
#     """
#
#     n, m = A.shape
#     if n != m:
#         raise ValueError('Matrix should be square.')
#
#     if overwrite_a:
#         ldu = A
#     else:
#         ldu = numpy.copy(A)
#
#     piv = numpy.empty(n, dtype=numpy.int32)
#     cdef int[:] piv_mv = piv
#     cdef int* piv_p = &piv_mv[0]
#
#     cdef float[:, ::1] A_fp32_c_mv
#     cdef float[::1, :] A_fp32_f_mv
#     cdef double[:, ::1] A_fp64_c_mv
#     cdef double[::1, :] A_fp64_f_mv
#
#     cdef float* A_fp32_p
#     cdef double* A_fp64_p
#     cdef int info
#
#
#     # dispatch based on floating point precision and order
#     if (A.dtype == numpy.float32):
#         # Treat C and F contiguous the same as it is assumed array is symmetric
#         if A.flags['C_CONTIGUOUS']:
#             A_fp32_c_mv = ldu
#             A_fp32_p = &A_fp32_c_mv[0, 0]
#         elif A.flags['F_CONTIGUOUS']:
#             A_fp32_f_mv = ldu
#             A_fp32_p = &A_fp32_f_mv[0, 0]
#         else:
#             raise ValueError('Array should be either "C" or "F" contiguous.')
#
#         info = _ldl_fp32(A_fp32_p, piv_p, n, bool(lower))
#
#     elif (A.dtype == numpy.float32):
#         # Treat C and F contiguous the same as it is assumed array is symmetric
#         if A.flags['C_CONTIGUOUS']:
#             A_fp64_c_mv = ldu
#             A_fp64_p = &A_fp64_c_mv[0, 0]
#         elif A.flags['F_CONTIGUOUS']:
#             A_fp64_f_mv = ldu
#             A_fp64_p = &A_fp64_f_mv[0, 0]
#         else:
#             raise ValueError('Array should be either "C" or "F" contiguous.')
#
#         info = _ldl_fp64(A_fp64_p, piv_p, n, bool(lower))
#
#     else:
#         raise ValueError('Array should be "fp32" or "fp64" precision.')
#
#     if info != 0:
#         raise ValueError('LDL decomposition failed with error code: %d' % info)
#
#     return ldu, piv
#
#
# # ========
# # ldl fp32
# # ========
#
# cdef int _ldl_fp32(
#         float* A,
#         int* piv,
#         int n,
#         bint lower) nogil:
#     """
#     Process float64 precision.
#     """
#
#     cdef char uplo
#
#     if lower:
#         uplo = b'l'
#     else:
#         uplo = b'u'
#
#     cdef int info
#     cdef int lda = n
#     cdef float* work = <float*> malloc(1 * sizeof(float))
#     cdef int lwork = -1  # query optimal workspace size
#
#     # Query optimal workspace
#     with nogil:
#         ssytrf(&uplo, &n, A, &lda, piv, work, &lwork, &info)
#
#     # Get actual size of work that is needed
#     lwork = int(work[0])
#
#     # Allocate work with actual size
#     free(work)
#     work = <float*> malloc(lwork * sizeof(float))
#
#     # Perform actual decomposition
#     with nogil:
#         ssytrf(&uplo, &n, A, &lda, piv, work, &lwork, &info)
#
#     free(work)
#
#     return info
#
#
# # ========
# # ldl fp64
# # ========
#
# cdef int _ldl_fp64(
#         double* A,
#         int* piv,
#         int n,
#         bint lower) nogil:
#     """
#     Process float64 precision.
#     """
#
#     cdef char uplo
#
#     if lower:
#         uplo = b'l'
#     else:
#         uplo = b'u'
#
#     cdef int info
#     cdef int lda = n
#     cdef double* work = <double*> malloc(1 * sizeof(double))
#     cdef int lwork = -1  # query optimal workspace size
#
#     # Query optimal workspace
#     with nogil:
#         dsytrf(&uplo, &n, A, &lda, piv, work, &lwork, &info)
#
#     # Get actual size of work that is needed
#     lwork = int(work[0])
#
#     # Allocate work with actual size
#     free(work)
#     work = <double*> malloc(lwork * sizeof(double))
#
#     # Perform actual decomposition
#     with nogil:
#         dsytrf(&uplo, &n, A, &lda, piv, work, &lwork, &info)
#
#     free(work)
#
#     return info
