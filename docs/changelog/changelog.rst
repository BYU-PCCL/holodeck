Changelog
=========

Holodeck 0.3.0
--------------
*Release Date TBD*

Features! Features! Features!

New Features
~~~~~~~~~~~~
- Added the :ref:`hand-agent` - a simplified Android hand that can float around
  (`#287 <https://github.com/BYU-PCCL/holodeck/issues/287>`_)

  - HandAgent can be used with the same Android-specific sensors (
    :class:`~holodeck.sensors.JointRotationSensor`,
    :class:`~holodeck.sensors.PressureSensor`,
    :class:`~holodeck.sensors.RelativeSkeletalPositionSensor`)
- Packages can be installed directly from a URL 
  (see :class:`~holodeck.packagemanager.install`)
  (`#129 <https://github.com/BYU-PCCL/holodeck/issues/129>`_)
- Pressing ``h`` now shows the coordinates of the agent the viewport is 
  following or the coordinates of the camera if it is detached (see 
  :ref:`hotkeys`)
  (`#253 <https://github.com/BYU-PCCL/holodeck/issues/253>`_)

Changes
~~~~~~~
- Increased the :ref:`android-agent`'s strength in the 
  ``ANDROID_MAX_SCALED_TORQUES`` control scheme.

  - Previously the AndroidAgent didn't have enough strength to even move its 
    legs.
  - Strength was approximately doubled (See
    `JointMaxTorqueControlScheme.h <https://github.com/BYU-PCCL/holodeck-engine/blob/develop/Source/Holodeck/Agents/Public/JointMaxTorqueControlScheme.h#L50>`_
    )
- Updated to Unreal Engine 4.22
  (`#241 <https://github.com/BYU-PCCL/holodeck/issues/241>`_)

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
