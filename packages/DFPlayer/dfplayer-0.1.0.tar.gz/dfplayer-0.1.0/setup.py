from setuptools import find_packages, setup

setup(
    name='DFPlayer',
    packages=find_packages(exclude=['tests', 'assets']),
    version='0.1.0',
    description='Python3 library for the DFPlayer-mini',
    author='Dianudi',
    url="https://github.com/dianudi/dfplayer-py",
    keywords=['dfplayer', 'dfplayer-mini', 'mp3-module'],
    license='MIT',
    requires=['pyserial'],
)
