#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


# https://github.com/pypa/setuptools_scm
setup(
    name="svs-polygon-cropping",
    author="Pranathi Vemuri, Snigdha Agarwal",
    author_email="pranathi93.vemuri@gmail.com",
    license="BSD-3",
    url="https://github.com/czbiohub/svs-polygon-cropping",
    description="A plugin to lazily load multiscale whole-slide images with openslide and dask and crop polygonal segments.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.9",
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Framework :: napari",
    ],
    entry_points={
        "napari.plugin": [
            "svs_polygon_cropping = svs_polygon_cropping",
        ],
        "console_scripts": [
            "svs_polygon_cropping = svs_polygon_cropping.svs_polygon_cropping:main"
        ],
    },
)
