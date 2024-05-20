from setuptools import setup

with open("README.rst","r") as f:
    long_description = f.read()

setup(
    name='dzidb',
    version='1.0',
    long_description=long_description,
    py_modules=['dzidb'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dzidb = dzidb:main',
        ]
    }
)