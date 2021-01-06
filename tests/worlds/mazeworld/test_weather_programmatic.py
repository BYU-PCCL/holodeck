import pytest
from _pytest.fixtures import FixtureRequest
from holodeck import HolodeckException
from holodeck.environments import HolodeckEnvironment

from tests.utils.captures import compare_rgb_sensor_data_with_baseline
from tests.worlds.mazeworld.conftest import (
    weather_type_test_data,
    time_test_data,
    day_cycle_test_data,
    fog_density_test_data,
    env_with_config,
    weather_config,
)


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
        weather_type: Type of weather in ["sunny", "cloudy", "rain"]
        max_err: Maximum mean squared error between sensor data and baseline
        weather_env: Environment fixture shared by programmatic tests
        data allowed for test to pass
        request: pytest fixture request information

    """
    weather_env.weather.set_weather(weather_type)
    weather_env.tick(5)
    err = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        "weather_type_{}".format(weather_type),
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
        max_err: Maximum mean squared error between sensor data and baseline
        weather_env: Environment fixture shared by programmatic tests
        data allowed for test to pass
        request: pytest fixture request information

    """
    weather_env.weather.set_day_time(hour)
    weather_env.tick(5)
    err = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        "weather_time_{}".format(hour),
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
        cycle_length: The hour in 24-hour format: [0, 23].
        ticks : Number of ticks between captures
        max_err_before: Maximum mean squared error between sensor data and
        baseline for `before` image
        max_err_before: Maximum mean squared error between sensor data and
        baseline for `after` image
        weather_env: Environment fixture shared by programmatic tests
        data allowed for test to pass
        request: pytest fixture request information

    """
    weather_env.tick(5)
    weather_env.weather.start_day_cycle(cycle_length)
    err_before = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        "weather_time_before_{}".format(cycle_length),
    )

    weather_env.tick(ticks)

    err_after = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        "weather_time_after_{}".format(cycle_length),
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
        fog_density: Density of fog in interval [0, 1]
        max_err: Maximum mean squared error between sensor data and baseline
        weather_env: Environment fixture shared by programmatic tests
        data allowed for test to pass
        request: pytest fixture request information

    """
    weather_env.weather.set_fog_density(fog_density)
    weather_env.tick(5)
    err = compare_rgb_sensor_data_with_baseline(
        weather_env.tick()["TestCamera"],
        request.fspath.dirname,
        "weather_fog_density_{}".format(fog_density),
    )

    assert err < max_err


def test_fail_incorrect_weather_type_programmatic(weather_env: HolodeckEnvironment):
    """
    Validate that an exception is thrown when an invalid weather type is
    specified programmatically

    Args:
        weather_env: Environment fixture shared by programmatic tests
    """

    with pytest.raises(HolodeckException):
        # Hail is not a valid weather type--this is on purpose
        weather_env.weather.set_weather("hail")


# TODO(vinhowe): If someone knows of a better way to scope a fixture to a
#  parameterized test, please let me know or use it here
cur_programmatic_weather_env = None
last_programmatic_test_name = None


@pytest.fixture(scope="package", autouse=True)
def env_cleanup():
    global cur_programmatic_weather_env

    yield

    if cur_programmatic_weather_env is not None and hasattr(
        cur_programmatic_weather_env, "_reset_ptr"
    ):
        cur_programmatic_weather_env.__on_exit__()


@pytest.fixture
def weather_env(request: FixtureRequest):
    """Get basic MazeWorld environment with RGBCamera sensor for use in
    visual comparison tests where environments can be reused. Cached per test.

    Args:
        request: pytest fixture request information
    """

    global cur_programmatic_weather_env

    cur_programmatic_test_name = request.function.__name__
    if (
        cur_programmatic_test_name != last_programmatic_test_name
        or cur_programmatic_weather_env is None
    ):
        if cur_programmatic_weather_env is not None and hasattr(
            cur_programmatic_weather_env, "_reset_ptr"
        ):
            cur_programmatic_weather_env.__on_exit__()
        cur_programmatic_weather_env = env_with_config(weather_config)

    return cur_programmatic_weather_env
