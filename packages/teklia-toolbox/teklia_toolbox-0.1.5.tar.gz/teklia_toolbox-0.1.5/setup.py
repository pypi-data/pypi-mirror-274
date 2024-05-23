#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup


def requirements(path):
    assert path.exists(), f"Missing requirements {path}"
    with path.open() as f:
        return list(map(str.strip, f.read().splitlines()))


with Path("VERSION").open() as f:
    VERSION = f.read()

install_requires = requirements(Path("requirements.txt"))

setup(
    name="teklia-toolbox",
    version=VERSION,
    author="Teklia",
    author_email="contact@teklia.com",
    python_requires=">=3.10",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
)
