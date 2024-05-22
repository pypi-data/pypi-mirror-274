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


def check_coordinate(coordinate: tuple, _id=None) -> None:
    """
    Ensures that the coordinate set passed matches the criteria of a  _
    coordinate point.
    :param coordinate: <tuple(2)> of latitude and longitude
    :param _id: An identification for the point.
    """
    latitude, longitude = coordinate
    if not _id:
        _id = str((latitude, longitude))
    assert type(latitude) == type(longitude) == float, (
        f'Error in {_id}, the values for latitude and longitude must be float.'
    )
    assert -180 < latitude < 180, (
        f'Error in {_id}, the latitude (first value) of point {latitude} is '
        f'invalid (not between -180 and 180).'
    )
    assert -90 < longitude < 90, (
        f'Error in {_id}, the longitude (second value) of point {longitude} '
        f'is invalid (not between -90 and 90).'
    )


def digest_coordinates(title: str, coordinates: list) -> list:
    """
    Asserts that the values for latitude and longitude are valid
    and gets the coordinates of the polygon (often passed as
    `<list(3)>` [which are: lat, lng and alt; since altitude is
    irrelevant, for now, its discarded] to `<tuple(2)>`).
    :param title: The name of the structure
    :param coordinates: list(list(3))
    :return: list(tuple(2))
    """
    new_coordinates = []
    for coordinate in coordinates:
        check_coordinate(coordinate, title)
        new_point = (coordinate[0], coordinate[1])
        new_coordinates.append(new_point)

    return new_coordinates
