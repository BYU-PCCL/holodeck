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
from tests.worlds.mazeworld.conftest import (
    env_with_config,
    weather_type_test_data,
    weather_config, fog_density_test_data, day_cycle_test_data, time_test_data)


def mean_square_error_before_after_reset(env: HolodeckEnvironment):
    """

    Args:
        env: Environment to reset and test on

    Returns: mean squared error between RGB sensor data capture before and
    after and environment reset

    """
    env.tick(10)
    before_data = env.tick()["TestCamera"]

    env.reset()
    env.tick(10)
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
        weather_type: Type of weather in ["sunny", "cloudy", "rain"]
        max_err: Maximum mean squared error between sensor data and baseline
        data allowed for test to pass
        request: pytest fixture request information

    """
    config = weather_config.copy()
    config["weather"] = {"type": weather_type}

    with env_with_config(config) as env:
        env.tick(5)
        err = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            "weather_type_{}".format(weather_type),
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
        fog_density: Density of fog in interval [0, 1]
        max_err: Maximum mean squared error between sensor data and baseline
        data allowed for test to pass
        request: pytest fixture request information

    """
    config = weather_config.copy()
    config["weather"] = {"fog_density": fog_density}

    with env_with_config(config) as env:
        env.tick(5)

        err = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            "weather_fog_density_{}".format(fog_density),
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
        cycle_length: The hour in 24-hour format: [0, 23].
        ticks: Number of ticks between captures
        max_err_before: Maximum mean squared error between sensor data and
        baseline for `before` image
        max_err_before: Maximum mean squared error between sensor data and
        baseline for `after` image
        data allowed for test to pass
        request: pytest fixture request information

    """
    config = weather_config.copy()
    config["weather"] = {"day_cycle_length": cycle_length}

    with env_with_config(config) as env:
        env.tick(5)
        err_before = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            "weather_time_before_{}".format(cycle_length),
        )

        env.tick(ticks)

        err_after = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            "weather_time_after_{}".format(cycle_length),
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
        hour: The hour in 24-hour format: [0, 23].
        max_err: Maximum mean squared error between sensor
        data and baseline
        request: pytest fixture request information

    """
    config = weather_config.copy()
    config["weather"] = {"hour": hour}

    with env_with_config(config) as env:
        env.tick(5)
        err = compare_rgb_sensor_data_with_baseline(
            env.tick()["TestCamera"],
            request.fspath.dirname,
            "weather_time_{}".format(hour),
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

    Args:
        weather_type: Type of weather in ["sunny", "cloudy", "rain"]
        max_err: Maximum mean squared error between sensor data and baseline
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

    Args:
        fog_density: Density of fog in interval [0, 1]
        max_err: Maximum mean squared error between sensor data and baseline
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

    Args:
        hour: The hour in 24-hour format: [0, 23].
        max_err: Maximum mean squared error between sensor data and baseline
    """

    config = weather_config.copy()
    config["weather"] = {"hour": hour}

    err = mean_square_error_before_after_reset(env_with_config(config))

    assert err < max_err
