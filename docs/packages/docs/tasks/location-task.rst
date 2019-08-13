.. _`location-task`:

Location Task
=============

Calculates a sparse distance reward based on the distance to a location or an
actor. Can maximize or minimize a distance. A reward of 1 is only given only if
the agent reaches the goal target within the goal distance.

Configuration
-------------

Each of the following parameters can be placed in the configuration field
for a location task sensor (see :ref:`scenario files <scenario-files>`.)


LocationActor
~~~~~~~~~~~~~

The reward is given based on the distance between this actor and the goal target.
Defaults to the task's agent.

``"LocationActor": "name-of-actor"``

GoalTarget
~~~~~~~~~~~

The Location task needs an actor or a location to use in the distance calculations.

``"GoalActor": "name-of-actor"``

or

``"GoalLocation": [3.14, 2.71, 117]``

GoalDistance
~~~~~~~~~~~~~

This is the distance from the goal target the ``LocationActor`` must be to get a reward
and terminal.

``"GoalDistance": 1024.0``

NegativeReward
~~~~~~~~~~~~~~

A boolean representing whether reaching the goal target returns ``1`` or ``-1``. Defaults
to false.

``"NegativeReward": false``

HasTerminal
~~~~~~~~~~~

A boolean representing whether reaching the goal target returns a terminal value or
not. Defaults to false.

``"HasTerminal": true``


Example
-------

.. code-block:: json

   {
       "LocationActor": "golf-ball",
       "GoalActor": "cup",
       "GoalDistance": 1024.0,
       "NegativeReward": false,
       "HasTerminal": true
   }

