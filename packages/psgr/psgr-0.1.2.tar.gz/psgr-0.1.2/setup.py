from setuptools import setup, find_packages

setup(
    name='psgr',
    version='0.1.2',
    description='A password manager application',
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
            'passman = passman.main:main',
        ],
    },
)
