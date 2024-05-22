"""
(PT-BR)
    Geolocalização e Georreferenciamento com poligonos
(EN-US)
    Geolocation and Georefferencing with polygons
Copyright (C) 2024 Thiago Daniel Pessoa

This program is free software: you can redistribute it and/or modify it _
under the terms of the GNU General Public License as published by the   _
Free Software Foundation, either version 3 of the License, or (at your  _
option) any later version.

This program is distributed in the hope that it will be useful, but     _
WITHOUT ANY WARRANTY; without even the implied warranty of              _
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU        _
General Public License for more details.

You should have received a copy of the GNU General Public License along _
with this program. If not, see <https://www.gnu.org/licenses/>.
"""


import pathlib
from setuptools import (
    setup, 
    find_packages
)

setup(
    name='geo_bound',
    version='0.1.1',
    description='Location of coordinates in geospatial maps.',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/TDPessoa/geolocation-with-coordinates',
    license='GPL-3.0 license',
    author='TDPessoa',
    author_email='thiago.d.pessoa@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Free To Use But Restricted',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Localization',
        'Topic :: Utilities'
    ],
    python_requires=">=3.11,<3.14",


)
