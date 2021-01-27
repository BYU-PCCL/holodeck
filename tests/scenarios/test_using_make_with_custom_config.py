import random
import holodeck


def test_using_make_with_custom_config():
    """
    Validate that we can use holodeck.make with a custom configuration instead
    of loading it from a config file
    """

    conf = {"name": "test_randomization", "agents": []}

    # pick a random world from the installed packages
    pkg = random.choice(list(holodeck.packagemanager._iter_packages()))

    world = random.choice(pkg[0]["worlds"])["name"]

    conf["world"] = world
    conf["package_name"] = pkg[0]["name"]

    print("world: {} package: {}".format(world, pkg[0]["name"]))
    with holodeck.make(scenario_cfg=conf, show_viewport=False) as env:
        for _ in range(0, 10):
            env.tick()
