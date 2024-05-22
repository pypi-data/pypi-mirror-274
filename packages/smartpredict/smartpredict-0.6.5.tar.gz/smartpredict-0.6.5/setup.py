# from setuptools import setup, find_packages
# from pathlib import Path

# # Read the contents of your README file
# this_directory = Path(__file__).parent
# readme_path = this_directory / "README.md"

# if readme_path.exists():
#     long_description = readme_path.read_text()
# else:
#     long_description = "SmartPredict: An advanced machine learning library for effortless model training, evaluation, and selection."

# setup(
#     name="smartpredict",
#     version="0.6",  # Update the version number
#     description="An advanced machine learning library for effortless model training, evaluation, and selection.",
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     author="Subashanan Nair",
#     author_email="subaashnair12@gmail.com",
#     url="https://github.com/SubaashNair/SmartPredict",
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
readme_path = this_directory / "README.md"

if readme_path.exists():
    long_description = readme_path.read_text(encoding='utf-8')
else:
    long_description = "SmartPredict: An advanced machine learning library for effortless model training, evaluation, and selection."

setup(
    name="smartpredict",
    version="0.6.5",  # Update the version number
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

# Rebuild the distribution package
# Run these commands in your terminal

# python setup.py sdist bdist_wheel

# Upload to PyPI using Twine
# twine upload dist/*

