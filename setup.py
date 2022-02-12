from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    requirements = fh.read().split("\n")

setup(
    name="webscraper",
    version="1.0",
    author="Vishal Mohanty",
    author_email="vishalmohanty97@gmail.com",
    description="A Python tool for search engine scraping.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishalmohanty/webscraper",
    packages=["webscraper"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[requirements]
)
