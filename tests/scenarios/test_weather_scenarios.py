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
