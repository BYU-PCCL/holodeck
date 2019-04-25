import holodeck
from holodeck import agents
from holodeck.environments import *


def test_install():
    # This will install the binaries for the DefaultWorlds Package if it is not already installed.
    holodeck.install("DefaultWorlds")
    print(holodeck.package_info("DefaultWorlds"))

    assert "DefaultWorlds" in holodeck.installed_packages()
