Changelog
=========

.. Changelog Style Guide
  - Each release should have a New Features / Changes / Bug Fixes section.
  - Keep the first sentence of each point short and descriptive
  - The passive voice should be avoided
  - Try to make the first word a verb in past tense. Bug fixes should use
    "Fixed"
  - Add a link to the issue describing the change or the pull request that
    merged it at the end in parentheses
  - see https://github.com/BYU-PCCL/holodeck/wiki/Holodeck-Release-Notes-Template

Holodeck 0.3.2
--------------
*03/25/2021*

More bug fixes, improvements, and even a few new features.

Highlights
~~~~~~~~~~

New Features
~~~~~~~~~~~~
- Added a 'max tick' functionality that will exit out of the environment after
  a designated number of ticks has occurred.
  (`#325 <https://github.com/BYU-PCCL/holodeck/issues/325>`_)

Changes
~~~~~~~

Bug Fixes
~~~~~~~~~
- Fixed Command.add_number_parameters silently failing if given numpy array (`#427 <https://github.com/BYU-PCCL/holodeck/issues/427>`_)

Holodeck 0.3.1
--------------
*04/02/2020*

More bug fixes, improvements, and even a few new features.

Highlights
~~~~~~~~~~
- **Holodeck now requires Python 3.5 or greater**
- Added :class:`~holodeck.sensors.AbuseSensor` and 
  :class:`~holodeck.sensors.RangeFinderSensor`
- Added programmatic spawning of props, see
  :meth:`~holodeck.environments.HolodeckEnvironment.spawn_prop`
- Weather can be specified in scenarios, see :ref:`weather`.

New Features
~~~~~~~~~~~~
- Added optional start location and rotation randomization on 
  :meth:`~holodeck.environments.HolodeckEnvironment.reset`. See 
  :ref:`location-randomization`.
  (`#295 <https://github.com/BYU-PCCL/holodeck/issues/295>`_)
- :meth:`~holodeck.environments.HolodeckEnvironment.spawn_prop` now allows 
  basic objects (spheres, cubes, cylinders) to be spawned at arbitrary 
  locations in the environment.
  (`#397 <https://github.com/BYU-PCCL/holodeck/issues/397>`_)
- :ref:`distance-task` by default now calculates the distance to the objective
  along the XY plane, to discourage flying straight up.
  (`#360 <https://github.com/BYU-PCCL/holodeck/issues/360>`_)

  If the full 3D distance is desired, set the ``3dDistance`` flag in the
  configuration block of the :ref:`distance-task`.
  (`#360 <https://github.com/BYU-PCCL/holodeck/issues/360>`_)
- Added :class:`~holodeck.sensors.AbuseSensor`, which senses if an agent
  has been abused. Agents experience abuse when they fall from a high distance
  or other agent-specific situations.
  (`#262 <https://github.com/BYU-PCCL/holodeck/issues/262>`_)
- Environment weather/time can be optionally configured with :ref:`scenarios`
  (`#263 <https://github.com/BYU-PCCL/holodeck/issues/263>`_). See
  :ref:`weather`.
- :meth:`~holodeck.weather.WeatherController.set_weather` now has sunny
  weather available, which allows you to revert back to the default weather.
  (`#376 <https://github.com/BYU-PCCL/holodeck/issues/376>`_)
- Added :class:`~holodeck.sensors.RangeFinderSensor` which calculates the
  distance from the sensor to the first collision in the environment. The 
  sensor can send out multiple rays in a circle if desired.
- Added a 'max tick' function that will exit out of the environment after
  a designated number of ticks has occurred.
  (`#325 <https://github.com/BYU-PCCL/holodeck/issues/325>`_)

Changes
~~~~~~~

- **Holodeck now requires Python >= 3.5**
  (`#389 <https://github.com/BYU-PCCL/holodeck/issues/389>`_)
