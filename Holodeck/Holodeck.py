import uuid

from .Environments import *
from .Exceptions import HolodeckException
from .Agents import *


# Load in all existing worlds
holodeck_path = os.environ("HOLODECKPATH")
if holodeck_path == "":
    raise HolodeckException("Couldn't find environment variable HOLODECKPATH.")
for file_name in os.listdir(os.path.join(holodeck_path, "worlds")):
    if file_name.endswith(".config"):
        with open(file_name, 'r') as f:
            for line in f.readlines():
                print(line)


def make(world):
    worlds = {"SphereMaze-v0": {"agent_type": DiscreteSphereAgent,
                                "agent_name": "sphere0",
                                "task_key": HolodeckMaps.MAZE_WORLD_SPHERE,
                                "height": 512,
                                "width": 512,
                                "start_world": True,
                                "sensors": [Sensors.PRIMARY_PLAYER_CAMERA, Sensors.ORIENTATION_SENSOR],
                                "uuid": str(uuid.uuid4())}}

    if world not in worlds:
        raise HolodeckException("Invalid World Name")

    return HolodeckEnvironment(**worlds[world])
