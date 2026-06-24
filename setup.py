"""
Setup configuration for the ubu package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ubu",
    version="0.1.0",
    author="Lee Azzarello",
    description="A Python module for archiving content from UbuWeb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lazzarello/ubuweb-mirror",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Archiving",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "requests-html",
        "lxml[html-clean]",
        "beautifulsoup4",
        "tqdm",
        "youtube-dl",
        "tweepy",
    ],
    entry_points={
        "console_scripts": [
            "ubu-download=main:main",
        ],
    },
)
