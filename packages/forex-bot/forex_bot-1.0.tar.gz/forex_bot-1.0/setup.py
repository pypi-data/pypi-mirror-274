from setuptools import setup, find_packages

setup(
    name='forex_bot',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'MetaTrader5',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'forex_bot=forex_bot.main:main',
        ],
    },
)
