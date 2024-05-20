from setuptools import setup, find_packages

setup(
    name='hebing-code',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hebingcode=hebingcode.merger:main',
        ],
    },
)
