from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.11'
DESCRIPTION = 'Package for personal use in Data Science'
LONG_DESCRIPTION = 'Package for personal use in DataS Science, Machine Learning and Deep Learning'

# Setting up
setup(
    name="gogr_tools",
    version=VERSION,
    author="Grzegorz Gomza",
    author_email="<gomza.datascience@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['plotly', 'pandas', 'random'],
    keywords=['python', 'Data Science'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)