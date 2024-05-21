# setup.py
"""
Setup script for SmartPredict.
Defines the package and its dependencies.
"""

from setuptools import setup, find_packages

setup(
    name="smartpredict",
    version="0.1",
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