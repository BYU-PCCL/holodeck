agent_definition_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://https://holodeck.cs.byu.edu/schemas/agent_schema.json",
    "type": "object",
    "title": "The Agent Schema",
    "required": [
        "agent_name",
        "agent_type",
        "sensors",
        "control_scheme",
        "location"
    ],
    "properties": {
        "agent_name": {
            "type": "string",
            "description": "The name of the agent. Must be unique within the scenario",
            "default": "",
            "examples": [
                "sphere0"
            ]
        },
        "agent_type": {
            "type": "string",
            "description": "The agent type. Must be a valid Holodeck agent",
            "default": "",
            "examples": [
                "SphereAgent", "AndroidAgent", "TurtleAgent", "UavAgent", "HandAgent", "NavAgent"
            ],
        },
        "sensors": {
            "type": "array",
            "description": "An array of sensor definition objects",
            "items": {
                "type": "object",
                "description": "Sensor specification",
                "required": [
                    "sensor_type"
                ],
                "properties": {
                    "sensor_type": {
                        "type": "string",
                        "description": "The name of the sensor. Must be a sensor for the agent",
                        "default": "",
                        "examples": [
                            "LocationSensor"
                        ]
                    }
                }
            }
        },
        "control_scheme": {
            "type": "integer",
            "description": "The control scheme to be used to control the agent.",
            "default": 0,
            "examples": [0, 1]
        },
        "location": {
            "type": "array",
            "description": "The initial location in the world to create the agent",
            "items": {
                "type": "number"
            },
            "title": "The X, Y and Z location coordinates",
            "default": [0.0, 0.0, 0.0],
            "examples": [[0.95, -1.75, 0.5]]
        },
        "rotation": {
            "type": "array",
            "description": "The initial rotation of the agent",
            "items": {
                "type": "number",
                "title": "The Items Schema",
                "default": 0,
                "examples": [1, 2, 3]
            },
            "default": [0.0, 0.0, 0.0],
            "examples": [[0.95, -1.75, 0.5]]
        },
        "location_randomization": {
            "type": "array",
            "title": "Specifies the X, Y, and Z variance to use to randomize the agent's initial location",
            "items": {
                "type": "number",
                "default": 0.0,
                "examples": [0.6, 0.5, 0.5]
            },
            "default": [0.0, 0.0, 0.0],
            "examples": [[0.95, -1.75, 0.5]]
        },
        "rotation_randomization": {
            "type": "array",
            "title": "Specifies the yaw, pitch and roll variance to use to randomize the agent's initial rotation",
            "items": {
                "type": "number",
                "default": 0.0,
                "examples": [0.4, 0.3, 0.6]
            }
        }
    }
}

scenario_config_schema = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://https://holodeck.cs.byu.edu/schemas/scenario_config_schema.json",
    "type": "object",
    "title": "The configuration file schema to create a Holodeck scenario",
    "required": [
        "name",
        "world",
        "main_agent",
        "agents",
    ],
    "properties": {
        "name": {
            "type": "string",
            "title": "The name of the scenario",
            "default": "",
            "examples": [
                "test_scenario"
            ]
        },
        "world": {
            "type": "string",
            "title": "The world to use in the scenario",
            "default": "",
            "examples": [
                "TestWorld", "CyberPunkCity", "EuropeanForest", "UrbanCity"
            ]
        },
        "main_agent": {
            "type": "string",
            "title": "The name of the main agent. The agent must be in the agents list",
            "default": "",
            "examples": [
                "sphere0"
            ]
        },
        "agents": {
            "type": "array",
            "description": "Holodeck agents",
            "items": agent_definition_schema,
            "window_width": {
                "type": "integer",
                "description": "The window width",
                "examples": [1024]
            },
            "window_height": {
                "type": "integer",
                "title": "The window width",
                "examples": [1024]
            }
        }
    }
}
