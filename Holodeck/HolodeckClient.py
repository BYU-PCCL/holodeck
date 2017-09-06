import os
from HolodeckSharedMemory import HolodeckSharedMemory


class HolodeckClient:
    def __init__(self):
        # Important functions
        self._get_semaphore_fn = None
        self._release_semaphore_fn = None
        self._semaphore1 = None
        self._semaphore2 = None

        self._sensors = dict()
        self._agents = dict()
        self._settings = dict()

        if os.name == "nt":
            self.__windows_init__()
        elif os.name == "posix":
            self.__posix_init__()
        else:
            print "Currently unsupported os:", os.name

    def __windows_init__(self):
        import win32event
        semaphore_all_access = 0x1F0003
        self._semaphore1 = win32event.OpenSemaphore(semaphore_all_access, False, "Global\\HOLODECK_SEMAPHORE_1")
        self._semaphore2 = win32event.OpenSemaphore(semaphore_all_access, False, "Global\\HOLODECK_SEMAPHORE_2")

        def windows_acquire_semaphore(sem):
            win32event.WaitForSingleObject(sem, 100000) # 100 second timeout

        def windows_release_semaphore(sem):
            win32event.ReleaseSemaphore(sem, 1)

        self._get_semaphore_fn = windows_acquire_semaphore
        self._release_semaphore_fn = windows_release_semaphore

    def __posix_init__(self):
        import posix_ipc
        self._semaphore1 = posix_ipc.Semaphore("/tmp/HOLODECK_SEMAPHORE_1")
        self._semaphore2 = posix_ipc.Semaphore("/tmp/HOLODECK_SEMAPHORE_2")

        def posix_acquire_semaphore(sem):
            sem.acquire(None)

        def posix_release_semaphore(sem):
            sem.release()

        self._get_semaphore_fn = posix_acquire_semaphore
        self._release_semaphore_fn = posix_release_semaphore

    def acquire(self):
        self._get_semaphore_fn(self._semaphore2)

    def release(self):
        self._release_semaphore_fn(self._semaphore1)

    def subscribe_sensor(self, agent_name, sensor_key, shape, dtype):
        key = agent_name + "_" + sensor_key
        self._sensors[key] = HolodeckSharedMemory(key, shape, dtype)

    def get_sensor(self, agent_name, sensor_key):
        return self._sensors[agent_name + "_" + sensor_key].np_array

    def subscribe_command(self, agent_name, shape):
        self._agents[agent_name] = HolodeckSharedMemory(agent_name, shape)
        return self._agents[agent_name].np_array

    def subscribe_setting(self, setting_name, shape, dtype):
        self._settings[setting_name] = HolodeckSharedMemory(setting_name, shape, dtype)
        return self._settings[setting_name].np_array
