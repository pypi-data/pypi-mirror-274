import setuptools
from setup_kwargs import kwargs

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    **kwargs,
    long_description=long_description,
    packages=setuptools.find_packages(),
)
