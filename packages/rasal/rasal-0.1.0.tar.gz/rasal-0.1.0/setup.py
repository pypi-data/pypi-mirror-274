#!/usr/bin/env python
import re
from pathlib import Path

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with Path(__file__).parent.joinpath(*names).open(
        encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


__name__ = "rasal"
__version__ = "0.1.0"


setup(
    name=__name__,
    version=__version__,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    license="MIT",
    description="Resolution and Sensors and Lens.",
    long_description="{}\n{}".format(
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Aidan Johnston",
    author_email="contact@aidanjohnston.ca",
    url="https://github.com/AidanJohnston/rasal",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://rasal.readthedocs.io/en/latest",
        "Changelog": "https://rasal.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/AidanJohnston/rasal/issues",
    },
    keywords=[
        "resolution", "sensor" "lens",
    ],
    python_requires=">=3.8",
    install_requires=[
        # eg: "aspectlib==1.1.1", "six>=1.7",
    ],
    extras_require={
        "test": [
        ]
    },
)
