from setuptools import setup, find_packages
from os import getenv

setup(
    name='space-exploration-common-lib',
    version=getenv('VERSION', '0.0.1'),
    packages=find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    python_requires='>=3.12, <4',
    include_package_data=True,
    install_requires=[
        'pydantic==2.7.1'
    ],
    author='Steven Hatch',
    author_email='stevegreghatch@gmail.com',
    description='A common library for space exploration projects',
    long_description='A common library for space exploration projects'
)
