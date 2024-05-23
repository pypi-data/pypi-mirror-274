# setup.pyの例
from setuptools import setup, find_packages

setup(
    name='commute_agci',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'agci=agci:main',
        ],
    },
)
