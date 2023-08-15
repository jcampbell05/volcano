from setuptools import setup

setup(
    name='volcano',
    version='0.1',
    py_modules=['volcano'],
    package_data={
        'volcano': ['image.png'],
    },
    entry_points='''
        [console_scripts]
        volcano=volcano:cli
    ''',
)