import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    install_requires=open(os.path.join(here, "requirements", "reqs.txt"), encoding="utf-8")
    .read()
    .split("\n")
)
