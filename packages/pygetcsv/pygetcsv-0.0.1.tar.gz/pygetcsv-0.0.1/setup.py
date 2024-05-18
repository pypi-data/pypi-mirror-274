from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.1'
DESCRIPTION = 'Convert a Binary file into a CSV file, a Excel file'


# Setting up
setup(
    name="pygetcsv",
    version=VERSION,
    author="UNshubh (UnOfficialShubh)",
    author_email="<shubhashishpresent@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'Binary', 'csv', 'excel', 'dat', 'pickle'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)