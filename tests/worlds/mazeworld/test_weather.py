"""
Test that weather options can be configured both from scenario and
programmatically
"""

import pytest
from _pytest.fixtures import FixtureRequest
from holodeck import HolodeckException
from holodeck.environments import HolodeckEnvironment

from tests.utils.captures import (
    compare_rgb_sensor_data_with_baseline,
    compare_rgb_sensor_data,
)
from tests.worlds.mazeworld.conftest import env_with_config

# TODO: Maybe we should consider creating a config used across the board for
#  visual tests with data from RGBCamera sensor
weather_config = {
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
                    "sensor_name": "TestCamera",
                }
            ],
            "control_scheme": 0,
            "location": [0.95, -1.75, 0.5],
        }
    ],
    "window_width": 1024,
    "window_height": 1024,
}

weather_type_test_data = [
    # weather_type, max_err
    pytest.param("sunny", 1000, id="Sunny"),
    pytest.param("cloudy", 1000, id="Cloudy"),
    pytest.param("rain", 1000, id="Rain"),
]

fog_density_test_data = [
    # fog_depth, max_err
    pytest.param(0, 1000, id="Fog density 0%"),
    pytest.param(1, 1000, id="Fog density 100%"),
]

time_test_data = [
    # hour, max_err
    pytest.param(0, 1000, id="Time 0"),
    pytest.param(12, 1000, id="Time 12"),
    pytest.param(23, 1000, id="Time 23"),
]

day_cycle_test_data = [
    # cycle_length, max_err_before, max_err_after
    pytest.param(1, 500, 1000, 1000, id="1 minute day cycle"),
    pytest.param(5, 500, 1000, 1000, id="5 minute day cycle"),
    pytest.param(30, 500, 1000, 1000, id="30 minute day cycle"),
]


def mean_square_error_before_after_reset(env: HolodeckEnvironment):
    env.tick(5)
    before_data = env.tick()["TestCamera"]

    env.reset()
    env.tick(5)
    after_data = env.tick()["TestCamera"]

    return compare_rgb_sensor_data(before_data, after_data)


@pytest.mark.parametrize("weather_type, max_err", weather_type_test_data)
def test_weather_type_scenario(
    weather_type: str, max_err: float, request: FixtureRequest
) -> None:
    """Validate that weather type is loaded correctly from scenario by
    comparing RGB sensor data with saved baseline
    data

    Args:
        weather_type: type of weather in ["sunny", "cloudy", "rain"]
        max_err: maximum mean squared error between sensor data and baseline
        data allowed for test to pass
        request:

    """
    config = weather_config.copy()
    config["weather"] = {"type": weather_type}

    with env_with_config(config) as env:
        env.tick(5)
        err = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            f"weather_type_{weather_type}",
        )
        assert err < max_err


@pytest.mark.parametrize("fog_density, max_err", fog_density_test_data)
def test_weather_fog_density_scenario(
    fog_density: float, max_err: float, request: FixtureRequest
) -> None:
    """Validate that fog density is loaded correctly from scenario by
    comparing RGB sensor data with saved baseline data
    image

    Args:
        fog_density: density of fog in interval [0, 1]
        max_err: maximum mean squared error between sensor data and baseline
        data allowed for test to pass
        request:

    """
    config = weather_config.copy()
    config["weather"] = {"fog_density": fog_density}

    with env_with_config(config) as env:
        env.tick(5)

        err = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            f"weather_fog_density_{fog_density}",
        )
        assert err < max_err


