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
from multiprocessing import Process, shared_memory
from .._openmp import get_avail_num_threads

__all__ = ['load', 'store']


# ==========
# load slice
# ==========

def _transfer_slice(
        memmap,
        memmap_row_range,
        memmap_col_range,
        shared_mem_name,
        shared_mem_shape,
        order,
        trans,
        operation,
        num_proc,
        proc_index):
    """
    """

    num_rows = memmap_row_range[1] - memmap_row_range[0]

    # Calculate rows per core
    num_rows_per_proc = (num_rows // num_proc) + (num_rows % num_proc > 0)

    # Start and of rows in each process
    start_row = proc_index * num_rows_per_proc
    end_row = min((proc_index + 1) * num_rows_per_proc, num_rows)

    # Access the existing shared memory
    existing_shared_mem = shared_memory.SharedMemory(name=shared_mem_name)
    array = numpy.ndarray(shared_mem_shape, dtype=memmap.dtype,
                          buffer=existing_shared_mem.buf, order=order)

    if operation == 'r':
        # Transfer from memmap to shared mem (reading from scratch space)
        if trans:
            array[:, start_row:end_row] = memmap[
                memmap_row_range[0]+start_row:memmap_row_range[0]+end_row,
                memmap_col_range[0]:memmap_col_range[1]].T
        else:
            array[start_row:end_row, :] = memmap[
                memmap_row_range[0]+start_row:memmap_row_range[0]+end_row,
                memmap_col_range[0]:memmap_col_range[1]]

    elif operation == 'w':
        # Transfer from shared mem to memmap (writing to scrarch space)
        if trans:
            memmap[
                memmap_row_range[0]+start_row:memmap_row_range[0]+end_row,
                memmap_col_range[0]:memmap_col_range[1]] = \
                        array[:, start_row:end_row].T
        else:
            memmap[
                memmap_row_range[0]+start_row:memmap_row_range[0]+end_row,
                memmap_col_range[0]:memmap_col_range[1]] = \
                        array[start_row:end_row, :]

    else:
        raise ValueError('Operation should be "r" or "w".')

    # No need to close the shared memory here since we are not deleting it
    existing_shared_mem.close()


# ===========
# parallel io
# ===========

def _parallel_io(
        memmap,
        memmap_row_range,
        memmap_col_range,
        shared_mem,
        shared_mem_shape,
        order,
        trans,
        operation,
        num_proc=None):
    """
    Load or store a slice of matrix to shared memory array in parallel.
    """

    # Check Operation
    if operation not in ['r', 'w']:
        raise ValueError('Operation should be "r" or "w".')

    # Check type
    if not isinstance(memmap, numpy.memmap):
        raise TypeError('"memmap" should be a numpy.memmap object.')

    if not isinstance(shared_mem, shared_memory.SharedMemory):
        raise TypeError('"shared_mem" should be a SharedMemory object.')

    # Check consistency of shapes of memmap and shared memory
    num_rows = memmap_row_range[1] - memmap_row_range[0]
    num_columns = memmap_col_range[1] - memmap_col_range[0]

    if (trans is False) and ((num_rows, num_columns) != shared_mem_shape):
        raise ValueError('Source array rows and column ranges do not match ' +
                         'with the shape of shared memory array.')
    elif (trans is True) and ((num_columns, num_rows) != shared_mem_shape):
        raise ValueError('Source array rows and column ranges do not match ' +
                         'with the shape of transposed shared memory array.')

    # Size of memmap array slice
    itemsize = numpy.dtype(memmap.dtype).itemsize
    memmap_slice_nbytes = num_rows * num_columns * itemsize

    if memmap_slice_nbytes != shared_mem.size:
        raise RuntimeError('Size of shared memory (%d) ' % (shared_mem.size) +
                           'does not match the size of memory map slice (%d).'
                           % (memmap_slice_nbytes))

    # When number of processor is not specified, use all available cores
    if num_proc is None:
        num_proc = get_avail_num_threads()

    # List to hold processes
    processes = []

    for proc_index in range(num_proc):
        process = Process(target=_transfer_slice,
                          args=(memmap, memmap_row_range, memmap_col_range,
                                shared_mem.name, shared_mem_shape, order,
                                trans, operation, num_proc, proc_index))

        processes.append(process)

    try:
        for process in processes:
            process.start()
    finally:
        for process in processes:
            process.join()


# ====
# load
# ====

def load(
        memmap,
        memmap_row_range,
        memmap_col_range,
        shared_mem,
        shared_mem_shape,
        order,
        trans,
        num_proc=None):
    """
    Load a slice of matrix to shared memory array in parallel.
    """

    # Read operation
    _parallel_io(memmap, memmap_row_range, memmap_col_range, shared_mem,
                 shared_mem_shape, order, trans, operation='r',
                 num_proc=num_proc)


# =====
# store
# =====

def store(
        memmap,
        memmap_row_range,
        memmap_col_range,
        shared_mem,
        shared_mem_shape,
        order,
        trans,
        num_proc=None):
    """
    Store a slice of matrix from shared memory array in parallel.
    """

    # Write operation
    _parallel_io(memmap, memmap_row_range, memmap_col_range, shared_mem,
                 shared_mem_shape, order, trans, operation='w',
                 num_proc=num_proc)
