Cup Game Task
=============

Calculates reward based on whether the correct cup is touched and whether
the ball is touched. A reward of 1 is given if the correct cup is touched
and no other cups are touched, and a reward of 2 and terminal is given
when the ball itself is touched and no incorrect cups are touched.

The cup game task only works in the CupGame world in the dexterity package.
The game will not start if a cup game task is not added to an agent.

Configuration
-------------

Each of the following parameters can be placed in the configuration field
for a cup game task sensor (see :ref:`scenario files <scenario-files>`.)
The configuration can also be changed programmatically by calling
:meth:`~holodeck.sensors.CupGameTask.start_game`, though the configuration
block must be removed from the config file or it will not work.


Speed Multiplier
~~~~~~~~~~~~~~~~

``1.0`` is the base speed, cups will rotate faster with a higher multiplier. 
It is best to keep values between ``1`` and ``10``.

``"Speed": 2.4``


NumShuffles
~~~~~~~~~~~

Number of times the cups are exchanged.

``"NumShuffles": 10``


Seed
~~~~

Seed for the RNG used to shuffle the cups. Providing a fixed seed will result
in a deterministic set of exchanges, which may be useful for training.

If left empty or not defined, the cups will rotate using a randomly generated
seed.

``"Seed": 1``


Example
-------

.. code-block:: json

    {
        "Speed": 5.0,
        "NumShuffles": 1,
        "Seed": 0
    }

