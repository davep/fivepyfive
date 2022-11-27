"""Setup file for the game."""

##############################################################################
# Python imports.
from pathlib    import Path
from setuptools import setup, find_packages

##############################################################################
# Import the library itself to pull details out of it.
import fivepyfive

##############################################################################
# Work out the location of the README file.
def readme():
    """Return the full path to the README file.

    :returns: The path to the README file.
    :rtype: ~pathlib.Path
    """
    return Path( __file__).parent.resolve() / "README.md"

##############################################################################
# Load the long description for the package.
def long_desc():
    """Load the long description of the package from the README.

    :returns: The long description.
    :rtype: str
    """
    with readme().open( "r", encoding="utf-8" ) as rtfm:
        return rtfm.read()

##############################################################################
# Perform the setup.
setup(

    name                          = "fivepyfive",
    version                       = fivepyfive.__version__,
    description                   = str( fivepyfive.__doc__ ),
    long_description              = long_desc(),
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/davep/fivepyfive",
    author                        = fivepyfive.__author__,
    author_email                  = fivepyfive.__email__,
    maintainer                    = fivepyfive.__maintainer__,
    maintainer_email              = fivepyfive.__email__,
    packages                      = find_packages(),
    package_data                  = { "fivepyfive": [ "py.typed", "fivepyfive.css", "help.md" ] },
    include_package_data          = True,
    install_requires              = [ "textual" ],
    python_requires               = ">=3.8",
    keywords                      = "puzzle game terminal",
    entry_points                  = {
        "console_scripts": "fivepyfive=fivepyfive.app:run"
    },
    license                       = (
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    ),
    classifiers                   = [
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Terminals",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Typing :: Typed"
    ]

)

### setup.py ends here
