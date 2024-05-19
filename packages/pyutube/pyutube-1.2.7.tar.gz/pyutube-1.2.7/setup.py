"""
This module contains the setup configuration for the pyutube package.
"""


from setuptools import find_packages, setup
from pyutube.utils import __version__


# Read the README file to use as the long description
with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

# Setup configuration
setup(
    name="pyutube",

    version=__version__,

    author="Ebraheem Alhetari",

    author_email="hetari4all@gmail.com",

    description="Awesome CLI to download YouTube videos (as video or audio)/shorts/playlists from the terminal",

    long_description=description,

    long_description_content_type="text/markdown",

    keywords=["youtube", "download", "cli", "pyutube", "pytubefix"],

    license="MIT",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],


    include_package_data=True,

    python_requires=">=3.6",

    install_requires=[
        "pytubefix",
        "inquirer",
        "yaspin",
        "typer",
        "requests",
        "rich",
        "inquirer",
        "termcolor",
        "moviepy"
    ],


    entry_points={
        "console_scripts": [
            "pyutube=pyutube:cli.app",
        ],
    },


    project_urls={
        "Homepage": "https://github.com/Hetari/pyutube",
    },

    platforms=["Windows", "MacOS", "Linux"],
    packages=find_packages()
)
