.. _`distance-task`:

Distance Task
=============

The distance tasks calculates a dense distance based reward. The agent will receive a
reward of 1 as it crosses intervals that are a certain distance away from a goal location.
It can be configured to have the agent either maximize or minimize the distance from a
location, actor or the agent's starting location.


Configuration
-------------

Each of the following parameters can be placed in the configuration field
for a distance task sensor (see :ref:`scenario files <scenario-files>`.)

DistanceActor
~~~~~~~~~~~~~

The reward is calculated by measuring the distance between the distance actor
and the goal actor/location. If left empty, it will default to the task's agent.

- ``"DistanceActor": "name-of-actor"``

Goal
~~~~

The distance between the goal actor/location and the distance actor is used
to calculate the reward. Only the GoalActor or GoalLocation can be set, not
both.

``"GoalActor": "name-of-actor"``

or

``"GoalLocation": [1.0, 2.0, 3.0]``

Interval
~~~~~~~~

The interval controls the distance an agent must cover before it receives a
reward.

``"Interval": 5``

GoalDistance
~~~~~~~~~~~~

This distance is used to determine if the task has reached its terminal state
and the agent has travelled far enough away.

``"GoalDistance": 1``

MaximizeDistance
~~~~~~~~~~~~~~~~

Boolean value to indicate if the distance should be maximized or minimized.
If left empty, it defaults to false.

``"MaximizeDistance": true``

3dDistance
~~~~~~~~~~

Boolean value to indicate whether to incorporate height into the distance calculation.
If false, it will only use the xy values and ignore vertical distance.
If left empty, it defaults to false.

``"3dDistance": true``

Example
-------
.. code-block:: json

   {
       "DistanceActor": "baseball",
       "GoalActor": "target",
       "Interval": 5,
       "GoalDistance": 0.2,
       "MaximizeDistance": false
   }
