from setuptools import find_packages, setup

setup(
    name='WebsJSON',
    packages=find_packages(include=['WebsJSON']),
    version='0.1.1',
    description='Library to make functions for json messages over websockets',
    author='R2Boyo25',
    license='GPLV3',
    install_requires=['websockets']
)