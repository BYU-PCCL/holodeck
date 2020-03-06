from holodeck.environments import HolodeckEnvironment

from tests.scenarios.conftest import scenario_test


def test_weather_type_scenario(scenario: str) -> None:
    """Test that weather can be set correctly in a scenario without errors

    Args:
        scenario (str): Scenario to test

    """

    def set_weather_type_action(env: HolodeckEnvironment, weather_type: str):
        env.weather.set_weather(weather_type)

    weather_types = ["sunny", "cloudy", "rain"]

    scenario_test(scenario, set_weather_type_action, weather_types)


def test_weather_fog_scenario(scenario: str) -> None:
    """Test that fog can be set correctly in a scenario without errors

    Args:
        scenario (str): Scenario to test

    """

    def set_weather_fog_action(env: HolodeckEnvironment, fog_density: int):
        env.weather.set_fog_density(fog_density)

    fog_densities = [1, 0]

    scenario_test(scenario, set_weather_fog_action, fog_densities)


def test_weather_day_cycle_scenario(scenario: str) -> None:
    """Test that day cycle can be started correctly in a scenario without
    errors

    Args:
        scenario (str): Scenario to test

    """

    def set_weather_day_cycle_action(
        env: HolodeckEnvironment, day_length: int
    ):
        if day_length == 0:
            env.weather.stop_day_cycle()
        else:
            env.weather.start_day_cycle(day_length)

    day_length = [10, 1, 0]

    scenario_test(scenario, set_weather_day_cycle_action, day_length)
