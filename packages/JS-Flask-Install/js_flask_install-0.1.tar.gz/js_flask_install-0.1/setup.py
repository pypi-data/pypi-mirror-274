from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'Sets up a basic Javascript Boilerplate and Directory Structure for a Flask App.'
LONG_DESCRIPTION = 'A package that sets up a basic Javascript Boilerplate and Directory Structure for a Flask App.'

# Setting up
setup(
    name="JS_Flask_Install",
    version=VERSION,
    author="kunaalg",
    author_email="<kunaal@runcode.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    scripts=['run.sh'],
    install_requires=['datetime', 'pandas', 'requests', 'numpy', 'flask', 'python-dotenv', 'pipreqs', 'pip-tools', 'JS_Flask_Install.writefile_js'],
    keywords=['python', 'Flask', 'App', 'Javascript', 'Function', 'math'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)