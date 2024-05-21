from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name="roscpp",
    version="1.15.11.1",
    packages=find_packages(),
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple example package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/roscpp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
