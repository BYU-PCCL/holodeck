import cv2
import os
from tests.utils.equality import mean_square_err


def test_sensor_rotation(rotation_env, request):
    """Validates that calling rotate actually rotates the sensor using the RGBCamera.

    Positions the SphereAgent above the target cube so that if it rotates down, it will
    capture the test pattern.
    """
    # Re-use the screenshot for test_rgb_camera
    rotation_env.agents["sphere0"].sensors["RGBCamera"].rotate([0, 0, 0])
    pixels = rotation_env.tick(10)["RGBCamera"][:, :, 0:3]

    baseline = cv2.imread(os.path.join(request.fspath.dirname, "expected", "256.png"))

    err = mean_square_err(pixels, baseline)
    assert err < 2000, "The sensor appeared to not rotate!"


def test_sensor_rotation_resets_after_reset(rotation_env):
    """Validates that the sensor rotation is reset back to the starting position after
    calling ``.reset()``.
    """

    # Re-use the screenshot for test_rgb_camera
    rotation_env.agents["sphere0"].sensors["RGBCamera"].rotate([0, 0, 0])
    pixels_before = rotation_env.tick(5)["RGBCamera"][:, :, 0:3]

    rotation_env.reset()

    pixels_after = rotation_env.tick(5)["RGBCamera"][:, :, 0:3]

    err = mean_square_err(pixels_before, pixels_after)
    assert err > 2000, "The images were too similar! Did the sensor not rotate back?"
