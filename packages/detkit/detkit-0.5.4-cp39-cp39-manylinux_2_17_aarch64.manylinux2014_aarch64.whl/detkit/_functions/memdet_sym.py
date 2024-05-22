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

import os
import numpy
import scipy
import tempfile
from .memory import Memory
from .parallel_io import load, store
from multiprocessing import shared_memory
import inspect
from ._fill_triangle import fill_triangle
from .._openmp import get_avail_num_threads
import time
import shutil
import zarr
import dask
import dask.array as da
from dask.distributed import Client
from ..__version__ import __version__
from ._utilities import get_processor_name

__all__ = ['memdet_sym']


# ============
# get dir size
# ============

def _get_dir_size(path):
    """
    get the size of a director.
    """

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    return total_size


# ==================
# get scratch prefix
# ==================

def _get_scratch_prefix():
    """
    Prefix for filename of scratch space. The prefix is the combination of
    package name and function name.
    """

    # Get the name of caller function
    stack = inspect.stack()
    caller_frame = stack[1]
    caller_function_name = caller_frame.function

    # Get the name of package
    frame = inspect.currentframe()
    module_name = frame.f_globals['__name__']
    package_name = module_name.split('.')[0]

    # scratch space filename prefix
    prefix = '.' + package_name + '-' + caller_function_name + '-'

    return prefix


# =========
# get array
# =========

def _get_array(shared_mem, m, dtype, order):
    """
    Get numpy array from shared memory buffer.
    """

    if isinstance(shared_mem, shared_memory.SharedMemory):
        # This is shared memory. Return its buffer.
        return numpy.ndarray(shape=(m, m), dtype=dtype, order=order,
                             buffer=shared_mem.buf)

    else:
        # This is already numpy array. Return itself.
        return shared_mem


# ====================
# pivot to permutation
# ====================

def _pivot_to_permutation(piv):
    """
    Convert pivot of indices to permutation of indices.
    """

    perm = numpy.arange(len(piv))
    for i in range(len(piv)):
        perm[i], perm[piv[i]] = perm[piv[i]], perm[i]

    return perm


# ==================
# permutation parity
# ==================

def _permutation_parity(p_inv):
    """
    Compute the parity of a permutation represented by the pivot array `piv`.

    Parameters
    ----------

    piv (array_like): The pivot array returned by `scipy.linalg.lu_factor`.

    Returns
    -------
    int: The parity of the permutation (+1 or -1).
    """

    n = len(p_inv)
    visited = numpy.zeros(n, dtype=bool)
    parity = 1

    for i in range(n):
        if not visited[i]:
            j = i
            while not visited[j]:
                visited[j] = True
                j = p_inv[j]
                if j != i:
                    parity = -parity

    return parity


# =============
# permute array
# =============

def _permute_array(array, perm, m, dtype, order):
    """
    Permutes rows of 2D array.

    Note that this function overwrites the input array.
    """

    # Get buffer from shared memory
    array_ = _get_array(array, m, dtype, order)

    array_copy = numpy.copy(array_, order=order)

    for i in range(len(perm)):
        array_[i, :] = array_copy[perm[i], :]


# =========
# lu factor
# =========

def _lu_factor(A, m, dtype, order, overwrite):
    """
    Performs LU factorization of an input matrix.
    """

    # Get buffer from shared memory
    A_ = _get_array(A, m, dtype, order)

    lu, piv = scipy.linalg.lu_factor(A_, overwrite_a=overwrite,
                                     check_finite=False)

    return lu, piv


# ==========
# ldl factor
# ==========

def _ldl_factor(A, m, dtype, order, overwrite):
    """
    Performs LDL factorization of an input matrix.
    """

    # Get buffer from shared memory
    A_ = _get_array(A, m, dtype, order)

    lu, d, perm = scipy.linalg.ldl(A_, overwrite_a=overwrite, lower=True,
                                   check_finite=False)

    return lu, d, perm


# ==========
# compute ld
# ==========

