#   Copyright (c) Meta Platforms, Inc. and affiliates.

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="dragonclaw_library",
    version="1.0.0",
    author="Vani Sundaram",
    author_email="vasu1360@colorado.edu",
    description="Interfacing Library for DragonClaw",
    long_description=read("README.md"),
    packages=find_packages(),
    install_requires=["numpy>=1.21.3", "pyserial>=3.5"],
    python_requires=">=3.6",
    url="https://github.com/vasu1360/dragonclaw_library.git",
)
