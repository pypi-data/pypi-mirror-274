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

from utils import treat_data, geometry, io


class Area:
    """
    Represents a collection of coordinates that forms a geospatial
    polygon.
    """
    def __init__(self, title='', polygon=None, file_name=''):
        if file_name != '':
            title, polygon = self._get_from_file(file_name)

        self.title = title
        self.polygon = treat_data.digest_coordinates(self.title, polygon)
        assert self.polygon[0] == self.polygon[-1], (
            f'The polygon of {self.title} is open.'
        )

    @property
    def borders(self) -> list:
        """
        Every pair of coordinates in the polygon that are sequential.
        """
        borders = []
        for i in range(len(self.polygon) - 1):
            border = (self.polygon[i], self.polygon[i + 1])
            borders.append(border)
        return borders

    def verify_containment(self, coordinate: tuple) -> bool:
        """
        Asserts that the coordinate is valid, verify the coordinate's _
        appearance in its polygon, run the calculations necessary to  _
        verify if the point is inside the polygon.
        :param coordinate: tuple(latitude, longitude)
        :return: Boolean value for the point being part of the polygon_
        or its area
        """
        treat_data.check_coordinate(coordinate)
        return geometry.point_in_poly(coordinate, self.polygon)

    def verify_borderline(self, coordinate: tuple) -> bool:
        """
        Iterates through the borders of the object, verifying if the  _
        coordinate point is collinear to the segments.
        :param coordinate: A <tuple(2)> of latitude and longitude.
        :return: Whether the point is on the border of Self or not.
        """
        for border in self.borders:
            if geometry.verify_collinearity(coordinate, border):
                return True

        return False

    @staticmethod
    def _get_from_file(path: str) -> tuple:
        """
        Gets the data needed from a `.geojson` or `.json` file.
        :param path: The path to the file
        """
        feature = io.get_single_area(path)
        return (
            feature[0]['properties']['name'],
            feature[0]['geometry']['coordinates'][0]
        )
