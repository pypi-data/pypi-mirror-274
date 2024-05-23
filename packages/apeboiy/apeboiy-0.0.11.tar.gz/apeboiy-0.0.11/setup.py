import os
from setuptools import setup, find_packages

setup(
    name="apeboiy",
    version="0.0.11",
    author="AppleBoiy",
    author_email="contact.chaipat@gmail.com",
    description="Shared AppleBoiy's packages.",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    keywords=["appleboiy", "shared", "packages"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.25.1",
        "numpy>=1.21.0",
    ],
    packages=find_packages(exclude=[]),
    project_urls={"Homepage": "https://github.com/AppleBoiy"},
    test_suite="tests",
    tests_require=["unittest"],
)
