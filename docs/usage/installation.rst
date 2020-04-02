.. _installation:

============
Installation
============

Holodeck is installed in two portions: a client python library (``holodeck``)
is installed first, which then downloads world packages. The python portion is
very small, while the world packages ("binaries") can be several gigabytes.


Requirements
============

- >= Python 3.5
- Several gigabytes of storage
- pip3
- Linux: OpenGL 3+

Install Client via pip
======================

The latest stable Holodeck package is available in a pip repository:

``pip install holodeck``

.. note::
   On some Ubuntu systems a dependency of Holodeck (``posix-ipc``) can fail to
   install if you do not have the ``python3-dev`` package installed.

   .. code-block:: console

      $ apt install python3-dev

Install Client via git
=======================

To use the latest version of Holodeck, you can install and use Holodeck simply
by cloning the `BYU-PCCL/holodeck`_ repository, and ensuring it is on your
``sys.path``.

.. _`BYU-PCCL/holodeck`: https://github.com/BYU-PCCL/holodeck

The ``master`` branch is kept in sync with the pip repository, the ``develop``
branch is the bleeding edge of development.

If you want to download a specific release of Holodeck, each release is tagged
in the Git repository.

.. _docker:

Docker Installation
===================

Holodeck's docker image is only supported on Linux hosts.

You will need ``nvidia-docker`` installed.

The repository on DockerHub is `pccl/holodeck`_.

Currently the following tags are availible:

- ``base`` : base image without any worlds
- ``default-worlds`` : comes with the default worlds pre-installed
- ``dexterity`` : comes with the dexterity package pre-installed

.. _`pccl/holodeck`: https://hub.docker.com/r/pccl/holodeck

This is an example command to start a holodeck container

``nvidia-docker run --rm -it --name holodeck pccl/holodeck:default-worlds``

.. note::
   Holodeck cannot be run with root privileges, so the user ``holodeckuser`` with
   no password is provided in the docker image.

Managing World Packages
=======================

The ``holodeck`` python package includes a :ref:`packagemanager` that is used
to download and install world packages. Below are some example usages, but see
:ref:`packagemanager` for complete documentation.

Install a Package Automatically
-------------------------------
::

   >>> from holodeck import packagemanager
   >>> packagemanager.installed_packages()
   []
   >>> packagemanager.available_packages()
   {'DefaultWorlds': ['0.1.0', '0.1.1'], 'MoveBox': ['0.0.1']}
   >>> packagemanager.install("DefaultWorlds")
   Installing DefaultWorlds ver. 0.1.1 from http://localhost:8080/packages/0.2.0/DefaultWorlds/Linux/0.1.1.zip
   File size: 1.55 GB
   |████████████████████████| 100%
   Unpacking worlds...
   Finished.
   >>> packagemanager.installed_packages()
   ['DefaultWorlds']

Installation Location
---------------------

By default, Holodeck will install packages local to your user profile. See
:ref:`package-locations` for more information.

Manually Installing a Package
-----------------------------

To manually install a package, you will be provided a ``.zip`` file.
Extract it into the ``worlds`` folder in your Holodeck installation location 
(see :ref:`package-locations`)

.. note::

   Ensure that the file structure is as follows:

   ::

      + worlds
      +-- YourManuallyInstalledPackage
      |   +-- config.json
      |    +-- etc...
      +-- AnotherPackage
      |   +-- config.json
      |   +-- etc...

   Not

   ::

      + worlds
      +-- YourManuallyInstalledPackage
      |   +-- YourManuallyInstalledPackage
      |       +-- config.json
      |   +-- etc...
      +-- AnotherPackage
      |   +-- config.json
      |   +-- etc...

Print Information
-----------------

There are several convenience functions provided to allow packages, worlds,
and scenarios to be easily inspected.

::

   >>> packagemanager.package_info("DefaultWorlds")
   Package: DefaultWorlds
      Platform: Linux
      Version: 1.04
      Path: LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck
      Worlds:
      UrbanCity
            Scenarios:
            UrbanCity-Follow:
               Agents:
                  Name: ThisIsAScenario
                  Type: UavAgent
                  Sensors:
                  RGBCamera
                  OrientationSensor
                  LocationSensor
      CyberPunkCity
            Scenarios:
            CyberPunkCity-Follow:
               Agents:
                  Name: ThisIsAScenario
                  Type: UavAgent
                  Sensors:
                  RGBCamera
                  OrientationSensor
                  LocationSensor


You can also look for information for a specific world or scenario

::

   packagemanager.world_info("UrbanCity")
   packagemanager.scenario_info("UrbanCity-Follow")
