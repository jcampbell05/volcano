import atexit
from setuptools import setup

def post_install():
    print("Installation complete!")

setup(
    name='volcano',
    version='0.1',
    package_data={
        'volcano': ['*.vsh', '*.vol'],
    },
    entry_points='''
        [console_scripts]
        volcano=volcano.cli:cli
    '''
)

atexit.register(post_install)