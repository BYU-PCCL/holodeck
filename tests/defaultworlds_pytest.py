import holodeck
from holodeck.packagemanager import get_scenario
from test_utils import *
from test_lib import *


def test_infiniteforest():
    env = holodeck.make("InfiniteForest-MaxDistance")
    load_test(env, "InfiniteForest-MaxDistance")
    reset_test(env, "uav0", sensors_to_ignore=["RGBCamera"])
    action_test(env, "uav0", [100, 100, 100, 100], ["LocationSensor", "OrientationSensor"])

def test_androidplayground():
    env = holodeck.make("AndroidPlayground-MaxDistance")
    load_test(env, "AndroidPlayground-MaxDistance")
    reset_test(env, "android0", sensors_to_ignore=["RGBCamera"])
    action_test(env, "android0", np.ones(94) * 10, ["LocationSensor", "OrientationSensor", "JointRotationSensor"])

def test_cyberpunk():
    env = holodeck.make("CyberPunkCity-FollowSight")
    load_test(env, "CyberPunkCity-FollowSight")
    reset_test(env, "uav0", sensors_to_ignore=["RGBCamera"])
    reset_test(env, "nav0")
    action_test(env, "uav0", [0, 0, 100, 1000], ["LocationSensor", "OrientationSensor"])
    action_test(env, "nav0", [0, 0, .3], ["LocationSensor"])

def test_european():
    env = holodeck.make("EuropeanForest-MaxDistance")
    load_test(env, "EuropeanForest-MaxDistance")
    reset_test(env, "uav0", sensors_to_ignore=["RGBCamera"])
    action_test(env, "uav0", [100, 100, 100, 100], ["LocationSensor", "OrientationSensor"])

def test_mazeworld():
    env = holodeck.make("MazeWorld-FinishMazeSphere")
    load_test(env, "MazeWorld-FinishMazeSphere")
    reset_test(env, "sphere0", sensors_to_ignore=["RGBCamera"])
    action_test(env, "sphere0", [2], ["OrientationSensor"])

def test_redwood():
    env = holodeck.make("RedwoodForest-MaxDistance")
    load_test(env, "RedwoodForest-MaxDistance")
    reset_test(env, "uav0", sensors_to_ignore=["RGBCamera"])
    action_test(env, "uav0", [100, 100, 100, 100], ["LocationSensor", "OrientationSensor"])

def test_urbancity():
    env = holodeck.make("UrbanCity-MaxDistance")
    load_test(env, "UrbanCity-MaxDistance")
    reset_test(env, "uav0", sensors_to_ignore=["RGBCamera"])
    action_test(env, "uav0", [0,0,2,12], ["LocationSensor", "OrientationSensor"])

