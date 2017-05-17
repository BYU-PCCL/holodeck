import os
from HolodeckSharedMemory import HolodeckSharedMemory


class HolodeckClient:
    def __init__(self):
        # Important functions
        self._get_semaphore_fn = None
        self._release_semaphore_fn = None
        self._semaphore1 = None
        self._semaphore2 = None

        self._sensors = HolodeckSharedMemory("SENSORS", 33177600, 10000)
        self._commands = HolodeckSharedMemory("COMMANDS", 10000, 10000)
        self._settings = HolodeckSharedMemory("SETTINGS", 10000, 10000)

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
        # Do the necessary imports
        # TODO
        raise NotImplementedError()

    def acquire(self):
        self._get_semaphore_fn(self._semaphore2)

    def release(self):
        self._release_semaphore_fn(self._semaphore1)

    def start(self):
        # TODO
        raise NotImplementedError()

    def kill(self):
        # TODO
        raise NotImplementedError()

    def subscribe_sensor(self, agent_name, sensor_key, size):
        self._sensors.subscribe(agent_name, sensor_key, size)

    def set_sensor(self, agent_name, sensor_key, data):
        self._sensors.set(agent_name, sensor_key, data)

    def get_sensor(self, agent_name, sensor_key):
        return self._sensors.get(agent_name, sensor_key)

    def get_sensor_data(self):
        self._sensors.get_data()

    def get_sensor_mapping(self):
        self._sensors.get_mapping()

    def subscribe_command(self, agent_name, command_key, size):
        self._sensors.subscribe(agent_name, command_key, size)

    def set_command(self, agent_name, command_key, data):
        self._sensors.set(agent_name, command_key, data)

    def get_command(self, agent_name, command_key):
        return self._commands.get(agent_name, command_key)

    def get_command_data(self):
        self._commands.get_data()

    def get_command_mapping(self):
        self._commands.get_mapping()

    def subscribe_setting(self, agent_name, setting_key, size):
        self._sensors.subscribe(agent_name, setting_key, size)

    def set_setting(self, agent_name, setting_key, data):
        self._commands.set(agent_name, setting_key, data)

    def get_setting(self, agent_name, setting_key):
        return self._settings.get(agent_name, setting_key)

    def get_setting_data(self):
        self._settings.get_data()

    def get_setting_mapping(self):
        self._settings.get_mapping()
