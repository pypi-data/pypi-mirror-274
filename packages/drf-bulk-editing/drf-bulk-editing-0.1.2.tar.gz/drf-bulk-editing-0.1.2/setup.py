from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='drf-bulk-editing',
    version='0.1.2',
    packages=['drf-bulk-editing'],
    entry_points={
        'console_scripts': [
            'entry_point=main:hello_world',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
