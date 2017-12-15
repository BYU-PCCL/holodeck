from __future__ import print_function
from .Environments import  *
from .Exceptions import HolodeckException
from .Agents import *


def make(world):
    worlds = {"SphereMaze-v0": {"agent_type": DiscreteSphereAgent,
                                "agent_name": "sphere0",
                                "task_key": HolodeckMaps.MAZE_WORLD_SPHERE,
                                "height": 512,
                                "width": 512,
                                "start_world": True,
                                "sensors": [Sensors.PRIMARY_PLAYER_CAMERA, Sensors.ORIENTATION_SENSOR]}}

    if world not in worlds:
        raise HolodeckException("Invalid World Name")

    return HolodeckEnvironment(**worlds[world])