- Moved weather/time methods from
  :class:`~holodeck.environments.HolodeckEnvironment` to new
  :class:`~holodeck.weather.WeatherController`
  (`#196 <https://github.com/BYU-PCCL/holodeck/issues/196>`_,
  `#263 <https://github.com/BYU-PCCL/holodeck/issues/263>`_)
- Calling :meth:`~holodeck.environments.HolodeckEnvironment.send_world_command`
  for an environment without the given command will now cause
  the environment to exit rather than fail silently.
  This includes all relevant methods in the
  :class:`~holodeck.weather.WeatherController`.
- Removed the ability to toggle sensors during runtime with the removal of
  :class:`~holodeck.environments.command.SetSensorEnabledCommand`,
  :meth:`~holodeck.environments.HolodeckEnvironment.set_sensor_enabled`, and
  :meth:`~holodeck.sensors.HolodeckSensor.set_sensor_enable`.
  To specify which sensors to include, use :ref:`custom-scenarios`.
  (`#268 <https://github.com/BYU-PCCL/holodeck/issues/268>`_)
- Improved Docker images. See :ref:`docker`.
  (`#347 <https://github.com/BYU-PCCL/holodeck/issues/347>`_)
  
  - Tests can now be run inside of Docker containers
  - All images are based on Ubuntu 18.04 now
  - Added image for Dexterity package, and an image with every package
- Every control scheme now has limits on inputs (ie maximum or minimum thrust)
  (`#369 <https://github.com/BYU-PCCL/holodeck/issues/369>`_)

  See :meth:`~holodeck.spaces.ActionSpace.get_high` and 
  :meth:`~holodeck.spaces.ActionSpace.get_low` to read them.
- Scenario Changes:

  - **EuropeanForest-MaxDistance, RedwoodForest-MaxDistance,**
    **UrbanCity-MaxDistance:** Added :class:`~holodeck.sensors.AbuseSensor`
  - **InfiniteForest-MaxDistance:** Added :class:`~holodeck.sensors.AbuseSensor` 
    and :class:`~holodeck.sensors.RangeFinderSensor`.
  - **MazeWorld-FinishMazeSphere:** Added 
    :class:`~holodeck.sensors.RangeFinderSensor`


Bug Fixes
~~~~~~~~~
- Fixed UAV blades rotating incorrectly (thanks @sethmnielsen!)
  (`#331 <https://github.com/BYU-PCCL/holodeck/issues/331>`_)
- Fixed some ``posix_ipc.BusyError: Semaphore is busy`` errors on Linux systems 
  when creating a scenario
  (`#285 <https://github.com/BYU-PCCL/holodeck/issues/285>`_)
- Fixed a bug where the UE4 editor crashes when an agent is manually added
  to a level
  (`#361 <https://github.com/BYU-PCCL/holodeck/issues/361>`_)
- Fixed crash when manually disabling viewport when it would've been disabled 
  anyway.
  (`#378 <https://github.com/BYU-PCCL/holodeck/issues/378>`_)
- Fixed SphereAgent having the incorrect default control scheme
  (`#350 <https://github.com/BYU-PCCL/holodeck/issues/350>`_)
  
Holodeck 0.3.0
--------------
*11/02/2019*

This is a content release focused on improving the :ref:`android-agent` and
adding more scenarios and tasks for it. We also added a new floating hand
agent to provide a simpler agent that can do many of the dexterity tasks.

Highlights
~~~~~~~~~~
- Added :ref:`dexterity-package` with new worlds and scenarios (see below for
  comprehensive listing)
- Added :ref:`clean-up-task` and :ref:`cup-game-task` tasks
- Added :ref:`hand-agent`

