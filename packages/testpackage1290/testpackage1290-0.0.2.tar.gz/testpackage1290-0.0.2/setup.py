# setup.py
from setuptools import setup, find_packages

setup(
    name = "testpackage1290",
    version = "0.0.2",
    packages = find_packages(),
    install_requires = [],
    include_package_data = True,
    description = "A simple example package",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://pypi.org/project/testpackage1290/",
    author = "Stefan Jansen",
    author_email = "stefanjansen95@hotmail.com",
    license = "MIT",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
)
