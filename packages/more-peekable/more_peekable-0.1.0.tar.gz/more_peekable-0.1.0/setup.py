#!/usr/bin/env python3

import re

from setuptools import find_packages, setup

src = "more_peekable"
string_assignment = re.compile(r"""__([\w_]+)__\s*=\s*"(.+)"$""")


data: dict[str, str] = {}
readme: str
requirements: list[str] = []

with open(f"{src}/__init__.py", "r") as file:
    for line in file.readlines():
        if (match := re.match(string_assignment, line)) is not None:
            data[match[1]] = match[2]
    data.pop("copyright", None)

with open("README.md", "r") as file:
    readme = file.read()

with open("requirements.txt", "r") as file:
    for line in file.read().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            requirements.append(line)

setup(
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requirements=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={src: ["py.typed"]},
    include_package_data=True,
    **data,  # type: ignore
)
