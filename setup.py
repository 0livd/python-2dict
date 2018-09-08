from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="todict",
    version="0.2.4",
    description="Export python objects as dictionnaries so they can then be easily serializable.",
    long_description=long_description,
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
    author="0livd",
    url="https://github.com/0livd/python-todict",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
)
