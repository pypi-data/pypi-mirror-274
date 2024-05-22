#setup.py
from setuptools import setup, find_packages

setup(
    name="crispml-opus",
    version="0.0.1",
    author="R.Costa",
    author_email="rafael@aineural.net",
    description="The definitive Python framework for CRISP-ML Methodology Workflows",
    packages=find_packages(),
    install_requires=["polars"]
)