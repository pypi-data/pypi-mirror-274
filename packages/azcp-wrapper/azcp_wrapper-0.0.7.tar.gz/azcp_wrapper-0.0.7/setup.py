import os
import sys
from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# read version number from version.txt, otherwise alpha version
# Github CI can create version.txt dynamically.
def get_version(fname):
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            version = f.readline().strip()
    else:
        version = 'alpha'

    return version

print(get_version("version.txt"))
setup(
    name="azcp_wrapper",
    version=get_version("version.txt"),
    description="A simple AzCopy wrapper to transfer data",
    long_description=open("README.md", encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eabdala/azcp_wrapper",
    author="Erik Alejandro Abdala",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "azcp-init=azcp_wrapper.setup:main",
        ],
    },
)
