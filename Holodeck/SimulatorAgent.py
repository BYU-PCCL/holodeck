import zmq
from gym import spaces
import json
import threading
from collections import defaultdict
import time
import numpy as np
import base64


class SimulatorAgent(object):
    class TimeoutError(Exception):
        pass
    
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultAgent", height=256, width=256):
        self.resolution = [height, width, 3]
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, agentName.encode("ascii"))
        self.socket.connect("tcp://" + hostname + ":" + str(port))
        self.socket.setsockopt(zmq.SNDTIMEO, 1000)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.delegates = defaultdict(list)

        self.is_listening = True
        self.thread = threading.Thread(target=self.__listen__)
        self.thread.daemon = True
        self.thread.start()

        self.state_locks = {}
        self.state = {}
        self.last_receive_error = None

    def wait_for_connect(self):
        class context:
            isWaiting = True

        def wait(command, type):
            context.isWaiting = False

        self.subscribe('Connect', wait)

        while context.isWaiting:
            self.send_command("WaitForConnect", None)
            time.sleep(1)
        

        self.unsubscribe('Connect', wait)

        return self

    def send_command(self, type, command):
        try:
            message = json.dumps({
                "CommandType": type,
                "CommandJSON": json.dumps(command) if command else ""
            })
            return self.socket.send_string(message)
        except zmq.ZMQError:
            print("Error in sendString")
            return None

    def __receive__(self, blocking=True):
        try:
            data = self.socket.recv(flags=0 if blocking else zmq.NOBLOCK)
            return json.loads(data.decode())
        except zmq.Again as e:
            self.__on_receive_error__(e)

    def __listen__(self):
        while self.is_listening:
            message = self.__receive__(True)
            if message is not None:
                self.__publish__(message)

    def kill(self):
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.is_listening = False
        self.thread.join()

    def subscribe(self, type, function):
        self.delegates[type].append(function)

    def unsubscribe(self, type, function):
        self.delegates[type].remove(function)

    def __publish__(self, message):
        if len(self.delegates[message['type']]) != 0:
            processed_message = self.__preprocess__(message['data'], message['type'])

        for function in self.delegates[message['type']]:
            function(processed_message, message['type'])

    def __preprocess__(self, data, type):
        if type == 'PrimaryPlayerCamera':
            hex_data = bytearray.fromhex(data[1:-1])
            return np.frombuffer(hex_data, dtype=np.uint8).reshape(self.resolution)
            
        elif type == 'CameraSensorArray2D':
            sensor = json.loads(data)
            images = []
            for obj in sensor:
                for camera, base64_image in obj.items():
                    img = base64.b64decode(base64_image)

                    np_img = np.fromstring(img, dtype=np.uint8)
                    images.append(np_img)
            return images

        elif type == 'RelativeSkeletalPositionSensor':
            skeletal_positions = json.loads(data)
            positions = []
            for obj in skeletal_positions:
                positions += [obj["Quaternion"]["X"]. obj["Quaternion"]["Y"], obj["Quaternion"]["Z"], obj["Quaternion"]["W"]]

            return positions

        elif type == 'JointRotationSensor' or type == 'IMUSensor':
            return json.loads(data)

        return data

    def __on_receive_error__(self, error):
        self.last_receive_error = error
        for sensor, lock in self.state_locks.items():
            lock.release()

    def __store_state__(self, data, type):
        self.state[type] = data
        self.state_locks[type].release()

    def act(self, action, sensors):
        while True:
            self.last_receive_error = None

            for sensor in sensors:
                self.state_locks[sensor] = threading.Semaphore(1)
                self.state_locks[sensor].acquire()
                self.subscribe(sensor, self.__store_state__)

            self.__act__(action)
            
            response = []
            for sensor in sensors:
                self.state_locks[sensor].acquire()
                self.unsubscribe(sensor, self.__store_state__)
                if sensor in self.state:
                    response.append(self.state[sensor])
                
            if self.last_receive_error is None:
                break
            
        return response

    @property
    def action_space(self):
        raise NotImplementedError()

    def __act__(self, action):
        raise NotImplementedError()


class UAVAgent(SimulatorAgent):
    @property
    def action_space(self):
        return spaces.Box(-100, 100, shape=[4])

    def __act__(self, action):
        self.send_command('UAVCommand', {
            "Roll": str(action[0]),
            "Pitch": str(action[1]),
            "YawRate": str(action[2]),
            "Altitude": str(action[3])
        })


class ContinuousSphereAgent(SimulatorAgent):
    @property
    def action_space(self):
        return spaces.Box(-100, 100, shape=[2])

    def __act__(self, action):
        self.send_command('SphereRobotCommand', {
            "Forward": str(action[0]),
            "Right": str(action[1])
        })


class DiscreteSphereAgent(SimulatorAgent):
    @property
    def action_space(self):
        return spaces.Discrete(4)

    def __act__(self, action):
        actions = [(10, 0), (-10, 0), (0, 90), (0, -90)]
        to_act = None
        for i, j in enumerate(action):
            if j == 1:
                to_act = actions[i]

        if to_act is None:
            raise RuntimeError("Action must be one-hot")

        self.send_command('SphereRobotCommand', {
            "Forward": str(to_act[0]),
            "Right": str(to_act[1])
        })


class AndroidAgent(SimulatorAgent):
    @property
    def action_space(self):
        return spaces.Box(-1000, 1000, shape=[127])

    def __act__(self, action):
        action = map(str,action)
        self.send_command('AndroidCommand', {
            "ConstraintVector": action
        })