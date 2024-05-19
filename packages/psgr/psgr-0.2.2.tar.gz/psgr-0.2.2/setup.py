from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='psgr',
    version='0.2.2',
    description='A password manager application',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Naresh Karthigeyan',
    author_email='nareskarthigeyan.2005@gmail.com',
    packages=find_packages(),
    install_requires=[
        'tabulate',
        'rsa',
        'InquirerPy'
    ],
    entry_points={
        'console_scripts': [
            'passman = psgr.main:main',
            'psgr = psgr.main:main'
        ],
    },
)