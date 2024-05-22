from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="remla24-team7-app",
    version='0.0.2',
    url='https://github.com/remla24-team7/app',
    author='Arjun Vilakathara',
    description='App for assigment 2 of REMLA',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['frontend', 'backend'],
)