def _compute_ld(d):
    """
    Computes logdet from diagonals.
    """

    # TODO

    # ld_ = 0
    #
    # for i in range(d.shape[0]):
    #     if d[i, i] != 0:
    #         ld_ += numpy.log(numpy.abs(d[i, i]))
    #     if
    #         ld_ = numpy.log


# ================
# solve triangular
# ================

def _solve_triangular(lu, B, m, dtype, order, trans, lower, unit_diagonal,
                      overwrite):
    """
    Solve triangular system of equations.
    """

    # Get buffer from shared memory
    B_ = _get_array(B, m, dtype, order)

    x = scipy.linalg.solve_triangular(lu, B_, trans=trans, lower=lower,
                                      unit_diagonal=unit_diagonal,
                                      check_finite=False,
                                      overwrite_b=overwrite)

    return x


# ================
# schur complement
# ================

def _schur_complement(L_t, U, S, m, dtype, order):
    """
    Computes in-place Schur complement without allocating any intermediate
    memory. This method is parallel.

    For this function to not allocate any new memory, all matrices, L, U,
    and S should be in Fortran ordering.
    """

    alpha = -1
    beta = 1
    trans_a = 1
    trans_b = 0
    overwrite_c = 1

    # Get buffer from shared memory
    S_ = _get_array(S, m, dtype, order)

    # Check all matrices have Fortran ordering
    if not L_t.flags['F_CONTIGUOUS']:
        raise TypeError('Matrix "L" should have column-ordering.')
    if not U.flags['F_CONTIGUOUS']:
        raise TypeError('Matrix "U" should have column-ordering.')
    if not S_.flags['F_CONTIGUOUS']:
        raise TypeError('Matrix "S" should have column-ordering.')

    if numpy.dtype(dtype) == numpy.float64:
        scipy.linalg.blas.dgemm(alpha, L_t, U, beta, S_, trans_a, trans_b,
                                overwrite_c)
    elif numpy.dtype(dtype) == numpy.float32:
        scipy.linalg.blas.sgemm(alpha, L_t, U, beta, S_, trans_a, trans_b,
                                overwrite_c)
    else:
        raise TypeError('dtype should be float64 or float32.')


# ======
# memdet
# ======

