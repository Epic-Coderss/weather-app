try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "url": "https://github.com/shriraj20/weather-app",
    "download_url": "https://github.com/shriraj20/weather-app.",
    "version": "0.1.0",
    "install_requires": ["requests", "pillow"],
    "packages": ["hackathon"],
    "scripts": [],
    "name": "hackathon",
    "python_requires": ">=3.6",
}

setup(**config)
