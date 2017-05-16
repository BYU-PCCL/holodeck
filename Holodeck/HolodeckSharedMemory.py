import mmap
import numpy as np

class HolodeckSharedMemory:
    def __init__(self, name, mem_size, map_size):
        self._mem_path = "/HOLODECK_MEM_" + name
        self._map_path = "/HOLODECK_MAP_" + name
        self._mem_size = mem_size
        self._map_size = map_size

        self._mem_pointer = mmap.mmap(0, mem_size, self._mem_path)
        self._map_pointer = mmap.mmap(0, map_size, self._map_path)

        self._map_current_length = 0
        self._mem_last_index = 0
        self._subscribed_items = {}

    def clear(self):
        pass

    def contains_key(self, agent_name, key):
        self.__update_subscribed_dict__()
        dict_key = agent_name + "/" + key
        return dict_key in self._subscribed_items and self._subscribed_items[dict_key] is not None

    def get(self, agent_name, key):
        assert self.contains_key(agent_name, key)

        data = self._subscribed_items[agent_name + "/" + key]

        # TODO: Handle the different types of sensor
        if key == 'PrimaryPlayerCamera':
            print "Sensor not handled yet:", key
            #hex_data = bytearray.fromhex(data[1:-1])
            #return np.frombuffer(hex_data, dtype=np.uint8).reshape(self.resolution)

        elif key == 'CameraSensorArray2D':
            print "Sensor not handled yet:", key
            # sensor = json.loads(data)
            # images = []
            # for obj in sensor:
            #     for camera, byte_array in obj.items():
            #         hex_data = bytearray.fromhex(byte_array)
            #         images.append(np.frombuffer(hex_data, dtype=np.uint8).reshape([256, 256, 3]))
            #         # img = base64.b64decode(base64_image)
            #         #
            #         # np_img = np.fromstring(img, dtype=np.uint8)
            #         # images.append(np_img)
            # return images

        elif key == 'RelativeSkeletalPositionSensor':
            print "Sensor not handled yet:", key
            # skeletal_positions = json.loads(data)
            # positions = np.empty([67, 4])
            # for i, obj in enumerate(skeletal_positions):
            #     positions[i][0] = obj["Quaternion"]["X"]
            #     positions[i][1] = obj["Quaternion"]["Y"]
            #     positions[i][2] = obj["Quaternion"]["Z"]
            #     positions[i][3] = obj["Quaternion"]["W"]
            #
            # return positions

        elif key == 'JointRotationSensor' or type == 'IMUSensor':
            print "Sensor not handled yet:", key
            # return np.array(json.loads(data))

        elif key == "OrientationSensor":
            print "Sensor not handled yet:", key
            # return np.array(data.split(',')).astype(np.float32).reshape([3, 3]).T

        else:
            print "Sensor has no handler:", key

        return

    def subscribe(self, agent_name, key, size):
        pass

    def set(self, agent_name, key, data):
        pass

    def get_data(self):
        pass

    def get_mapping(self):
        results = []
        self._map_pointer.seek(0)
        line = self._map_pointer.readline()
        while line:
            results.append(line.split())
            line = self._map_pointer.readline()

        print results[0]

    def __get_length__(self):
        length = self._map_current_length
        self._map_pointer.seek(length)
        while (self._map_pointer.read_byte() != '\0'):
            length += 1
        return length

    def __update_subscribed_dict__(self):
        new_length = self.__get_length__()
        if new_length == self._map_current_length:
            return
        old_length = self._map_current_length
        self._map_current_length = new_length

        # Otherwise, read the new sensor data
        self._map_pointer.seek(old_length)
        new_raw_data = self._map_pointer.read(self._map_current_length - old_length).split()

        # Save it into the sensors
        num_new = len(new_raw_data) / 5
        for i in xrange(num_new):
            new_data = new_raw_data[5*i:5*i+5]
            new_data[2:] = map(int, new_data[2:])
            self._subscribed_items[new_data[0] + "/" + new_data[1]] = new_data
