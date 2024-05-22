from setuptools import setup
import os

from kamangir import NAME, VERSION

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read().replace(
        "./",
        "https://github.com/kamangir/kamangir/raw/main/",
    )


setup(
    name=NAME,
    author="arash@kamangir.net",
    version=VERSION,
    description="kamangir.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[NAME],
)
