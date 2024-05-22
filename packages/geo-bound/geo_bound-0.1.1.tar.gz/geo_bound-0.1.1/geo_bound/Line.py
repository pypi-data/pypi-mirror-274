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

from utils import treat_data, io


class Line:
    """
    Represents a collection of coordinates that forms a geospatial line.
    """
    def __init__(self, title='', shape=None, file_name=''):
        if file_name != '':
            title, shape = self._get_from_file(file_name)

        self.title: str = title
        self.shape: list = treat_data.digest_coordinates(self.title, shape)
        self._check_line()

    @property
    def segments(self) -> list:
        """
        An organized form of all segments that forms the object.
        :returns: Tuples of two sequential coordinates from the object
        that forms a segment.
        """
        segments = []
        for i in range(len(self.shape) - 1):
            segment = (self.shape[i], self.shape[i + 1])
            segments.append(segment)
        return segments

    def _check_line(self) -> None:
        """
        Verify for duplicates of the coordinates in the shape.
        Raises AssertionError if any is found.
        """
        for point in self.shape:
            assert self.shape.count(point) == 1, (
                'The line has duplicated points.'
            )

    @staticmethod
    def _get_from_file(path: str) -> tuple:
        """
        Extracts the data from the json/geojson file passed and       _
        returns the shape and name of the first line found.
        :param path: The path of the file that has the data
        :return:  A <tuple(2)> with the name and coordinates set of   _
        the line.
        """
        features = io.get_single_line(path)
        return (
            features[0]['properties']['Name'],
            features[0]['geometry']['coordinates']
        )
