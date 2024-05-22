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
import platform
import subprocess
import re

__all__ = ['get_processor_name', 'get_data_type_name']


# ==================
# get processor name
# ==================

def get_processor_name():
    """
    Returns name of processor.
    """

    if platform.system() == "Windows":
        return platform.processor()

    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()

    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(
                command, shell=True).decode().strip()

        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)

    return ""


# ==================
# get data type name
# ==================

def get_data_type_name(data):
    """
    Returns the typename of data as string.
    """

    if data.dtype in [b'float32', 'float32']:
        data_type_name = b'float32'
    elif data.dtype in [b'float64', 'float64']:
        data_type_name = b'float64'
    elif data.dtype in [b'float128', 'float128']:
        data_type_name = b'float128'
    elif data.dtype in [b'int32', 'int32']:
        data_type_name = b'int32'
    elif data.dtype in [b'int64', 'int64']:
        data_type_name = b'int64'
    else:
        raise TypeError('Data type should be "float32", "float64", ' +
                        '"float128", "int32", or "int64".')

    return data_type_name
