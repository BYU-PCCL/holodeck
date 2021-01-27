import copy
import os
import uuid
import holodeck
import cv2
import pytest


from tests.utils.equality import mean_square_err


base_cfg = {
    "name": "test_rgb_camera",
    "world": "TestWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "RGBCamera",
                    "socket": "CameraSocket",
                    # note the different camera name. Regression test for #197
                    "sensor_name": "TestCamera",
                }
            ],
            "control_scheme": 0,
            "location": [
                0.95,
                -1.75,
                0.5,
            ],  # if you change this, you must change rotation_env too.
        }
    ],
}


def test_rgb_camera(resolution, request):
    """Makes sure that the RGB camera is positioned and capturing correctly.

    Capture pixel data, and load from disk the baseline of what it should look like.
    Then, use mse() to see how different the images are.

    """
    global base_cfg

    cfg = copy.deepcopy(base_cfg)

    cfg["agents"][0]["sensors"][0]["configuration"] = {
        "CaptureWidth": resolution,
        "CaptureHeight": resolution,
    }

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(
        scenario=cfg,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:

        for _ in range(5):
            env.tick()

        pixels = env.tick()["TestCamera"][:, :, 0:3]
        baseline = cv2.imread(
            os.path.join(
                request.fspath.dirname, "expected", "{}.png".format(resolution)
            )
        )
        err = mean_square_err(pixels, baseline)

        assert err < 2000


shared_ticks_per_capture_env = None


@pytest.fixture(scope="module")
def ticks_per_capture_env():
    """test_rgb_camera_ticks_per_capture shares an environment with different
    instances of the same test
    """
    global base_cfg, shared_ticks_per_capture_env

    if shared_ticks_per_capture_env is None:
        cfg = copy.deepcopy(base_cfg)

        cfg["agents"][0]["sensors"][0]["configuration"] = {
            "CaptureWidth": 512,
            "CaptureHeight": 512,
        }

        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )

        shared_ticks_per_capture_env = holodeck.environments.HolodeckEnvironment(
            scenario=cfg,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )

    with shared_ticks_per_capture_env:
        yield shared_ticks_per_capture_env


def test_rgb_camera_ticks_per_capture(ticks_per_capture, ticks_per_capture_env):
    """Validate that the ticks_per_capture method actually makes the RGBCamera take fewer
    screenshots.

    Capture a screenshot, wait for it to change, then make sure that the image doesn't
    change until ticks_per_capture ticks have elapsed.

    """

    ticks_per_capture_env.reset()

    # The agent needs to be moving for the image to change
    ticks_per_capture_env.act("sphere0", [2])

    ticks_per_capture_env.agents["sphere0"].sensors["TestCamera"].set_ticks_per_capture(
        ticks_per_capture
    )

    # Take the initial capture, and wait until it changes
    initial = ticks_per_capture_env.tick()["TestCamera"][:, :, 0:3]

    MAX_TRIES = 50
    tries = 0

    while tries < MAX_TRIES:
        intermediate = ticks_per_capture_env.tick()["TestCamera"][:, :, 0:3]
        if mean_square_err(initial, intermediate) > 10:
            break
        tries += 1

    assert MAX_TRIES != tries, "Timed out waiting for the image to change!"

    # On the last tick, intermediate changed. Now, it should take
    # ticks_per_capture ticks for it to change again.
    initial = intermediate
    for _ in range(ticks_per_capture - 1):
        # Make sure it doesn't change
        intermediate = ticks_per_capture_env.tick()["TestCamera"][:, :, 0:3]
        assert (
            mean_square_err(initial, intermediate) < 10
        ), "The RGBCamera output changed unexpectedly!"

    # Now it should change

    final = ticks_per_capture_env.tick()["TestCamera"][:, :, 0:3]
    assert (
        mean_square_err(initial, final) > 10
    ), "The RGBCamera output did not change when expected!"
