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

import tracemalloc


# ======
# Memory
# ======

class Memory(object):
    """
    Trace memory allocation.

    Parameters
    ----------

    unit : str {``'B'``, ``'KB'``, ``'MB'``, ``'GB'``, ``'TB'``}, \
            default=``'MB'``
        Unit of the memory

    chunk : int, default=1
        The reporting memory is divided by chunk. That ism, a chunk of memory
        is considered as one unit of memory. This is useful to compare the
        memory with the size of an array. For instance, for an array of size
        1000, if ``chunk=100``, the reported memory becomes 1.

    dtype : str, default='float64'
        Data type
    """

    # ====
    # init
    # ====

    def __init__(self, unit='MB', chunk=1, dtype='float64'):
        """
        Initialization.
        """

        self._mem = 0
        self._peak = 0
        self._init_mem = 0
        self._init_peak = 0
        self.chunk = chunk

        # Set unit size
        if unit == 'B':
            self.unit_size = 1
        elif unit == 'KB':
            self.unit_size = 1024
        elif unit == 'MB':
            self.unit_size = 1024**2
        elif unit == 'GB':
            self.unit_size = 1024**3
        elif unit == 'TB':
            self.unit_size = 1024**4
        else:
            raise ValueError('"unit" is invalid.')

        # Set itemsize from dtype
        if dtype is None:
            self.itemsize = 1
        elif dtype == 'float16':
            self.itemsize = 2
        elif dtype == 'float32':
            self.itemsize = 4
        elif dtype == 'float64':
            self.itemsize = 8
        elif dtype == 'float128':
            self.itemsize = 16
        else:
            raise ValueError('"dtype" is invalid.')

        # Memory size of an array of the size "chunk" of data type "dtype"
        self.scale = self.itemsize * self.chunk

        self.set()

    # ===
    # set
    # ===

    def set(self):
        """
        Set or reset tracing allocated memory.
        """

        tracemalloc.start()
        tracemalloc.clear_traces()
        tracemalloc.reset_peak()

        mem, peak = tracemalloc.get_traced_memory()
        self._init_mem = mem / self.scale
        self._init_peak = peak / self.scale
        self._mem = 0
        self._peak = 0

    # ====
    # read
    # ====

    def _read(self):
        """
        Returns current and peak memory allocation.
        """

        mem, peak = tracemalloc.get_traced_memory()
        self._mem = (mem / self.scale) - self._init_mem
        self._peak = (peak / self.scale) - self._init_peak

    # ===
    # now
    # ===

    def now(self):
        """
        Returns current memory allocation.
        """

        self._read()
        return self._mem

    # ====
    # peak
    # ====

    def peak(self):
        """
        Returns peak memory allocation since memory is set.
        """

        self._read()
        return self._peak
