from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'A simple implimentation of the blockchain technology.'
LONG_DESCRIPTION = 'A package that sets up a block chain running in a seperate flask app.'

# Setting up
setup(
    name="BlockchainServer",
    version=VERSION,
    author="kunaalg",
    author_email="<kunaal@runcode.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=[],
    packages=find_packages(),
    install_requires=['virtualenv', 'datetime', 'numpy','requests', 'hashlib','time', 'flask', 'rsa'],
    keywords=['python', 'blockchain', 'flask', 'block', 'numbers', 'math'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)