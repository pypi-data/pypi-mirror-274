from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Sets up a basic CLI application to print the Home Directory and use inputs to change the cuurent directory or make a new directory '
LONG_DESCRIPTION = 'A package that sets up a basic CLI App to work and nvigate through the home directories.'

# Setting up
setup(
    name="CLI_APP_DIRECTORY",
    version=VERSION,
    author="kunaalg",
    author_email="<kunaal@runcode.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['datetime', 'requests'],
    keywords=['python', 'Directory', 'App', 'Home', 'Make', 'Home Directory'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)