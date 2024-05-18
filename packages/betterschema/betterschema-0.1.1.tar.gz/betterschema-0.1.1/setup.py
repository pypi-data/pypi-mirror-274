from setuptools import setup, find_packages, Extension
import os


module = Extension(
    "betterschema.baselib",
    # all c files in the lib/src directory
    sources=[
        os.path.join("baselib", "src", f)
        for f in os.listdir("baselib/src")
        if f.endswith(".c")
    ],
    include_dirs=["baselib/include"],
    extra_compile_args=["-O3", "-Wall", "-Wextra", "-Werror", "-std=c11"],
    extra_link_args=["-O3", "-Wall", "-Wextra", "-Werror", "-std=c11"],
)


setup(
    name="betterschema",
    version="0.1.1",
    author="Wilson Wang",
    project_urls={
        'Source': 'https://github.com/wilsonwang371/betterschema',
    },
    author_email="wilsonny371@gmail.com",
    description="A library for schema support in Python",
    packages=find_packages(where="src", exclude=["tests"]),
    setup_requires=[
        "build",
    ],
    install_requires=[
        "pyyaml",
    ],
    extras_require={
        "dev": [
            "unittest",
            "black",
            "build",
        ]
    },
    # only include from source directory
    package_dir={"": "src"},
    ext_modules=[module],
)
