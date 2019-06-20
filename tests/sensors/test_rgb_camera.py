import holodeck
import cv2
import copy
import numpy as np
import os
import uuid


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
                    "socket": "CameraSocket"
                }
            ],
            "control_scheme": 0,
            "location": [.95, -1.75, .5]
        }
    ]
}


def mse(im1, im2):
    """Compute the mean square error of the two images

    Args:
        im1 (np array):
        im2 (np array):

    Returns: integer, lower is more similar

    """
    err = np.sum((im1.astype("float") - im2.astype("float")) ** 2)
    err /= float(im1.shape[0] * im1.shape[1])
    return err


def test_rgb_camera(resolution, request):
    """Makes sure that the RGB camera is positioned and capturing correctly.

    Capture pixel data, and load from disk the baseline of what it should look like.
    Then, use mse() to see how different the images are.

    """
    global base_cfg

    cfg = copy.deepcopy(base_cfg)

    cfg["agents"][0]["sensors"][0]["configuration"] = {
        "CaptureWidth": resolution,
        "CaptureHeight": resolution
    }

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=cfg,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        for _ in range(5):
            env.tick()

        pixels = env.tick()['RGBCamera'][:, :, 0:3]
        baseline = cv2.imread(os.path.join(request.fspath.dirname, "expected", "{}.png".format(resolution)))
        err = mse(pixels, baseline)

        assert err < 2000