New Features
~~~~~~~~~~~~
- Added the :ref:`dexterity-package` with new worlds and scenarios:

  - :ref:`playroom-world`

    - :ref:`playroom-android`
    - :ref:`playroom-hand`
    - :ref:`playroom-standfromground`
    - :ref:`playroom-standfromstanding`

  - :ref:`clean-up-world`
    (`#290 <https://github.com/BYU-PCCL/holodeck/issues/290>`_)

    - :ref:`cleanup-groundandroid`
    - :ref:`cleanup-groundhand`
    - :ref:`cleanup-tableandroid`
    - :ref:`cleanup-tablehand`

  - :ref:`cup-game-world`
    (`#288 <https://github.com/BYU-PCCL/holodeck/issues/288>`_)

    - :ref:`cupgame-custom`
    - :ref:`cupgame-easy`
    - :ref:`cupgame-hard`

  - :ref:`grip-world`

    - :ref:`grip-liftbottle`

- Added the :ref:`hand-agent` - a simplified Android hand that can float
  around
  (`#287 <https://github.com/BYU-PCCL/holodeck/issues/287>`_)

  - HandAgent can be used with the same Android-specific sensors (
    :class:`~holodeck.sensors.JointRotationSensor`,
    :class:`~holodeck.sensors.PressureSensor`,
    :class:`~holodeck.sensors.RelativeSkeletalPositionSensor`)

- Added new tasks sensors for specific worlds

  - :ref:`cup-game-task`
    (`#318 <https://github.com/BYU-PCCL/holodeck/pull/318>`_)

  - :ref:`clean-up-task`
    (`#321 <https://github.com/BYU-PCCL/holodeck/pull/321>`_)

- Packages can be installed directly from a URL
  (see :class:`~holodeck.packagemanager.install`)
  (`#129 <https://github.com/BYU-PCCL/holodeck/issues/129>`_)
- Agent sensors can now be rotated at run time with
  :meth:`~holodeck.sensors.HolodeckSensor.rotate`.
  (`#305 <https://github.com/BYU-PCCL/holodeck/issues/305>`_)
- The config files can now specify whether an agent should be spawned
  (`#303 <https://github.com/BYU-PCCL/holodeck/pull/303>`_)
- Pressing ``h`` now shows the coordinates of the agent the viewport is
  following or the coordinates of the camera if it is detached (see
  :ref:`hotkeys`).
  (`#253 <https://github.com/BYU-PCCL/holodeck/issues/253>`_)
- The viewport now follows the main agent as specified in the
  config file by default.
  (`#238 <https://github.com/BYU-PCCL/holodeck/issues/238>`_)
- You can now specify the number of ticks you want to occur in the
  :meth:`~holodeck.environments.HolodeckEnvironment.tick` and the
  :meth:`~holodeck.environments.HolodeckEnvironment.step` methods,
  (`#313 <https://github.com/BYU-PCCL/holodeck/pull/313>`_)

Changes
~~~~~~~
- Increased the :ref:`android-agent`'s strength in the
  ``ANDROID_MAX_SCALED_TORQUES`` control scheme.

  - Previously the AndroidAgent didn't have enough strength to even move its
    legs.
  - Strength was approximately doubled (See
    `JointMaxTorqueControlScheme.h <https://github.com/BYU-PCCL/holodeck-engine/blob/develop/Source/Holodeck/Agents/Public/JointMaxTorqueControlScheme.h#L50>`_
    )
- Location sensor now returns the location of the sensor, not just the agent
  (`#306 <https://github.com/BYU-PCCL/holodeck/issues/306>`_)
- Updated to Unreal Engine 4.22
  (`#241 <https://github.com/BYU-PCCL/holodeck/issues/241>`_)
- :ref:`turtle-agent` is now subject to gravity, has increased power,
  is black, and slightly smaller.
  (`#217 <https://github.com/BYU-PCCL/holodeck/issues/217>`_)
- Removed the ``set_state()`` and ``teleport()`` methods from the
  :class:`~holodeck.environments.HolodeckEnvironment` class.

  These methods were duplicates of the corresponding methods on the
  :class:`~holodeck.agents.HolodeckAgent` class. See the linked issue for
  migration suggestions 👉
  (`#311 <https://github.com/BYU-PCCL/holodeck/issues/311>`_)
