try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "url": "https://github.com/HereIsKevin/hackathon",
    "download_url": "https://github.com/HereIsKevin/hackathon",
    "version": "0.1.0",
    "install_requires": [],
    "packages": ["hackathon"],
    "scripts": [],
    "name": "hackathon",
    "python_requires": ">=3.6",
}

setup(**config)
