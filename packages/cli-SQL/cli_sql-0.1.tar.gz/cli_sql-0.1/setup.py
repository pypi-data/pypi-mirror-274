from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'Sets up a basic CLI application to connect with a SQL_Database'
LONG_DESCRIPTION = 'A package that sets up a basic CLI application interact with your SQL database.'

# Setting up
setup(
    name="cli_SQL",
    version=VERSION,
    author="kunaalg",
    author_email="<kunaal@runcode.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    include_package_data=True,
    data_files=[
        ('src/SQLcli.py', ['src/SQLcli.py']),
        ],
    packages=find_packages(),
    scripts=[],
    install_requires=['datetime', 'argparse', 'requests', 'mysql.connector', 'flask', 'virtualenv'],
    keywords=['python', 'Flask', 'App', 'SQL', 'CLI', 'Database'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)