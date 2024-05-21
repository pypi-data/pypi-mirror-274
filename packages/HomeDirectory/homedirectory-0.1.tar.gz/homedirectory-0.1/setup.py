from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'Sets up a basic function to print and show the Home Directory of the current Terminal.'
LONG_DESCRIPTION = 'A package that sets up a basic function to print and show the Home Directory of the current terminal.'

# Setting up
setup(
    name="HomeDirectory",
    version=VERSION,
    author="kunaalg",
    author_email="<kunaal@runcode.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    scripts=['run.sh'],
    install_requires=['datetime', 'requests', 'virtualenv'],
    keywords=['python', 'homedirectory', 'home', 'directory', 'root', 'hd'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)