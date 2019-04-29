# Holodeck Packages and Configuration
How packages are installed, managed, and interpreted in holodeck.

## Package Installation

Packages are located on an S3 bucket, due to the size of the files and the 
bandwidth required to distribute them. 

### Retrieving Package List
A version of holodeck has a certain set of packages that are associated with it. 
Each package can have multiple versions, and a version of holodeck can be 
compatible with multiple versions of a package. A package can also be added
after shipping a version of holodeck, so the client fetches a list of available
packages from the backend.

The client will post a GET to the following endpoint:
`%BACKEND%/packages/%HOLODECK_VERSION%/available`, or
`https://s3.amazonaws.com/holodeckworlds/packages/0.2.0/available` for example.

The server will return a JSON file with the following format:

```json
{
    "packages": {
        "%WORLD_NAME%" : ["%VERSION1", "%VERSION_2%"]
    }
}
```

for example

```json
{
    "packages": {
        "DefaultWorlds" : ["0.1.0", "0.1.1"],
        "MoveBox" : ["0.0.1"]
    }
}
```

The client will use this information to craft the download URL.

### Download URL

This is the format of a download URL:

`%BACKEND%/packages/%HOLODECK_VERSION%/%PACKAGE_NAME%/%PLATFORM%/%PACKAGE_VERSION%.zip`

for example

`%BACKEND%/packages/0.1.0/DefaultWorlds/Linux/1.0.2.zip`

### Installation Location

Packages are saved in a holodeck version dependent subfolder. So for holodeck 
version `0.2.0`, all worlds will be saved in
`%HOLODECKPATH%/%HOLODECK_VERSION%/worlds`

This will prevent holodeck from loading binaries from the wrong version, and 
will also allow multiple versions of holodeck to be installed at once.

A package may have multiple versions, but only one version of a package must 
be installed at a given time. This is because world names are assumed to be
unique between all installed packages currently, so having two versions of 
the package would cause issues.

## Package Config File Format

Each package has a `config.json` file located in the root of the archive. This 
configuration file defines the worlds that are in that package, and defines the
 agents in the world if it doesn't use dynamic spawning.

### `config.json`
```json
{  
    "name":"{package_name}",
    "platform":"{Linux | Windows}",
    "version":"{package_version}",
    "path" : "{path to binary within the archive}",
    "maps": [  
        "{map-objects}",
    ]
}
```

### `map` object
The `map` object defines the maps that are available in a package. 

Here is an example of a complete map object

```json
{  
    "name": "{map_name}",
    "pre_start_steps": 2,
    "default_scenario": "{name of default scenario - eg Follow}"
}
```

## Scenario Config File Format

A map may have several different scenarios associated with it. The filename of 
a scenario file distributed in a package must be `%WORLD_NAME%-%SCENARIO_NAME%.json`, 
for example `UrbanCity-Follow.json`. The scenario defines the agents and tasks
 that should be spawned in the world when an object is created.

Here is the file format for a scenario:

```json
{
    "name": "{Scenario Name}",
    "world": "{Map it is associated with}",

    "agents":[
        "array of agent objects"
    ],

    "window_width":  1280,
    "window_height": 720
}
```
The first agent defined in the `agents` array is the main agent.

All coordinates are right handed.
### Agent Object
For use with a scenario file only.

```json

{
    "agent_name": "uav0",
    "agent_type": "{agent types}",
    "sensors": [
        "array of sensor objects"
    ],
    "control_scheme": "{control scheme type}",
    "location": [1.0, 2.0, 3.0],
    "rotation": [1.0, 2.0, 3.0]
}
```

#### Agent Types
 - `UavAgent`
 - `SphereAgent`
 - `AndroidAgent`
 - `NavAgent`
 - `TurtleAgent`
 - `BoatAgent`

#### Control Schemes
Depends on the agent type

| Agent Type | Scheme                        |
|-----------:|-------------------------------|
| Android    | `android_torques`             |
| Sphere     | `sphere_discrete`             |
| Sphere     | `sphere_continuous`           |
| Nav Agent  | `nav_target_location`         |
| UAV        | `uav_torques`                 |
| UAV        | `uav_roll_pitch_yaw_rate_alt` |

### Sensor Object
All coordinates are right handed. Note that the coordinates are 

```json
{
    "sensor_type": "RGBCamera",
    "sensor_name": "FrontCamera",
    "location": [1.0, 2.0, 3.0],
    "rotation": [1.0, 2.0, 3.0],
    "socket": "socket name or """,
    "configuration": {
        "note": "Each sensor has a different configuration. This object is passed in verbatim to the C++ sensor object"
    }
}
```