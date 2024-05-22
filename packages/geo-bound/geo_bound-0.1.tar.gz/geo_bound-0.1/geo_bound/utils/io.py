"""
    GeoBound
(PT-BR)
    Identificação de coordenadas e geolocalização de polígonos e linhas.
(EN-US)
    Identification of coordinates and geolocation of polygons and lines.

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

import json

VALID_EXTENSIONS = ['geojson', 'json']
MESSAGES = {
    0: "The file's extension is unsupported: [`{}`].",
    1: 'The file `{}` must contain exactly one feature and it must be a '
       '`Polygon`.',
    2: 'The file `{}` must contain exactly one feature and it must be a '
       '`LineString`.',
    3: 'The file `{}` must contain at least one structure'
}


class InvalidFileExtension(Exception):
    """
    Handles the Exception call if an invalid extension is passed.
    """
    def __init__(self, file_name: str):
        message = MESSAGES[0].format(file_name)
        super().__init__(message)


def extract_data_from_file(file_path: str) -> str:
    """
    Reads the lines in the file and returns it as one single string.
    :param file_path: Path and name to the file
    :return: Text of the file
    """
    check_extension(file_path)
    file_data = ''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                file_data += line
    except FileNotFoundError:
        pass

    return file_data


def get_single_area(file_path: str) -> None | dict:
    """
    Collects the data from a file containing a single area.
    :param file_path: Path and name to the file
    :return: The json in the file data
    """
    file_data = extract_data_from_file(file_path)
    features = json.loads(file_data)['features']
    assert len(features) == 1 and file_data.count('Polygon') == 1, (
        MESSAGES[1].format(file_path)
    )
    return features


def get_multiple_areas(file_path: str) -> None | dict:
    """
    Collects the data from a file containing more than one area.
    :param file_path: Path and name to the file.
    :return: A dict containing the name of each structure as key and
    its perimeter as value.
    """
    file_data = extract_data_from_file(file_path)
    features = json.loads(file_data)['features']
    assert len(features) >= 1, (
        MESSAGES[3].format(file_path)
    )
    items_found = {}
    for feature in features:
        geometry = feature['geometry']
        if geometry['type'] == 'Polygon':
            name = feature['properties']['Name']
            coordinates = geometry['coordinates'][0]
            items_found[name] = coordinates

    return items_found


def get_single_line(file_path: str) -> None | dict:
    """
    Collects the data from a file containing a single line.
    :param file_path: Path and name to the file.
    :return: The json in the file data.
    """
    file_data = extract_data_from_file(file_path)
    features = json.loads(file_data)['features']
    assert len(features) == 1 and file_data.count('LineString') == 1, (
        MESSAGES[2].format(file_path)
    )
    return features


def get_multiple_lines(file_path: str) -> None | dict:
    """
    Collects the data from a file containing more than one line.
    :param file_path: Path and name to the file.
    :return: A dict containing the name of each structure as key and
    its shape as value.
    """
    file_data = extract_data_from_file(file_path)
    features = json.loads(file_data)['features']
    assert len(features) >= 1, (
        MESSAGES[3].format(file_path)
    )
    items_found = {}
    for feature in features:
        geometry = feature['geometry']
        if geometry['type'] == 'LineString':
            name = feature['properties']['Name']
            coordinates = geometry['coordinates']
            items_found[name] = coordinates

    return items_found


def check_extension(file_path: str) -> None:
    """
    Checks the path for the valid extensions.
    :param file_path: Path and name to the file
    """
    ext = file_path.split('.')[-1]
    if ext not in VALID_EXTENSIONS:
        raise InvalidFileExtension(file_path)
