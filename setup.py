import os
from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        os.system("./build_examples.vol")

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
    cmdclass={
        'install': PostInstallCommand
    },
)