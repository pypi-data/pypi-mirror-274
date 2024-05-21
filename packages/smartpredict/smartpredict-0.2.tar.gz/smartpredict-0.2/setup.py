# setup.py
"""
Setup script for SmartPredict.
Defines the package and its dependencies.
"""

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

from setuptools import setup, find_packages

setup(
    name="smartpredict",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "scikit-learn",
        "numpy",
        "pandas",
        "shap",
        "optuna",
        "xgboost",
        "lightgbm",
        "catboost",
        "tensorflow",
        "torch"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)