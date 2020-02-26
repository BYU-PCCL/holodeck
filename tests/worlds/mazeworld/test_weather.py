"""
Test that weather options can be configured both from scenario and programmatically
"""
import os
import uuid
from typing import List, Tuple

import pytest
from _pytest.fixtures import FixtureRequest
from cv2 import cv2
from holodeck import packagemanager as pm, HolodeckException
from holodeck.environments import HolodeckEnvironment

from tests.utils.captures import display_multiple
from tests.utils.equality import mean_square_err

weather_type_test_data = [
    # weather_type, max_err
    pytest.param("sunny", 100, id="Sunny"),
    pytest.param("cloudy", 100, id="Cloudy"),
    pytest.param("rain", 100, id="Rain"),
]

fog_test_data = [
    # fog_depth, max_err
    pytest.param(1, 100, id="Fog density 100%"),
    pytest.param(0, 100, id="Fog density 0%"),
]

config = {
    "name": "test_weather_config",
    "world": "MazeWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "RGBCamera",
                    "socket": "CameraSocket",
                    "sensor_name": "TestCamera"
                }
            ],
            "control_scheme": 0,
            "location": [.95, -1.75, .5]
        }
    ],
    "window_width": 1024,
    "window_height": 1024
}


def env_with_config(config):
    binary_path = pm.get_binary_path_for_package("DefaultWorlds")
    return HolodeckEnvironment(scenario=config,
                               binary_path=binary_path,
                               show_viewport=False,
                               uuid=str(uuid.uuid4()))


def cv2_show_images(images: List[Tuple[str, List]]):
    """
    Show list of images in OpenCV image windows when debugging
    """
    for image in images:
        cv2.imshow(image[0], image[1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def compare_rgb_with_baseline(sensor_data, base_path, baseline_name, show_images=False) -> float:
    """
    Compare data from RGB sensor with baseline file in `expected` folder and return mean squared error
    """
    pixels = sensor_data[:, :, 0:3]
    baseline = cv2.imread(os.path.join(base_path, "expected", f"{baseline_name}.png"))
    if show_images:
        # Show images when debugging--this will block tests until user input is provided
        display_multiple([(pixels, "pixels"), (baseline, "baseline")])
    return mean_square_err(pixels, baseline)


@pytest.mark.parametrize("weather_type, max_err", weather_type_test_data)
def test_weather_type_scenario(weather_type: str, max_err: float, request: FixtureRequest) -> None:
    current_config = config.copy()
    current_config["weather"] = {"type": weather_type}

    with env_with_config(current_config) as env:
        for _ in range(5):
            env.tick()
        err = compare_rgb_with_baseline(env.tick()["TestCamera"], request.fspath.dirname,
                                        f"weather_type_{weather_type}")
        assert err < max_err


@pytest.mark.parametrize("fog_density, max_err", fog_test_data)
def test_weather_fog_scenario(fog_density: float, max_err: float, request: FixtureRequest) -> None:
    current_config = config.copy()
    current_config["weather"] = {"fog_density": fog_density}

    with env_with_config(current_config) as env:
        for _ in range(5):
            env.tick()

        err = compare_rgb_with_baseline(env.tick()["TestCamera"], request.fspath.dirname,
                                        f"weather_fog_density_{fog_density}")
        assert err < max_err


@pytest.mark.parametrize("weather_type, max_err", weather_type_test_data)
def test_weather_type_programmatic(weather_type: str, max_err: float, request: FixtureRequest) -> None:
    with env_with_config(config) as env:
        env.weather.set_weather(weather_type)
        for _ in range(5):
            env.tick()
        err = compare_rgb_with_baseline(env.tick()["TestCamera"], request.fspath.dirname,
                                        f"weather_type_{weather_type}")
        assert err < max_err


def test_fail_incorrect_weather_type():
    binary_path = pm.get_binary_path_for_package("DefaultWorlds")

    # Hail is not a valid weather type--this is on purpose
    config["weather"] = {"type": "hail"}

    with pytest.raises(HolodeckException):
        HolodeckEnvironment(scenario=config,
                            binary_path=binary_path,
                            show_viewport=False,
                            uuid=str(uuid.uuid4()))
