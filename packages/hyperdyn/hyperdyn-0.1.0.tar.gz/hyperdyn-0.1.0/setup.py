# setup.py

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hyperdyn",
    version="0.1.0",
    author="Skandan V",
    author_email="skandanskandu23456@gmail.com",
    description="A collection of powerful tools from Hyperdyn.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperdyn.ai/hyperdyn",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["pandas", "numpy"],  # Specify additional dependencies here
    include_package_data=True,
    package_data={"hyperdyn": ["data/*.csv", "data/*.json"]},  # Include data files
    entry_points={
        "console_scripts": [
            "hyperdyn-tool = hyperdyn.cli:main",
        ],
    },
    test_suite="tests",  # Specify the test suite for running tests
    tests_require=["pytest"],  # Specify additional test requirements
)
