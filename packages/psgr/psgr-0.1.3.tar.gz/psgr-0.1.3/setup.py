from setuptools import setup, find_packages

setup(
    name='psgr',
    version='0.1.3',
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
            'passman = psgr.main:main',
            'psgr = psgr.main:main'
        ],
    },
)
