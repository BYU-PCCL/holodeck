from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="holodeck",
    version="0.0.21",
    description="High fidelity simulated environments for reinforcement learning",
    long_description=readme,
    author="Joshua Greaves, Max Robinson, Nick Walton",
    author_email="holodeck@cs.byu.edu",
    url="https://github.com/byu-pccl/holodeckpythonbinding",
    packages=["holodeck"],
    license='MIT License',
    python_requires=">=3",
    install_requires=[
        'posix_ipc >= 1.0.0; platform_system == "Linux"',
        'pywin32 >= 1.0; platform_system == "Windows"',
        'numpy'
    ],
)
