import codecs
import os
from setuptools import setup, find_packages


# Taken from pip's setup.py
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open("README.md") as readme_file:
    README = readme_file.read()

setup_args = dict(
    name="py-allspice",
    version=get_version("allspice/__init__.py"),
    description="A python wrapper for the AllSpice Hub API",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",
    packages=find_packages(),
    author="AllSpice, Inc.",
    author_email="maintainers@allspice.io",
    keywords=["AllSpice", "AllSpice Hub", "api", "wrapper"],
    url="https://github.com/AllSpiceIO/py-allspice",
    download_url="https://github.com/AllSpiceIO/py-allspice",
)

install_requires = [
    "requests",
    "frozendict",
]

extras_require = {"test": ["pytest"]}

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires, extras_require=extras_require)