@pytest.mark.parametrize(
    "cycle_length, ticks, max_err_before, max_err_after", day_cycle_test_data
)
def test_weather_day_cycle_scenario(
    cycle_length: float,
    ticks: int,
    max_err_before: float,
    max_err_after: float,
    request: FixtureRequest,
) -> None:
    """Verify that day cycle can be set with scenario by comparing RGB sensor
    data with saved baseline data

    Args:
        cycle_length (:obj:`float`): The hour in 24-hour format: [0, 23].
        ticks (:obj:`int`): number of ticks between captures
        max_err_before: maximum mean squared error between sensor data and
        baseline for `before` image
        max_err_before: maximum mean squared error between sensor data and
        baseline for `after` image
        data allowed for test to pass
        request:

    """
    config = weather_config.copy()
    config["weather"] = {"day_cycle_length": cycle_length}

    with env_with_config(config) as env:
        env.tick(5)
        err_before = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            f"weather_time_before_{cycle_length}",
        )

        env.tick(ticks)

        err_after = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            f"weather_time_after_{cycle_length}",
        )

        assert err_before < max_err_before
        assert err_after < max_err_after


@pytest.mark.parametrize("hour, max_err", time_test_data)
def test_weather_time_scenario(
    hour: float, max_err: float, request: FixtureRequest
) -> None:
    """Validate that time can be set with scenario by comparing RGB sensor
    data with saved baseline data

    Args:
        hour (:obj:`float`): The hour in 24-hour format: [0, 23].
        max_err (:obj:`float`): maximum mean squared error between sensor
        data and baseline
        request:

    """
    config = weather_config.copy()
    config["weather"] = {"hour": hour}

    with env_with_config(config) as env:
        env.tick(5)
        # TODO(vinhowe): Update time baseline images after
        #  BYU-PCCL/holodeck-engine#205 is wrapped into release
        # write_image_from_rgb_sensor_data(env.tick()["TestCamera"],
        #                                  request.fspath.dirname,
        #                                  f"weather_time_{hour}")
        err = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            f"weather_time_{hour}",
            show_images=True
        )
        assert err < max_err


def test_fail_incorrect_weather_type_scenario():
    """
    Validate that an exception is thrown when an invalid weather type is
    specified in scenario
    """

    # Hail is not a valid weather type--this is on purpose
    config = weather_config.copy()
    config["weather"] = {"type": "hail"}

    with pytest.raises(HolodeckException):
        env_with_config(config)


@pytest.mark.parametrize("weather_type, max_err", weather_type_test_data)
def test_weather_type_persists_after_reset_scenario(
    weather_type: str, max_err: float,
):
    """
    Validate that weather type set in scenario persists after an environment
    reset
    """

    config = weather_config.copy()
    config["weather"] = {"type": weather_type}

    err = mean_square_error_before_after_reset(env_with_config(config))

    assert err < max_err


@pytest.mark.parametrize("fog_density, max_err", fog_density_test_data)
def test_weather_fog_density_persists_after_reset_scenario(
    fog_density: float, max_err: float,
):
    """
    Validate that fog density set in scenario persists after an environment
    reset
    """

    config = weather_config.copy()
    config["weather"] = {"fog_density": fog_density}

    err = mean_square_error_before_after_reset(env_with_config(config))

    assert err < max_err


@pytest.mark.parametrize("hour, max_err", time_test_data)
def test_weather_time_persists_after_reset_scenario(
    hour: int, max_err: float,
):
    """
    Validate that time set in scenario persists after an environment
    reset
    """

    config = weather_config.copy()
    config["weather"] = {"hour": hour}

    err = mean_square_error_before_after_reset(env_with_config(config))

    assert err < max_err


@pytest.mark.parametrize("weather_type, max_err", weather_type_test_data)
def test_weather_type_programmatic(
    weather_type: str,
    max_err: float,
    weather_env: HolodeckEnvironment,
    request: FixtureRequest,
) -> None:
    """Validate that weather type can be set programmatically by comparing
    RGB sensor data with saved baseline data

    Args:
        weather_type: type of weather in ["sunny", "cloudy", "rain"]
        max_err: maximum mean squared error between sensor data and baseline
        weather_env: environment fixture shared by programmatic tests
        data allowed for test to pass
        request:

    """
    weather_env.weather.set_weather(weather_type)
    weather_env.tick(5)
    err = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        f"weather_type_{weather_type}",
    )
    assert err < max_err


