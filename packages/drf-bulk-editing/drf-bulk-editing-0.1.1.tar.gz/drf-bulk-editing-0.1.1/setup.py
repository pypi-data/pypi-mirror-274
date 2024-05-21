from setuptools import setup

setup(
    name='drf-bulk-editing',
    version='0.1.1',
    packages=['drf-bulk-editing'],
    entry_points={
        'console_scripts': [
            'entry_point=main:hello_world',
        ],
    },
)
