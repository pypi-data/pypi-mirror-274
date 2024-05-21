from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.1'
DESCRIPTION = 'Calculates the Mean of given Values'
LONG_DESCRIPTION = 'A package that defines a function to calculate the mean of n number of values'

# Setting up
setup(
    name="calculate_mean",
    version=VERSION,
    author="kunaalg",
    author_email="<kunaal@runcode.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=[],
    packages=find_packages(),
    install_requires=['virtualenv', 'datetime', 'numpy','requests'],
    keywords=['python', 'mean', 'calculate', 'calculate mean', 'numbers', 'math'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)