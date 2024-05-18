# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `rime-api-key` header.

    The version of the OpenAPI document: 1.0
    Contact: dev@robustintelligence.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501
from pathlib import Path

from setuptools import setup, find_packages  # noqa: H301

CUR_DIR = Path(__file__).parent

with open(CUR_DIR / "README.md", "r") as fh:
    long_description = fh.read()

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "robustintelligence"
VERSION = "0.1.0rc14"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "urllib3 >= 1.25.3, < 2.1.0",
    "python-dateutil",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="Robust Intelligence REST API SDK",
    author="Robust Intelligence",
    author_email="dev@robustintelligence.com",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Robust Intelligence REST API SDK", "Robust Intelligence SDK"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
	license="OSI Approved :: Apache Software License",
    long_description_content_type='text/markdown',
    long_description="""\
    API methods for Robust Intelligence. Users must authenticate using the 'rime-api-key' or 'X-Firewall-Api-Key' header.
    """,  # noqa: E501
    package_data={"ri.apiclient": ["py.typed"]},
)
