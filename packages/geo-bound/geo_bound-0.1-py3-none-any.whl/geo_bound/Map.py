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

from Area import *
from Line import *

MESSAGES = {
    0: 'At least one file must be passed.',
    1: 'Dispersed Charted Field.',
    2: 'Outer area of {}.',
    3: 'Out of charted field.',
    4: 'The point matches {} statement{}: ',
    5: 'Located inside {}',
    6: 'Located on the border of {}',
    7: 'Located on the line {}',
}


class Map:
    """
    Represents a collection of Lines and Areas that forms a
    geospatial map.
    """
    def __init__(
            self, map_name: str, file_map='none.geojson',
            file_areas='none.geojson', file_lines='none.geojson'
    ):
        assert (
                file_areas != 'none.geojson' or
                file_lines != 'none.geojson' or
                file_map != 'none.geojson'
        ), MESSAGES[0]
        io.check_extension(file_map)
        io.check_extension(file_areas)
        io.check_extension(file_lines)
        self.map_name = map_name

        if file_areas == 'none.geojson' == file_lines:
            self._gather_map(file_map)
        elif file_areas != 'none.geojson':
            self.areas = self._gather_areas(file_areas)
        if file_lines != 'none.geojson':
            self.lines = self._gather_lines(file_lines)

        self.map_area = self._join_areas()
        self._sort_areas()

    def locate_point(self, coordinate: tuple, simplify=False) -> str:
        """
        Checks for appearances of the point inside and in the borders _
        of every area in areas and in the line segments of every line _
        in lines.
        :param coordinate: tuple(latitude, longitude).
        :param simplify: boolean to alter the return value from a     _
        verbose (default) to a simple, easier to handle, result.
        :return: A message saying where the point was found or is _
        out of the charted field.
        """
        found_data = []
        for area in self.areas:
            if area.verify_containment(coordinate):
                # The point is inside the area
                found_data.append(('i', f'`{area.title}`.'))
            if area.verify_borderline(coordinate):
                # The point is on the border of the area
                found_data.append(('b', f'`{area.title}`.'))

        for line in self.lines:
            if coordinate == line.shape[0] or coordinate == line.shape[-1]:
                # The point is equal to an end point of the line
                found_data.append(('c', f'`{line.title}`.'))
            elif coordinate in line.shape:
                # The point is equal to a middle point of the line
                found_data.append(('c', f'`{line.title}`.'))
            else:
                for segment in line.segments:
                    if geometry.verify_collinearity(coordinate, segment):
                        # The point is collinear to a segment of the line
                        found_data.append(('c', f'`{line.title}`.'))

        return self._location_message(found_data, simplify)

    def _sort_areas(self) -> None:
        """
        Sorts `self.areas` by the top rightmost point of each area.
        """
        areas_u_r_m_points = {}
        for area in self.areas:
            area_all_points = []
            for point in area.polygon:
                if point not in area_all_points:
                    area_all_points.append(point)

            areas_u_r_m_points[
                self._upper_rightmost_point(area_all_points)
            ] = area

        areas_points_sorted = self._sort_points(areas_u_r_m_points.keys())
        sorted_areas = []
        for point in areas_points_sorted:
            sorted_areas.append(areas_u_r_m_points[point])

        self.areas = sorted_areas

    def _join_areas(self, areas=None) -> str | Area:
        """
        Joins the outer coordinates of the areas that share edges.
        :param areas: list of areas that may will be joined
        :return: A new `Area` object with the points that form the
        outer perimeter
        """
        if not areas:
            areas = self.areas

        all_unique_points, all_edges = (
            self._gather_unique_points_and_edges(areas)
        )
        # Asserting that none of the areas is separate from the rest
        if self._areas_are_separate(all_edges, areas):
            return MESSAGES[1]

        # Determining the upper-rightmost point
        u_r_m_point = self._upper_rightmost_point(all_unique_points)
        # Determining the count of unique edges
        ct_u_edges = self._count_unique_edges(all_edges)
        # Creating the outer polygon with unique edges and following
        # the sequence of edges
        outer_edges = self._create_outer_polygon(
            u_r_m_point, ct_u_edges, all_edges
        )
        # Creating the new polygon with the coordinates found
        new_polygon = [outer_edges[0][0]]
        for edge in outer_edges:
            new_polygon.append(edge[1])

        new_polygon.append(new_polygon[0])
        outer_area_title = MESSAGES[2].format(self.map_name)
        return Area(outer_area_title, new_polygon)

    def _gather_map(self, path: str) -> None:
        """
        Reads the `.geojson`/`.json` file, transforms it in json and  _
        gather the needed data, initiates an `Area` or `Line` for     _
        each shape found, append to its respective list.
        :param path: The location of the file.
        """
        self.lines = self._gather_lines(path)
        self.areas = self._gather_areas(path)

    def _sort_points(self, points: any) -> list:
        """
        Iterates through the points passed and orders from upper      _
        rightmost to bottom leftmost.
        :param points: <list(n)> of points to be sorted.
        :return: <list(n)> of sorted points.
        """
        sorted_points = []
        while True:
            highest_point = (-180, -90)
            for point in points:
                if (
                        point not in sorted_points and
                        self._point_is_higher(point, highest_point)
                ):
                    highest_point = point

            sorted_points.append(highest_point)

            if len(sorted_points) == len(points):
                break

        return sorted_points

    def _upper_rightmost_point(self, unique_points: list) -> tuple:
        """
        Iterates through the values in `unique_points`, verifying if  _
        `Map._point_is_higher()` returns True.
        :param unique_points: A <list(n)> of <tuples(2)> that contain _
        coordinates.
        :return: The upper-rightmost value in the list.
        """
        upper_rightmost_point = (-180, -90)
        for point in unique_points:
            if self._point_is_higher(point, upper_rightmost_point):
                upper_rightmost_point = point

        return upper_rightmost_point

    @staticmethod
    def _gather_unique_points_and_edges(list_of_areas: list) -> tuple:
        """
        Iterates through the list of areas collecting every pair of   _
        coordinates that are unique and the edges of every polygon    _
        from every area in `list_of_areas`.
        :param list_of_areas: <list(n)> of `Area` objects.
        :return: <tuple(2)> with the unique points [0] and the        _
        edges [1].
        """
        unique, borders = [], []
        for area in list_of_areas:
            for point in area.polygon:
                # Gathering every unique point
                if point not in unique:
                    unique.append(point)

            # Gathering every edge
            for border in area.borders:
                borders.append(border)

        return unique, borders

    @staticmethod
    def _location_message(results: list, simplify: bool) -> str:
        """
        Creates the output message for the findings of                _
        `Map.locate_point()`.
        :param results: The simplified version of the findings.
        :param simplify: The message will not be treated if True is   _
        passed.
        :return: A message of where the point was found.
        """
        if len(results) == 0:
            message = MESSAGES[3]
        elif simplify:
            message = ''
            for result in results:
                message += f'{result}\n'
        else:
            message = ''
            c = 1
            for result in results:
                phrase = ''
                if result[0] == 'i':
                    phrase = MESSAGES[5].format(result[1])
                elif result[0] == 'b':
                    phrase = MESSAGES[6].format(result[1])
                elif result[0] == 'c':
                    phrase = MESSAGES[7].format(result[1])
                message += f'\t{c}/{len(results)}:[{phrase}],'
                c += 1

            if c == 2:
                message = MESSAGES[4].format('this', '') + '{' + message + '}'
            else:
                message = MESSAGES[4].format('these', 's') + '{' + message + '}'

        return message

    @staticmethod
    def _areas_are_separate(all_edges: list, list_of_areas: list) -> bool:
        """
        Iterates through the areas in `list_of_areas` and counts its  _
        edges, verifying for any area that is separated from the rest.
        :param all_edges: All edges found in the group of areas.
        :param list_of_areas: All areas that it wishes to check for a _
        connected whole.
        :return: A boolean value for whether any of the areas is      _
        separated.
        """
        for area in list_of_areas:
            unique_count = 0
            borders_count = 0
            for border in area.borders:
                borders_count += 1
                if all_edges.count(border) > 1:
                    break  # At least one of the edges is not unique.
                else:
                    unique_count += 1  # The edge is unique

            if unique_count == borders_count:
                return True  # At least one area has the same count of_
                # edges and edges that are unique.

        return False  # All areas have at least one edge shared with  _
        # another

    @staticmethod
    def _point_is_higher(point: tuple, current_highest: tuple) -> bool:
        """
        Evaluates whether the candidate `point` is higher than the    _
        `current_higher` point, verifying if value for longitude of   _
        the former is greater than the latter or the longitudes are   _
        equal and the latitude of `point` is greater.
        :param point: the point that may be higher.
        :param current_highest: the highest point found so far.
        :return: Whether the point is upper rightmost from            _
        `current_higher`.
        """
        return (
            point[1] > current_highest[1] or (
                point[1] == current_highest[1] and
                point[0] > current_highest[0])
        )

    @staticmethod
    def _create_outer_polygon(
            up_rm_pt: tuple, ct_un_ed: int, edges: list
    ) -> list:
        """
        Iterates through `edges`, appending to a list the edge that   _
        is the next in the logical sequence. To be appended, the edge _
        must either be:
            - the first one to be added and its start the             _
            upper-rightmost point of the set; or
            - the edge must be unique in the set (considering that    _
            every inner-border's point is, at least, duplicated) and  _
            the endpoint of the last edge added is equal to the next  _
            one.
        Once the length of the new outer polygon reaches the count of _
        unique edges, the method halts, returning the finding.
        :param up_rm_pt: Upper-rightmost point in the set.
        :param ct_un_ed: Count of unique edges
        :param edges: All edges that are wished to form the outer     _
        polygon.
        :return: A <list(n)> of with the outer edges.
        """
        outer_edges = []
        last_edge = None
        while True:
            for edge in edges:
                if (
                        (not last_edge and edge[0] == up_rm_pt) or
                        (edges.count(edge) == 1 and last_edge[1] == edge[0])
                ):
                    outer_edges.append(edge)
                    last_edge = edge
                    break

            if len(outer_edges) == ct_un_ed:
                break

        return outer_edges

    @staticmethod
    def _count_unique_edges(edges: list) -> int:
        """
        Iterates through the values in `edges` adding to a count      _
        when the value isn't duplicated in the list.
        :param edges: <list(n)> of edges <tuple(2)<tuple(2)>>
        :return: The number of unique edges found.
        """
        count = 0
        for edge in edges:
            if edges.count(edge) == 1:
                count += 1

        return count

    @staticmethod
    def _gather_lines(path: str) -> list:
        """
        Reads the `.geojson`/`.json` file, transforms it in json and  _
        gather the needed data, initiates an `Line` for     _
        each shape found, append to the list.
        :param path: The location of the file
        :return: A list containing the `Line` objects found.
        """
        lines = []
        lines_dict = io.get_multiple_lines(path)
        for line_key in lines_dict:
            lines.append(Line(line_key, lines_dict[line_key]))

        return lines

    @staticmethod
    def _gather_areas(path: str) -> list:
        """
        Reads the `.geojson`/`.json` file, transforms it in json and  _
        gather the needed data, initiates an `Area` for     _
        each shape found, append to the list.
        :param path: The location of the file
        :return: A list containing the `Area` objects found.
        """
        areas = []
        areas_dict = io.get_multiple_areas(path)
        for area_key in areas_dict:
            areas.append(Area(area_key, areas_dict[area_key]))

        return areas
