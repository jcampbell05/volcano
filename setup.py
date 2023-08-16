from setuptools import setup

setup(
    name='volcano',
    version='0.1',
    package_data={
        'volcano': ['*.vsh', '*.vol'],
    },
    entry_points='''
        [console_scripts]
        volcano=volcano.cli:cli
    ''',
)