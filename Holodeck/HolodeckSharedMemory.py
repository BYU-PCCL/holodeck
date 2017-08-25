import mmap
import numpy as np
import ctypes

class HolodeckSharedMemory:
    _numpy_to_ctype = {
        np.float32: ctypes.c_float,
        np.bool: ctypes.c_bool,
    }

    def __init__(self, name, size, dtype=np.float32):
        size_bytes = np.dtype(dtype).itemsize * size
        self._mem_path = "/HOLODECK_MEM_" + name
        self._mem_size = size
        self._mem_pointer = mmap.mmap(0, size_bytes, self._mem_path)
        self.data = np.ndarray([size], dtype=dtype)
        self.data.data = (HolodeckSharedMemory._numpy_to_ctype[dtype] * size).from_buffer(self._mem_pointer)
