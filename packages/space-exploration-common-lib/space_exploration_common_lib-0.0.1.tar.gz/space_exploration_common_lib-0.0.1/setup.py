from setuptools import setup, find_packages
from os import getenv

setup(
    name='space-exploration-common-lib',
    version=getenv('VERSION', default='v0.0.1'),
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.12, <4',
    include_package_data=True,
    install_requires=[
        'pydantic==2.7.1'
    ],
    author='Steven Hatch',
    author_email='stevegreghatch@gmail.com'
)
