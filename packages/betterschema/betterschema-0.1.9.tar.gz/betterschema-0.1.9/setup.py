"""Setup script for the BetterSchema package."""

import os
import sys
import re

from setuptools import Extension, find_packages, setup

module = Extension(
    "betterschema.baselib",
    # all c files in the lib/src directory
    sources=[
        os.path.join("baselib", "src", f)
        for f in os.listdir("baselib/src")
        if f.endswith(".c")
    ],
    include_dirs=["baselib/include"],
    extra_compile_args=["-O3", "-Wall", "-Werror", "-std=c11"],
    extra_link_args=["-O3", "-Wall", "-Werror", "-std=c11"],
)

# Add compiler-specific options
if sys.platform == "win32":
    module.extra_compile_args = ["/W4"]
else:
    module.extra_compile_args = ["-Wextra"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read_version():
    """Read the version from the package __init__ file."""
    with open(
        os.path.join(os.path.dirname(__file__), "src", "betterschema", "__init__.py"),
        "r",
        encoding="utf-8",
    ) as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="betterschema",
    author="Wilson Wang",
    version=read_version(),
    project_urls={
        "Source": "https://github.com/wilsonwang371/betterschema",
    },
    author_email="wilsonny371@gmail.com",
    description="A Python schema library that supports type checking and validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src", exclude=["tests"]),
    setup_requires=[
        "build",
    ],
    install_requires=[
        "PyYAML",
    ],
    extras_require={
        "dev": [
            "unittest",
            "black",
            "build",
            "isort",
            "pylint",
            "bump2version",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    # only include from source directory
    package_dir={"": "src"},
    ext_modules=[module],
)
