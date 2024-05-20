import setuptools
from setuptools import setup, find_packages
setup(
    name="Package_G2",
    version='1.0.1',
    author="Groupe 2",
    description='Le package fournit des implémentations des algorithmes KNN et K-means',
    packages=find_packages(),
    readme = "Readme.md",
    install_requires=['numpy','pandas'],
    python_requires = ">=3.10"
)