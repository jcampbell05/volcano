from setuptools import setup

setup(
    name='volcano',
    version='0.1',
    py_modules=['volcano'],
    entry_points='''
        [console_scripts]
        volcano=volcano:cli
    ''',
    install_requires=['typed_ast']
)