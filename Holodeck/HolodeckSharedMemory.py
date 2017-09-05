import mmap
import numpy as np
import os
import ctypes


class HolodeckSharedMemory:
    _numpy_to_ctype = {
        np.float32: ctypes.c_float,
        np.uint8: ctypes.c_uint8,
        np.bool: ctypes.c_bool,
    }

    def __init__(self, name, shape, dtype=np.float32):
        size = reduce(lambda x, y: x * y, shape)
        size_bytes = np.dtype(dtype).itemsize * size

        self._mem_path = None
        self._mem_pointer = None
        if os.name == "nt":
            self._mem_path = "/HOLODECK_MEM_" + name
            self._mem_pointer = mmap.mmap(0, size_bytes, self._mem_path)
        elif os.name == "posix":
            self._mem_path = "/tmp/HOLODECK_MEM_" + name
            f = os.open(self._mem_path, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
            os.ftruncate(f, size_bytes)
            self._mem_pointer = mmap.mmap(f, size_bytes)
        else:
            print "Currently unsupported os:", os.name

        self.np_array = np.ndarray(shape, dtype=dtype)
        self.np_array.data = (HolodeckSharedMemory._numpy_to_ctype[dtype] * size).from_buffer(self._mem_pointer)
