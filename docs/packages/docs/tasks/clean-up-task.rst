.. _`clean-up-task`:

Clean Up Task
=============

Initializes the clean up task in the world. This task only works in the
CleanUp world in the Dexterity package where there is a trash can in the
middle of the map.

Trash will spawn randomly around the trash can when the task starts. A clean
up task must be added to an agent for the task to start.

The reward is based on the number of pieces of trash placed in the trash
can. For each piece of trash added to the can, a reward of ``1`` is given.
For each piece of trash removed, a reward of ``-1`` is given. If all the trash
is in the can, terminal is given.

If ``UseTable`` is ``true`` a table will spawn next to the trash can, all trash
will be on the table, and the trash can lid will be absent. This makes the task
significantly easier. If ``false``, all trash will spawn on the ground.


Configuration
-------------

Each of the following parameters can be placed in the configuration field
for a clean up task sensor (see :ref:`scenario files <scenario-files>`.)

The configuration can also be set programmatically by calling
:meth:`~holodeck.sensors.CleanUpTask.start_task`. Do not call
if the config file has a configuration block.
That configuration will reset after every call to
:meth:`~holodeck.environments.reset`.

NumTrash
~~~~~~~~

Int representing the amount of trash to spawn around the trash can.

``"NumTrash": 6``


UseTable
~~~~~~~~

Boolean value representing whether to use the simpler table task configuration.


``"UseTable": false``


Example
-------

.. code-block:: json

    {
        "NumTrash": 5,
        "UseTable": false
    }

