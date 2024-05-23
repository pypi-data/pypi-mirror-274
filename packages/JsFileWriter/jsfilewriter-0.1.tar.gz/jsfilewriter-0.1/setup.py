from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'Sets up and writes an Js File using a filewriter.'
LONG_DESCRIPTION = 'A package that sets up a basic filewriter to write a JS File in any directory.'

# Setting up
setup(
    name="JsFileWriter",
    version=VERSION,
    author="kunaalg",
    author_email="<kunaal@runcode.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('src/js_writer.py', ['src/js_writer.py']),
        ],
    scripts=[],
    install_requires=['datetime', 'pandas', 'requests', 'virtualenv'],
    keywords=['python', 'FileWriter', 'App', 'HTML', 'Function', 'math'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)