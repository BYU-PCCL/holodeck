.. _`package-locations`:

=============================
Package Installation Location
=============================

Holodeck packages are by default saved in the current user profile, depending
on the platform.

========== ==================================================================
 Platform   Location
========== ==================================================================
Linux      ``~/.local/share/holodeck/{holodeck_version}/worlds/``
Windows    ``%USERPROFILE%\AppData\Local\holodeck\{holodeck_version}\worlds``
========== ==================================================================

Note that the packages are saved in different subfolders based on the version
of Holodeck. This allows multiple versions of Holodeck to coexist, without
causing version incompatibility conflicts.

This is the path returned by :func:`holodeck.util.get_holodeck_path`

Each folder inside the worlds folder is considered a seperate package, so it 
must match the format of the archive described in :ref:`package-contents`.

Overriding Location
-------------------

The environment variable ``HOLODECKPATH`` can be set to override the default
location given above.

.. caution::
   If ``HOLODECKPATH`` is used, it will override
   this version partitioning, so ensure that ``HOLODECKPATH`` only points to 
   packages that are compatible with your version of Holodeck.
