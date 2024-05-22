from setuptools import setup

setup(
    name="rtd-cli",
    version="0.0.1",
    install_requires=open("requirements.txt").read(),
    entry_points={
        "console_scripts": [
            "rtd = rtd.main:cli",
        ],
    },
)
