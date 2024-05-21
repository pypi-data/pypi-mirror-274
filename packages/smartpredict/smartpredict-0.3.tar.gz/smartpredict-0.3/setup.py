# # setup.py
# """
# Setup script for SmartPredict.
# Defines the package and its dependencies.
# """

# # Read the contents of your README file
# from pathlib import Path
# from setuptools import setup, find_packages
# this_directory = Path(__file__).parent
# long_description = (this_directory / "README.md").read_text()

# from setuptools import setup, find_packages

# setup(
#     name="smartpredict",
#     version="0.2",
#     packages=find_packages(),
#     install_requires=[
#         "scikit-learn",
#         "numpy",
#         "pandas",
#         "shap",
#         "optuna",
#         "xgboost",
#         "lightgbm",
#         "catboost",
#         "tensorflow",
#         "torch"
#     ],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )



from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="smartpredict",
    version="0.3",  # Update the version number
    description="An advanced machine learning library for effortless model training, evaluation, and selection.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Subashanan Nair",
    author_email="subaashnair12@gmail.com",
    url="https://github.com/SubaashNair/SmartPredict",
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