.. _`avoid-task`:

Avoid Task
===========

The avoid task calculates a reward based on the distance between the agent and
an actor to avoid, with an option to incorporate whether the actor to avoid can
see the agent.

If ``OnlyWithinSight`` is ``false``, then the reward is set to the the percent distance
covered from the MinDistance to the ToAvoid Actor. The closer ToAvoid is, the lower
the reward.

If ``OnlyWithinSight`` is ``true``, the reward calculation is the same as above *if* the
angle from the ToAvoid to the agent is less than FOVRadians *and* is there is
nothing blocking the ToAvoid's line of sight. Otherwise the reward is 100.

The reward will be a value 0 to 100

Configuration
-------------

Each of the following parameters can be placed in the configuration field
for an avoid task sensor (see :ref:`scenario files <scenario-files>`.)

ToAvoid
~~~~~~~~

Name of the actor to avoid.

``"ToAvoid": "name-of-actor"``

OnlyWithinSight
~~~~~~~~~~~~~~~

Boolean value indicating if the reward should be calculated only when the
agent is within the ToAvoid actor's field of view.

``"OnlyWithinSight": true``

FOVRadians
~~~~~~~~~~

Float value, the field of view of the agent, in radians. See above how this is
used in the reward calculation.

``"FOVRadians": 1.5``

MinDistance
~~~~~~~~~~~

Float value, used to specify the minimum distance.

``"MinDistance": 512.0``

StartSocket
~~~~~~~~~~~~

The socket of the ToAvoid actor that its vision is calculated from.

``"StartSocket": "head"``

EndSocket
~~~~~~~~~~~~

The socket of the agent that the ToAvoid actor needs to see for the vision
calculation.

``"EndSocket": "body"``

Example
-------

.. code-block:: json

   {
       "ToAvoid": "hunter",
       "OnlyWithinSight": true,
       "FOVRadains": 2.0,
       "MinDistance": 1000.0,
       "StartSocket": "head",
       "EndSocket": "body"
   }
