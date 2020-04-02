.. _`hand-agent`:

HandAgent
=========

Images
------

.. image:: images/hand-agent.png
   :scale: 30%

Description
-----------
A floating hand agent that can be controlled by applying torques to joints and
moved around in three dimensions.

Control Schemes
---------------

- **Raw Joint Torques** (``0``)

  23 length vector of raw torques to pass into the joints, in the order listed
  beow in :ref:`hand-joints`

- **Scaled Joint Torques** (``1``)

  23 length vector of scaled torques, between ``-1`` and ``1``. The strength
  finger each joint is scaled depending on the weight of the bone and if it is
  a finger or not. ``1`` represents the maximum power in the forward direction


- **Scaled Joint Torques + Floating** (``2``)

  Same as above, but the vector is of length 26, with the last three values
  representing the amount of movement in the ``[x, y, z]`` directions (see
  :ref:`coordinate-system`), with a maximum of ``0.5`` meters of freedom.

  The last coordinates allow the HandAgent to float around.


.. _`hand-joints`:

HandAgent Joints
----------------
The control scheme for the HandAgent and the
:class:`~holodeck.sensors.JointRotationSensor` use a 94 length vector refer
to 48 joints.

To gain insight into these joints, refer to the table below.

.. note::
    Note that the index given is the start index for the joint, see the section
    header for how many values after this index each joint has.

    Example: ``hand_r`` starts at index 0, and has ``[swing1, swing2, twist]``,
    so index 0 in the vector corresponds to ``swing1``, 1 corresponds to
    ``swing2``, and 2 corresponds to ``twist`` for ``hand_r``

Returned in the following order:

+-------------------------------------+-----------------------+
| **Arm joints**                                              |
|                                                             |
| Each has ``[swing1, swing2, twist]``                        |
+-------------------------------------+-----------------------+
+-------------------------------------+-----------------------+
| ``0``                               | ``hand_r``            |
+-------------------------------------+-----------------------+
| **First joint of each finger**                              |
|                                                             |
| Has only ``[swing1, swing2]``                               |
+-------------------------------------+-----------------------+
| ``64``                              | ``thumb_01_r``        |
+-------------------------------------+-----------------------+
| ``66``                              | ``index_01_r``        |
+-------------------------------------+-----------------------+
| ``68``                              | ``middle_01_r``       |
+-------------------------------------+-----------------------+
| ``70``                              | ``ring_01_r``         |
+-------------------------------------+-----------------------+
| ``72``                              | ``pinky_01_r``        |
+-------------------------------------+-----------------------+
| **Second joint of each finger**                             |
|                                                             |
| Has only ``[swing1]``                                       |
+-------------------------------------+-----------------------+
| ``79``                              | ``thumb_02_r``        |
+-------------------------------------+-----------------------+
| ``80``                              | ``index_02_r``        |
+-------------------------------------+-----------------------+
| ``81``                              | ``middle_02_r``       |
+-------------------------------------+-----------------------+
| ``82``                              | ``ring_02_r``         |
+-------------------------------------+-----------------------+
| ``83``                              | ``pinky_02_r``        |
+-------------------------------------+-----------------------+
| **Third joint of each finger**                              |
|                                                             |
| Has only ``[swing1]``                                       |
+-------------------------------------+-----------------------+
| ``89``                              | ``thumb_03_r``        |
+-------------------------------------+-----------------------+
| ``90``                              | ``index_03_r``        |
+-------------------------------------+-----------------------+
| ``91``                              | ``middle_03_r``       |
+-------------------------------------+-----------------------+
| ``92``                              | ``ring_03_r``         |
+-------------------------------------+-----------------------+
| ``93``                              | ``pinky_03_r``        |
+-------------------------------------+-----------------------+

.. _`hand-bones`:

HandAgent Bones
---------------
The :class:`~holodeck.sensors.RelativeSkeletalPositionSensor` returns an
array with four entries for each of the 17 bones listed below.

========= ===============
  Index      Bone Name
========= ===============
``0``     ``lowerarm_r``
``4``     ``hand_r``
``8``     ``index_01_r``
``12``    ``index_02_r``
``16``    ``index_03_r``
``20``    ``middle_01_r``
``24``    ``middle_02_r``
``28``    ``middle_03_r``
``32``    ``pinky_01_r``
``36``    ``pinky_02_r``
``40``    ``pinky_03_r``
``44``    ``ring_01_r``
``48``    ``ring_02_r``
``52``    ``ring_03_r``
``56``    ``thumb_01_r``
``60``    ``thumb_02_r``
``64``    ``thumb_03_r``
========= ===============


Sockets
-------

- ``CameraSocket`` located behind and above the wrist
- ``Viewport`` located looking at the agent from the side
- All of the joints may be used as sockets. See
  :ref:`hand-joints`
