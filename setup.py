from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="holodeck",
    version="0.3.1dev",
    description="High fidelity simulated environments for reinforcement learning",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joshua Greaves, Max Robinson, Nick Walton, Jayden Milne",
    author_email="holodeck@cs.byu.edu",
    url="https://github.com/byu-pccl/holodeck",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='MIT License',
    python_requires=">=3.5",
    install_requires=[
        'posix_ipc >= 1.0.0; platform_system == "Linux"',
        'pywin32 >= 1.0; platform_system == "Windows"',
        'numpy'
    ],
)
