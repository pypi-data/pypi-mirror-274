#!/usr/bin/env python
from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
from expviz.version import __version__

setup(
    name='expviz',
    version=__version__,
    description='Visualize experiments tables and figures.',
    url='https://github.com/fuzihaofzh/expviz',
    author='',
    author_email='',
    license='',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Shell env',
    packages=find_packages(),
    install_requires=["matplotlib"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)