- Removed the ``get/set_ticks_per_capture`` methods from the
  :class:`~holodeck.agents.HolodeckAgent` and
  :class:`~holodeck.environments.HolodeckEnvironment` classes, moved
  :meth:`~holodeck.sensors.RGBCamera.set_ticks_per_capture` method to the
  :class:`~holodeck.sensors.RGBCamera` class.
  (`#197 <https://github.com/BYU-PCCL/holodeck/issues/197>`_)
- Viewport will now follow the main agent by default.
  (`#238 <https://github.com/BYU-PCCL/holodeck/issues/238>`_)
- Viewport will not be rendered when it is hidden (``show_viewport`` param in
  :class:`~holodeck.environments.HolodeckEnvironment`, Linux only)
  (`#283 <https://github.com/BYU-PCCL/holodeck/issues/283>`_)

Bug Fixes
~~~~~~~~~
- Fixed the :class:`~holodeck.sensors.RelativeSkeletalPositionSensor`.

  - This sensor returns the location of bones, not sensors. Since there are
    more bones than joints, previously it returned them in a completely
    different order than expected.
  - Now the order for this sensor is explicitly specified in
    :ref:`android-bones` and :ref:`hand-bones`.
  - Previously on the first tick it would return uninitialized garbage on the
    first tick
- Fixed being unable to spawn the :ref:`turtle-agent`.
  (`#308 <https://github.com/BYU-PCCL/holodeck/issues/308>`_)
- Fixed the :meth:`~holodeck.agents.HolodeckAgent.set_physics_state` method.
  (`#311 <https://github.com/BYU-PCCL/holodeck/issues/311>`_)
- Fixed agent spawn rotations being in the incorrect order. Fixed the
  documentation that specified the incorrect order as well (:ref:`rotations`)
  (`#309 <https://github.com/BYU-PCCL/holodeck/issues/309>`_)
- Fixed being unable to set the ticks per capture of a camera if it was not
  named ``RGBCamera``.
  (`#197 <https://github.com/BYU-PCCL/holodeck/issues/197>`_)
- Fixed being unable to make a Holodeck window larger than the current screen
  resolution
  (`#301 <https://github.com/BYU-PCCL/holodeck/issues/301>`_)
- Fixed being unable to configure :class:`~holodeck.sensors.ViewportCapture`
  sensor.
  (`#301 <https://github.com/BYU-PCCL/holodeck/issues/301>`_)

Known Issues
~~~~~~~~~~~~
- The TurtleAgent does not move consistently between Linux and Windows.
  (`#336 <https://github.com/BYU-PCCL/holodeck/issues/336>`_)


Holodeck 0.2.2
--------------
*06/20/2019*

This is mostly a maintenance release focused on cleaning up bugs that were
unresolved in ``0.2.1``


New Features
~~~~~~~~~~~~
- When freecamming around, :ref:`pressing shift <hotkeys>` moves the
  camera faster.
  (`#99 <https://github.com/BYU-PCCL/holodeck/issues/99>`_)
- Agents can have a rotation specified in the scenario config files
  (`#209 <https://github.com/BYU-PCCL/holodeck/issues/209>`_)
- Custom scenarios can be made with dictionaries as well as ``json`` files.
  See :ref:`custom-scenarios`
  (`#275 <https://github.com/BYU-PCCL/holodeck/issues/275>`_)
- Documented how to improve Holodeck performance.
  See :ref:`improving-performance`
  (`#109 <https://github.com/BYU-PCCL/holodeck/issues/109>`_)


Bug Fixes
~~~~~~~~~
- Fixed :meth:`~holodeck.environments.HolodeckEnvironment.info` method
  (`#182 <https://github.com/BYU-PCCL/holodeck/issues/182>`_)
- Fixed command buffer not being reset after calling
  :meth:`~holodeck.environments.HolodeckEnvironment.reset`.
  (`#254 <https://github.com/BYU-PCCL/holodeck/issues/254>`_)
