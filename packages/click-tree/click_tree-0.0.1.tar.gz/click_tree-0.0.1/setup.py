#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="click-tree",
    version="0.0.1",
    license="MIT",
    description=" automatically generate a tree view of a click CLI",
    author="Adam Miller",
    author_email="miller@adammiller.io",
    url="https://github.com/adammillerio/click-tree",
    download_url="https://github.com/adammillerio/click-tree/archive/v0.0.1.tar.gz",
    keywords=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "anytree",
        "click",
    ],
    extras_require={"dev": ["black", "pyre-check", "testslide"]},
)
