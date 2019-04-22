"""Install the pymint package."""
from distutils.core import setup

with open("README.rst") as f:
    readme = f.read()

setup(
    name="pymint",
    version="0.1",
    description=(
        "The 'pymint' package provides an interface for parsing and graphing "
        + "'transactions.csv' files from Intuit Mint."
    ),
    long_description=readme,
    author="Bryant Finney",
    author_email="bryant.finney@uah.edu",
    packages=["pymint", "pymint.tests"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],
)
