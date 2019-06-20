
def pytest_generate_tests(metafunc):
    """Iterate over every scenario
    """
    if 'resolution' in metafunc.fixturenames:
        metafunc.parametrize('resolution', [256, 512, 1024, 2048])
