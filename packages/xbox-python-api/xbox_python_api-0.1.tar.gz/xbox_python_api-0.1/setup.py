from setuptools import setup, find_packages

setup(
    name="xbox-python-api",
    version="0.1",
    url="https://github.com/Rarmash/XPA",
    author="Rarmash",
    description="Xbox API library",
    packages=find_packages(),
    install_requires=["requests==2.31.0"]
)
