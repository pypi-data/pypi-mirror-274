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


def point_in_poly(point: tuple, polygon: list) -> bool:
    """
    Iterates through the `polygon`'s items, counting if the ray of    _
    intersection calculated for item and the point is greater than    _
    the point's first value. When the count ends in an odd number,    _
    the point is inside the polygon.
    :param point: <tuple(2)> of latitude and longitude
    :param polygon: <list(n)<tuple(2)>> of latitudes and longitudes
    :return: Whether the point is inside or outside the polygon.
    """
    point_to_end_right_segment = (point, (point[0], 180))
    is_inside = False
    for i in range(len(polygon)):
        current_segment = (polygon[i], polygon[(i + 1) % len(polygon)])
        # The Mod is  used to ensure that the zero index value is
        # called when the index for the last item is reached.
        if verify_intersection(point_to_end_right_segment, current_segment):
            is_inside = not is_inside

    return is_inside


def verify_collinearity(point_a: tuple, segment_bc: tuple) -> bool:
    """
    Tells whether a point lies on a line segment.

    :param point_a: The coordinate point (latitude, longitude) to be
    checked for collinearity with the segment.
    :param segment_bc: Two endpoints of the line segment (latitudes,
    longitudes) to which the point may be collinear.
    :return: True if the point is collinear with the segment, False
    otherwise.
    """
    segment_ab = (point_a, segment_bc[0])
    slope_bc = calculate_slope(segment_bc)
    slope_ab = calculate_slope(segment_ab)
    return slope_ab == slope_bc


def round_point(point: tuple) -> tuple:
    """
    Rounds the point's longitude and latitude to the 6th decimal place.
    :param point: <tuple(2)> of longitude and latitude.
    :return: The rounded coordinates.
    """
    return (
        round(point[0], 6),
        round(point[1], 6)
    )


def calculate_slope(segment: tuple) -> float:
    """
    Divides the vertical change (rise) by the horizontal change (run)
    of the segment.
    :param segment: <tuple(2)<tuple(2)>> of two coordinates points.
    :return: the value of the slope between the points.
    """
    x_a, y_a = round_point(segment[0])
    x_b, y_b = round_point(segment[1])
    if x_a == x_b:
        slope = 0

    else:
        slope = (y_b - y_a) / (x_b - x_a)

    return round(slope, 2)


def verify_intersection(segment_a: tuple, segment_b: tuple) -> bool:
    """
    Tells whether two lines crosses.

    :param segment_a: First line's coordinates points for start and end.
    :param segment_b: Second line's coordinates points for start and end.
    :return: True if the lines crosses and False if not.
    """
    # Breaking the segments into its coordinate points.
    lineA_pointA, lineA_pointB = segment_a
    lineB_pointA, lineB_pointB = segment_b

    # Calculating the vectors for the lines
    vector_A = (
        lineA_pointB[0] - lineA_pointA[0],
        lineA_pointB[1] - lineA_pointA[1]
    )
    vector_B = (
        lineB_pointB[0] - lineB_pointA[0],
        lineB_pointB[1] - lineB_pointA[1]
    )

    determinant = vector_A[0] * vector_B[1] - vector_A[1] * vector_B[0]
    if determinant == 0:
        return False  # The segments are parallel to each other

    # Calculating the parameters s and t
    s = (
        (
            (lineB_pointA[0] - lineA_pointA[0]) * vector_B[1] -
            (lineB_pointA[1] - lineA_pointA[1]) * vector_B[0]
        ) / determinant
    )
    t = (
        (
            (lineB_pointA[0] - lineA_pointA[0]) * vector_A[1] -
            (lineB_pointA[1] - lineA_pointA[1]) * vector_A[0]
        ) / determinant
    )

    return 0 <= s <= 1 and 0 <= t <= 1