def memdet_sym(
        A,
        num_blocks=1,
        assume='gen',
        triangle=None,
        overwrite=False,
        mixed_precision='float64',
        parallel_io=None,
        io_chunk=5000,
        scratch_dir=None,
        return_info=False,
        verbose=False):
    """
    Compute log-determinant on contained memory.

    Parameters
    ----------

    A : numpy.ndarray or numpy.memmap or zarr
        Square non-singular matrix.

    num_blocks : int, default=1
        Number of blocks

    triangle : ``'l'``, ``'u'``, or None, default=None
        Indicates the  matrix symmetric, but only half triangle part of the
        matrix is given. ``'l'`` assumes the lower-triangle part of the
        matrix is given, and ``'u'`` assumes the upper-triangle part of the
        matrix is given. `None` indicates all the matrix is given.

    assume : str {``'gen'``, ``'sym'``, ``'spd'``}, default=``'gen'``
        Assumption on the matrix `A`. Matrix is assumed to be generic if
        ``'gen'``, symmetric if ``'sym'``, and symmetric positive-definite if
        ``'psd'``.

    parallel_io : str {'mp', 'dask'} or None, default=None
        Parallel load and store from memory to scratchpad.

    overwrite : boolean, default=True
        Overwrites intermediate computations. May increase performance and
        memory consumption.

    verbose : bool, default=False
        Prints verbose output during computation.

    Returns
    -------

    ld : float
        Log-determinant
    sign : int
        Sign of determinant

    Raises
    ------

    See also
    --------

    detkit.logdet
    detkit.loggdet
    detkit.logpdet

    Notes
    -----

    Examples
    --------

    .. code-block:: python
        :emphasize-lines: 9

        >>> # Open a memmmap matrix
        >>> import numpy
        >>> n = 10000
        >>> A = numpy.memmap('matrix.npy', shape=(n, n), mode='r',
        ...                  dtype=numpy.float32, order='C')

        >>> # Compute log-determinant
        >>> from detkit import  memdet
        >>> ld = memdet(A, mem=64)
    """

    n = A.shape[0]
    if mixed_precision is not None:
        dtype = mixed_precision
    else:
        dtype = A.dtype
    order = 'F'

    temp_file = None
    temp_dir = None
    scratch_file = ''
    scratch_nbytes = 0

    # Keep time of load and store
    io = {
        'load_wall_time': 0,
        'load_proc_time': 0,
        'store_wall_time': 0,
        'store_proc_time': 0,
        'num_block_loads': 0,
        'num_block_stores': 0,
    }

    # Block size
    m = (n + num_blocks - 1) // num_blocks

    if verbose:
        print(f'matrix size: {n}')
        print(f'num blocks: {num_blocks}')
        print(f'block size: {m}')
        print('dtype: %s' % str(dtype))

    # Initialize time and set memory counter
    mem = Memory(chunk=n**2, dtype=dtype, unit='MB')
    mem.set()
    init_wall_time = time.time()
    init_proc_time = time.process_time()

    # Start a Dask client to use multiple threads
    if (parallel_io == 'dask') and (num_blocks > 2):
        client = Client()

    block_nbytes = numpy.dtype(dtype).itemsize * (m**2)
    if parallel_io == 'mp':
        A11 = shared_memory.SharedMemory(create=True, size=block_nbytes)
    else:
        A11 = numpy.empty((m, m), dtype=dtype, order=order)

    if verbose:
        print('Allocated A11, %d bytes' % block_nbytes)

    # Create dask for input data
    if parallel_io == 'dask':
        if isinstance(A, zarr.core.Array):
            dask_A = da.from_zarr(A, chunks=(io_chunk, io_chunk))
        else:
            dask_A = da.from_array(A, chunks=(io_chunk, io_chunk))

    if num_blocks > 1:

        if parallel_io == 'mp':
            A12 = shared_memory.SharedMemory(create=True, size=block_nbytes)
            A21_t = shared_memory.SharedMemory(create=True, size=block_nbytes)
        else:
            A12 = numpy.empty((m, m), dtype=dtype, order=order)
            A21_t = numpy.empty((m, m), dtype=dtype, order=order)

        if verbose:
            print('Allocated A12, %d bytes' % block_nbytes)
            print('Allocated A21, %d bytes' % block_nbytes)

        if num_blocks > 2:

            if parallel_io == 'mp':
                A22 = shared_memory.SharedMemory(create=True,
                                                 size=block_nbytes)
            else:
                A22 = numpy.empty((m, m), dtype=dtype, order=order)

            if verbose:
                print('Allocated A22, %d bytes' % block_nbytes)

            # Scratch space to hold temporary intermediate blocks
            if parallel_io == 'mp':

                # Temporary file as scratch space
                temp_file = tempfile.NamedTemporaryFile(
                        prefix=_get_scratch_prefix(), suffix='.npy',
                        delete=True, dir=scratch_dir)
                scratch_file = temp_file.name

                scratch = numpy.memmap(temp_file.name, dtype=dtype, mode='w+',
                                       shape=(n, n-m), order=order)

            else:
                # Temporary directory as scratch space
                temp_dir = tempfile.mkdtemp(prefix=_get_scratch_prefix(),
                                            suffix='.zarr', dir=scratch_dir)

                scratch_file = temp_dir

                scratch = zarr.open(temp_dir, mode='w', shape=(n, n-m),
                                    dtype=dtype, order=order)

                if parallel_io == 'dask':
                    dask_scratch = da.from_zarr(
                            scratch, chunks=(io_chunk, io_chunk))

            if verbose:
                print('created scratch space: %s.' % scratch_file)

            # Cache table flagging which block is moved to scratch space. False
            # means the block is not yet on scratch space, True means it is
            # cached in the scratch space
            cached = numpy.zeros((num_blocks, num_blocks), dtype=bool)

    alloc_mem = mem.now()
    alloc_mem_peak = mem.peak()

    # ----------
    # load block
    # ----------

    def _load_block(array, i, j, trans=False):
        """
        If triangle is 'l' or 'u', it replicates the other half of the
        triangle only if reading the original data from the input matrix. But
        when loading from the scratch space, it does not replicate the other
        half. This is because when data are stored to scratch space, all matrix
        is stored, not just a half triangle of it. Hence its loading should be
        full.
        """

        io['num_block_loads'] += 1

        # Initialize load times
        init_load_wall_time = time.time()
        init_load_proc_time = time.process_time()

        if verbose:
            print('loading ... ', end='', flush=True)

        if (num_blocks > 2) and (bool(cached[i, j]) is True):
            read_from_scratch = True
        else:
            read_from_scratch = False

        if ((not read_from_scratch) and
            (((triangle == 'l') and (i < j)) or
             ((triangle == 'u') and (i > j)))):
            i_ = j
            j_ = i
            trans = numpy.logical_not(trans)
        else:
            i_ = i
            j_ = j

        i1 = m*i_
        if i_ == num_blocks-1:
            i2 = n
        else:
            i2 = m*(i_+1)

        j1 = m*j_
        if j_ == num_blocks-1:
            j2 = n
        else:
            j2 = m*(j_+1)

        if read_from_scratch:

            if parallel_io == 'mp':
                # Read in parallel
                load(scratch, (i1, i2), (j1-m, j2-m), array, (m, m), order,
                     trans, num_proc=None)
            else:
                # Get buffer from shared memory
                array_ = _get_array(array, m, dtype, order)

                if parallel_io == 'dash':
                    # Read from scratch
                    if trans:
                        with dask.config.set(scheduler='threads'):
                            array_[:, :] = \
                                da.store(dask_scratch[i1:i2, (j1-m):(j2-m)].T,
                                         array_)
                    else:
                        with dask.config.set(scheduler='threads'):
                            da.store(dask_scratch[i1:i2, (j1-m):(j2-m)],
                                     array_)

                else:
                    # Read from scratch
                    if trans:
                        array_[:, :] = scratch[i1:i2, (j1-m):(j2-m)].T
                    else:
                        array_[:, :] = scratch[i1:i2, (j1-m):(j2-m)]
        else:

            if (parallel_io == 'mp') and isinstance(A, numpy.memmap):
                # Read in parallel
                load(A, (i1, i2), (j1, j2), array, (m, m), order, trans,
                     num_proc=None)
            else:

                # Get buffer from shared memory
                array_ = _get_array(array, m, dtype, order)

                if parallel_io == 'dask':
                    # Read from original data
                    if trans:
                        with dask.config.set(scheduler='threads'):
                            da.store(dask_A[i1:i2, j1:j2].T, array_)
                    else:
                        with dask.config.set(scheduler='threads'):
                            da.store(dask_A[i1:i2, j1:j2], array_)

                else:
                    # Read from original data
                    if trans:
                        array_[:, :] = A[i1:i2, j1:j2].T
                    else:
                        array_[:, :] = A[i1:i2, j1:j2]

        # Fill the other half of diagonal blocks (if input data is triangle)
        if (i == j) and (triangle is not None) and (not read_from_scratch):

            # Get buffer from shared memory
            array_ = _get_array(array, m, dtype, order)

            if (triangle == 'l'):
                lower = True
            else:
                lower = False

            fill_triangle(array_, lower)

        # load times
        io['load_wall_time'] += time.time() - init_load_wall_time
        io['load_proc_time'] += time.process_time() - init_load_proc_time

        if verbose:
            print('done', flush=True)

    # -----------
    # store block
    # -----------

    def _store_block(array, i, j, flush=True):
        """
        Store array to scratch space.
        """

        io['num_block_stores'] += 1

        # Initialize store times
        init_store_wall_time = time.time()
        init_store_proc_time = time.process_time()

        if verbose:
            print('storing ... ', end='', flush=True)

        i1 = m*i
        if i == num_blocks-1:
            i2 = n
        else:
            i2 = m*(i+1)

        j1 = m*j
        if j == num_blocks-1:
            j2 = n
        else:
            j2 = m*(j+1)

        if parallel_io == 'mp':
            # Write in parallel
            trans = False
            store(scratch, (i1, i2), (j1-m, j2-m), array, (m, m), order, trans,
                  num_proc=None)
        else:
            # Get buffer from shared memory
            array_ = _get_array(array, m, dtype, order)

            if parallel_io == 'dask':
                with dask.config.set(scheduler='threads'):
                    dask_array = da.from_array(
                            array_, chunks=(io_chunk, io_chunk))
                    scratch[i1:i2, (j1-m):(j2-m)] = dask_array.compute()
            else:
                scratch[i1:i2, (j1-m):(j2-m)] = array_

        # Cache table to flag the block is now written to scratch space, so
        # next time, in order to access the block, scratch space should be
        # read, rather than the input matrix.
        cached[i, j] = True

        if flush and isinstance(scratch, numpy.memmap):
            scratch.flush()

        # store times
        io['store_wall_time'] += time.time() - init_store_wall_time
        io['store_proc_time'] += time.process_time() - init_store_proc_time

        if verbose:
            print('done', flush=True)

    # ------

    try:

        # Output, this will accumulate logdet of each diagonal block
        ld = 0
        sign = 1
        diag = []
        counter = 0
        total_count = (num_blocks-1) * num_blocks * (2*num_blocks+-1) // 6

        # Diagonal iterations
        for k in range(num_blocks):

            if k == 0:
                _load_block(A11, k, k)

            # lu_11, piv = _lu_factor(A11, m, dtype, order, overwrite)
            lu_11, d, perm = _ldl_factor(A11, m, dtype, order, overwrite)

            # log-determinant
            diag_lu_11 = numpy.diag(lu_11)
            ld += numpy.sum(numpy.log(numpy.abs(diag_lu_11)))

            # Sign of determinant
            # perm = _pivot_to_permutation(piv)
            parity = _permutation_parity(perm)
            sign *= numpy.prod(numpy.sign(diag_lu_11)) * parity

            # Save diagonals
            diag.append(numpy.copy(diag_lu_11))

            # Row iterations
            for i in range(num_blocks-1, k, -1):

                _load_block(A21_t, i, k, trans=True)

                # Solve upper-triangular system
                l_21_t = _solve_triangular(lu_11, A21_t, m, dtype, order,
                                           trans='T', lower=False,
                                           unit_diagonal=False,
                                           overwrite=overwrite)

                if (i - k) % 2 == 0:
                    # Start space-filling curve in a forward direction in the
                    # last row
                    j_start = k+1
                    j_end = num_blocks
                    j_step = +1
                else:
                    # start space-filling curve in a backward direction in the
                    # last row
                    j_start = num_blocks-1
                    j_end = k
                    j_step = -1

                # Column iterations
                for j in range(j_start, j_end, j_step):

                    # When the space-filling curve changes direction, do not
                    # read new A12, rather use the previous matrix already
                    # loaded to memory
                    if ((i == num_blocks-1) or (j != j_start) or
                            (overwrite is False)):
                        _load_block(A12, k, j)

                    if i == num_blocks-1:

                        # Permute A12
                        _permute_array(A12, perm, m, dtype, order)

                        # Solve lower-triangular system
                        u_12 = _solve_triangular(
                                lu_11, A12, m, dtype, order, trans='N',
                                lower=True, unit_diagonal=True,
                                overwrite=overwrite)

                        # Check u_12 is actually overwritten to A12
                        if overwrite:
                            A_12_array = _get_array(A12, m, dtype, order)
                            if not numpy.may_share_memory(u_12, A_12_array):
                                raise RuntimeError(
                                    '"A12" is not overwritten to "u_12".')

                        if num_blocks > 2:
                            # Store u_12, which is the same as A12 since u_12
                            # is overwritten to A_12. For this to always be the
                            # case, make sure overwrite is set to True in
                            # computing u_12.
                            if overwrite is True:
                                _store_block(A12, k, j)
                            else:
                                _store_block(u_12, k, j)
                    else:
                        u_12 = _get_array(A12, m, dtype, order)

                    if (i == k+1) and (j == k+1):
                        _load_block(A11, i, j)
                        _schur_complement(l_21_t, u_12, A11, m, dtype, order)
                    else:
                        _load_block(A22, i, j)
                        _schur_complement(l_21_t, u_12, A22, m, dtype, order)
                        _store_block(A22, i, j)

                    counter += 1
                    print(f'progress: {counter:>3d}/{total_count:>3d}, ',
                          end='', flush=True)
                    print(f'diag: {k+1:>2d}, ', end='', flush=True)
                    print(f'row: {i+1:>2d}, ', end='', flush=True)
                    print(f'col: {j+1:>2d}', flush=True)

        # concatenate diagonals of blocks of U
        # diag = numpy.concatenate(diag)

        # record time
        tot_wall_time = time.time() - init_wall_time
        tot_proc_time = time.process_time() - init_proc_time

    except Exception as e:
        print('failed')
        raise e

    finally:

        if temp_file is not None:
            scratch_nbytes = os.path.getsize(scratch_file)
            temp_file.close()
        elif temp_dir is not None:
            scratch_nbytes = _get_dir_size(temp_dir)
            shutil.rmtree(temp_dir)

            if verbose:
                print('removed scratch space: %s.' % scratch_file)

        # Free memory
        if ('A11' in locals()) and isinstance(A11, shared_memory.SharedMemory):
            A11.close()
            A11.unlink

        if ('A12' in locals()) and isinstance(A12, shared_memory.SharedMemory):
            A12.close()
            A12.unlink

        if ('A21_t' in locals()) and \
                isinstance(A21_t, shared_memory.SharedMemory):
            A21_t.close()
            A21_t.unlink

        if ('A22' in locals()) and isinstance(A22, shared_memory.SharedMemory):
            A22.close()
            A22.unlink

        # Record total memory consumption since start
        total_mem = mem.now()
        total_mem_peak = mem.peak()

    # Shut down the Dask client
    if (parallel_io == 'dask') and (num_blocks > 2):
        client.close()

    if return_info:
        info = {
            'matrix': {
                'dtype': str(A.dtype),
                'matrix_shape': (n, n),
                'triangle': triangle,
                'assume': assume,
            },
            'process': {
                'processor': get_processor_name(),
                'num_proc': get_avail_num_threads(),
                'tot_wall_time': tot_wall_time,
                'tot_proc_time': tot_proc_time,
                'load_wall_time': io['load_wall_time'],
                'load_proc_time': io['load_proc_time'],
                'store_wall_time': io['store_wall_time'],
                'store_proc_time': io['store_proc_time'],
            },
            'block': {
                'block_nbytes': block_nbytes,
                'block_shape': (m, m),
                'matrix_blocks': (num_blocks, num_blocks),
            },
            'scratch': {
                'num_scratch_blocks': num_blocks * (num_blocks - 1) - 1,
                'scratch_file': scratch_file,
                'scratch_nbytes': scratch_nbytes,
                'num_block_loads': io['num_block_loads'],
                'num_block_stores': io['num_block_stores'],
            },
            'memory': {
                'alloc_mem': alloc_mem,
                'alloc_mem_peak': alloc_mem_peak,
                'total_mem': total_mem,
                'total_mem_peak': total_mem_peak,
                'mem_unit': '%d bytes' % block_nbytes,
            },
            'solver': {
                'version': __version__,
                'method': 'lu',
                'dtype': str(dtype),
                'order': order,
            }
        }

        return ld, sign, diag, info

    else:

        return ld, sign, diag
