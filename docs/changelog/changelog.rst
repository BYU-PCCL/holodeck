Changelog
=========

Holodeck 0.2.0
--------------
*05/15/2019*

This release of Holodeck is focused on polishing existing features and allowing worlds to be customized more.
This summer we are planning on adding much more content (worlds, agents, etc).

Highlights
~~~~~~~~~~
- Added :ref:`Scenarios <scenarios>` to allow worlds to be more flexible and customizable
- Documentation has been greatly expanded

New Features
~~~~~~~~~~~~
- Added expanded teleport functionality 
  (`#128 <https://github.com/BYU-PCCL/holodeck/issues/128>`_)
- Add ticks per capture command for RGB Camera 
  (`#127 <https://github.com/BYU-PCCL/holodeck/issues/127>`_)
- Add ``__enter__`` and ``__exit__`` methods to :class:`~holodeck.environment.HolodeckEnvironment` 
  (`#125 <https://github.com/BYU-PCCL/holodeck/issues/125>`_)
- Add option to run headless on Linux 
  (``should_render_viewport`` on :class:`~holodeck.environment.HolodeckEnvironment`) 
  (`#135 <https://github.com/BYU-PCCL/holodeck/issues/135>`_)
- Add ability to adjust rendering options 
  (:meth:`~holodeck.environment.HolodeckEnvironment.set_render_quality`)
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


.. TODO: Add links to tasks!

Bug Fixes
~~~~~~~~~
- Fixed ``mmap length is greater than filesize`` error on startup 
  (`#115 <https://github.com/BYU-PCCL/holodeck/issues/115>`_)
- Make all unit conversions on holodeck-engine side 
  (`#162 <https://github.com/BYU-PCCL/holodeck/issues/162>`_)
- Fix multi-agent example (thanks bradyz!) 
  (`#118 <https://github.com/BYU-PCCL/holodeck/issues/118>`_)
- Make sure :meth:`~holdoeck.environment.HolodeckEnvironment.reset` called before 
  :meth:`~holdoeck.environment.HolodeckEnvironment.tick` and
  :meth:`~holdoeck.environment.HolodeckEnvironment.set`
  (`#156 <https://github.com/BYU-PCCL/holodeck/issues/156>`_)
- And many smaller bugs!

Holodeck 0.1.0
--------------

Initial public release.
