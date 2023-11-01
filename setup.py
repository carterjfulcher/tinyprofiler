from setuptools import setup, find_packages

setup(
    name="tinyprofiler",
    version="0.1.5",
    description="A Profiling Library for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Carter Fulcher",
    author_email="fulcher.carter@gmail.com",
    packages=find_packages(),
)