@pytest.mark.parametrize("hour, max_err", time_test_data)
def test_weather_time_programmatic(
    hour: float,
    max_err: float,
    weather_env: HolodeckEnvironment,
    request: FixtureRequest,
) -> None:
    """Validate that time can be set programmatically by comparing RGB
    sensor data with saved baseline data

    Args:
        hour (:obj:`float`): The hour in 24-hour format: [0, 23].
        max_err: maximum mean squared error between sensor data and baseline
        weather_env: environment fixture shared by programmatic tests
        data allowed for test to pass
        request:

    """
    weather_env.weather.set_day_time(hour)
    weather_env.tick(5)
    err = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        f"weather_time_{hour}",
    )

    assert err < max_err


@pytest.mark.parametrize(
    "cycle_length, ticks, max_err_before, max_err_after", day_cycle_test_data
)
def test_weather_day_cycle_programmatic(
    cycle_length: float,
    ticks: int,
    max_err_before: float,
    max_err_after: float,
    weather_env: HolodeckEnvironment,
    request: FixtureRequest,
) -> None:
    """Verify that day cycle can be started programmatically by comparing RGB
    sensor data with saved baseline data

    Args:
        cycle_length (:obj:`float`): The hour in 24-hour format: [0, 23].
        ticks (:obj:`int`): number of ticks between captures
        max_err_before: maximum mean squared error between sensor data and
        baseline for `before` image
        max_err_before: maximum mean squared error between sensor data and
        baseline for `after` image
        weather_env: environment fixture shared by programmatic tests
        data allowed for test to pass
        request:

    """
    weather_env.tick(5)
    weather_env.weather.start_day_cycle(cycle_length)
    err_before = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        f"weather_time_before_{cycle_length}",
    )

    weather_env.tick(ticks)

    err_after = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        f"weather_time_after_{cycle_length}",
    )

    assert err_before < max_err_before
    assert err_after < max_err_after


@pytest.mark.parametrize("fog_density, max_err", fog_density_test_data)
def test_weather_fog_density_programmatic(
    fog_density: float,
    max_err: float,
    weather_env: HolodeckEnvironment,
    request: FixtureRequest,
) -> None:
    """Validate that fog density can be set programmatically by comparing RGB
    sensor data with saved baseline data

    Args:
        fog_density: density of fog in interval [0, 1]
        max_err: maximum mean squared error between sensor data and baseline
        weather_env: environment fixture shared by programmatic tests
        data allowed for test to pass
        request:

    """
    weather_env.weather.set_fog_density(fog_density)
    weather_env.tick(5)
    err = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        f"weather_fog_density_{fog_density}",
    )

    assert err < max_err


def test_fail_incorrect_weather_type_programmatic(
    weather_env: HolodeckEnvironment,
):
    """
    Validate that an exception is thrown when an invalid weather type is
    specified programmatically

    Args:
        weather_env: environment fixture shared by programmatic tests
    """

    with pytest.raises(HolodeckException):
        # Hail is not a valid weather type--this is on purpose
        weather_env.weather.set_weather("hail")


# TODO(vinhowe): If someone knows of a better way to scope a fixture to a
#  parameterized test, please let me know or use it here
cur_programmatic_weather_env = None
last_programmatic_test_name = None


@pytest.fixture
def weather_env(request: FixtureRequest):
    """Get basic MazeWorld environment with RGBCamera sensor for use in
    visual comparison tests where environments can be reused. Cached per test.
    """

    global cur_programmatic_weather_env

    cur_programmatic_test_name = request.function.__name__
    if (
        cur_programmatic_test_name != last_programmatic_test_name
        or cur_programmatic_weather_env is None
    ):
        cur_programmatic_weather_env = env_with_config(weather_config)

    return cur_programmatic_weather_env
