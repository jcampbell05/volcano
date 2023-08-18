import os
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop

class PostInstallCommand(install):

    def run(self):
        install.run(self)
        os.system("./build_examples.vol")

class PostDevelopCommand(develop):

    def run(self):
        post_install = self.get_finalized_command('install')
        post_install.run()
        
        os.system("pip install shellcheck-py")

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
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
    },
)