- Fixed rain not being very visible on Linux
  (`#235 <https://github.com/BYU-PCCL/holodeck/issues/235>`_)
- Fixed teleport command not working on the Android
  (`#209 <https://github.com/BYU-PCCL/holodeck/issues/209>`_)
- Fixed RGBCamera intermittently returning a matrix of zeros after resetting
  (`#271 <https://github.com/BYU-PCCL/holodeck/issues/271>`_)
- Fixed ``EXCEPTION_ACCESS_VIOLATION`` on Windows after creating an environment
  (`#270 <https://github.com/BYU-PCCL/holodeck/issues/270>`_)
- Fixed :ref:`MazeWorld-FinishMazeSphere` task not going terminal when task
  was finished.

  - Added a post with a golden ball on top to the end of the maze,
    this is now the tasks's target

Holodeck 0.2.1
--------------
*05/20/2019*

This release of Holodeck is focused on polishing existing features and allowing
worlds to be customized more.

This summer we are planning on adding much more content (worlds, agents, etc).

Highlights
~~~~~~~~~~
- Added :ref:`Scenarios <scenarios>` to allow worlds to be more flexible and
  customizable
- Documentation has been greatly expanded

New Features
~~~~~~~~~~~~
- Added expanded teleport functionality
  (`#128 <https://github.com/BYU-PCCL/holodeck/issues/128>`_)
- Add ticks per capture command for RGB Camera
  (`#127 <https://github.com/BYU-PCCL/holodeck/issues/127>`_)
- Add ``__enter__`` and ``__exit__`` methods to :class:`~holodeck.environments.HolodeckEnvironment`
  (`#125 <https://github.com/BYU-PCCL/holodeck/issues/125>`_)
- Add option to run headless on Linux
  (:meth:`~holodeck.environments.HolodeckEnvironment.set_render_quality` on
  :class:`~holodeck.environments.HolodeckEnvironment`)
  (`#135 <https://github.com/BYU-PCCL/holodeck/issues/135>`_)
- Add ability to adjust rendering options
  (:meth:`~holodeck.environments.HolodeckEnvironment.set_render_quality`)
  (`#136 <https://github.com/BYU-PCCL/holodeck/issues/136>`_)
- Add environment flag that allows state to be returned as copied object
  instead of reference
  (`#151 <https://github.com/BYU-PCCL/holodeck/issues/151>`_)
- Packages are not hard-coded on server, binaries are saved in version-specific
  folder to prevent crosstalk
  (`#188 <https://github.com/BYU-PCCL/holodeck/pull/188>`_)
- Sensors can be disabled to improve performance
  (`#152 <https://github.com/BYU-PCCL/holodeck/pull/152>`_)
- Add the ability to draw points, lines, arrows and boxes in the worlds
  (`#144 <https://github.com/BYU-PCCL/holodeck/pull/144>`_)
- Added new tasks for use with scenarios
- Added new scaled torque control scheme to the Android
  (`#150 <https://github.com/BYU-PCCL/holodeck/pull/144>`_)


Bug Fixes
~~~~~~~~~
- Fixed ``mmap length is greater than filesize`` error on startup
  (`#115 <https://github.com/BYU-PCCL/holodeck/issues/115>`_)
- Make all unit conversions on holodeck-engine side
  (`#162 <https://github.com/BYU-PCCL/holodeck/issues/162>`_)
- Fix multi-agent example (thanks bradyz!)
  (`#118 <https://github.com/BYU-PCCL/holodeck/issues/118>`_)
- Make sure :meth:`~holodeck.environments.HolodeckEnvironment.reset` called before
  :meth:`~holodeck.environments.HolodeckEnvironment.tick` and
  :meth:`~holodeck.environments.HolodeckEnvironment.act`
  (`#156 <https://github.com/BYU-PCCL/holodeck/issues/156>`_)
- And many smaller bugs!

Holodeck 0.1.0
--------------

Initial public release.
