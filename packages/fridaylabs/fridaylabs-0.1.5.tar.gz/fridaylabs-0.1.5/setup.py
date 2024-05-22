# setup.py
from setuptools import setup, find_packages

setup(
    name="fridaylabs",
    version="0.1.5",
    packages=find_packages(),
    install_requires=["requests"],  # Add any dependencies here
    author="FridayLabs",
    author_email="fridaylabs@fridaylabs.ai",
    description="A package to interact with FridayLabs AI API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ImJustRicky/fridaylabs-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
