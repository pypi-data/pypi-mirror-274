import os

from setuptools import setup, find_packages


def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name), encoding="utf8").read()


setup(
    name="xbox-python-api",
    version="0.1.2.4",
    url="https://github.com/Rarmash/Xbox-Python-API",
    author="Rarmash",
    description="Xbox API library",
    packages=find_packages(),
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    install_requires=["requests==2.31.0"]
)
