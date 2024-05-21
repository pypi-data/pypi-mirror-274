from setuptools import setup, find_packages
from os import path

cwd = path.abspath(path.dirname(__file__))
with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="lambdatest-playwright-driver",
    version="1.0.0",
    author="LambdaTest <keys@lambdatest.com>",
    description="Python Playwright SDK for visual testing with Smart UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LambdaTest/lambdatest-python-sdk",
    keywords="lambdatest python playwright sdk visual testing",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "playwright>=1.12",
        "lambdatest-sdk-utils",
    ],
    python_requires='>=3.7',  # Playwright requires Python 3.7 or newer
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Testing",
    ],
)
