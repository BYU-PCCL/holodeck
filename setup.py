from setuptools import setup

setup(
    name="holodeck",
    version="0.0.21",
    packages=["holodeck"],
    license='MIT License',
    long_description=open('README.md').read(),
    install_requires=[
        'posix_ipc >= 1.0.0; platform_system == "Linux"',
        'pywin32 >= 1.0; platform_system == "Windows"',
        'numpy'
    ],
)
