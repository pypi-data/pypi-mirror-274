from setuptools import setup, find_packages

setup(
    name="rtd-cli",
    version="0.0.3",
    description="Simple CLI wrapper for the Readthedocs REST API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/runsascoded/rtd.py",
    author="Ryan Williams",
    author_email="ryan@runsascoded.com",
    install_requires=open("requirements.txt").read(),
    entry_points={
        "console_scripts": [
            "rtd = rtd.main:cli",
        ],
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
