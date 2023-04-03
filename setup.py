from distutils.core import setup

from setuptools import find_packages


setup(
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    download_url='https://github.com/erolyesin/logger-wrapper/archive/refs/tags/v0.0.1-rc01.tar.gz',
)
