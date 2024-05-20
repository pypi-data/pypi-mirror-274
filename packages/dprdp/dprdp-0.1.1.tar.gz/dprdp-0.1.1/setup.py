# coding=utf-8
from setuptools import setup
from setuptools import find_packages

VERSION = '0.1.1'

setup(
    name='dprdp',
    version=VERSION,
    description='my package',
    packages=find_packages(),
    install_requires=[
		'unicrypto>=0.0.10,<=0.1.0',
		'minidump>=0.0.21,<=0.1.0',
		'minikerberos>=0.4.1,<=0.5.0',
		'winacl>=0.1.9,<=0.2.0',
	]
)
