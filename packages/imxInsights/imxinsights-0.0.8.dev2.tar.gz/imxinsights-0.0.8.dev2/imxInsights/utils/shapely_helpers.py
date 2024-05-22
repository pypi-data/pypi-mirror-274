from __future__ import annotations

import math
from typing import List, Union

import numpy as np
import pyproj
from shapely.geometry import LineString, Point, Polygon


def gml_point_to_shapely(gml_point_coordinates: str) -> Point:
    """
    Converts a GML point coordinate string to a Shapely Point object.

    Args:
        gml_point_coordinates (str): The GML point coordinate string in the format "(x,y)".

    Returns:
        (Shapely.Point): The Shapely Point object.

    """
    coordinates = [float(x) for x in gml_point_coordinates.replace("(", "").replace(")", "").replace("'", "").replace(" ", "").split(",")]
    return Point(coordinates)


def shapely_point_to_gml(shapely_point: Point):
    """
    Converts a Shapely Point object to a GML point coordinate string.

    Args:
        shapely_point (Point): The Shapely point".

    Returns:
        (str): gml:point string representation.

    """
    if shapely_point.has_z:
        return f"{round(shapely_point.x, 3)},{round(shapely_point.y, 3)},{round(shapely_point.z, 3)}"
    else:
        return f"{round(shapely_point.x, 3)},{round(shapely_point.y, 3)}"


def gml_linestring_to_shapely(gml_linestring_coordinates: str) -> LineString:
    """
    Converts a GML linestring coordinate string to a Shapely LineString object.

    Args:
        gml_linestring_coordinates (str): A string of GML linestring coordinates in "x,y" format separated by spaces.

    Returns:
        (Shapely.LineString): A Shapely LineString object.

    """
    return LineString([tuple(map(float, x.split(","))) for x in gml_linestring_coordinates.split(" ")])


def gml_polygon_to_shapely(gml_linestring_coordinates: str) -> Polygon:
    """
    Converts a GML polygon to a Shapely Polygon object.

    Args:
        gml_linestring_coordinates (str): A string containing the GML coordinates of the polygon.

    Returns:
        (Polygon): A Shapely Polygon object.

    """
    return Polygon([tuple(map(float, x.split(","))) for x in gml_linestring_coordinates.split(" ")])


class ShapelyTransform:
    """A utility class to transform between RD and WGS84 coordinate systems."""

    rd = pyproj.CRS("EPSG:28992")
    wgs = pyproj.CRS("EPSG:4326")
    transformer_to_wgs = pyproj.Transformer.from_crs(rd, wgs)
    transformer_to_rd = pyproj.Transformer.from_crs(wgs, rd)

    @classmethod
    def rd_to_wgs(cls, shapely: Union[Point, LineString, Polygon]) -> Union[Point, LineString, Polygon]:
        """
        Convert a Shapely geometry from Dutch RD (Rijksdriehoekstelsel) coordinates (EPSG:28992) to WGS84 coordinates (EPSG:4326).

        Args:
            shapely (Union[Point, LineString, Polygon]): A Shapely geometry in Dutch RD coordinates.

        Returns:
            (Union[Point, LineString, Polygon]): A Shapely geometry in WGS84 coordinates.

        """
        return cls._convert(shapely, cls.transformer_to_wgs)

    @staticmethod
    def _convert(shapely: Union[Point, LineString, Polygon], transformer: pyproj.Transformer) -> Union[Point, LineString, Polygon]:
        if isinstance(shapely, Point):
            return Point(*reversed(transformer.transform(shapely.x, shapely.y)))

        elif isinstance(shapely, LineString):
            return LineString(zip(*reversed(transformer.transform(*shapely.coords.xy))))

        elif isinstance(shapely, Polygon):
            return LineString(zip(*reversed(transformer.transform(*shapely.exterior.coords.xy))))
        else:
            return shapely


def reverse_line(shapely_polyline: LineString) -> LineString:
    """
    Reverses the order of coordinates in a Shapely LineString object.

    Args:
        shapely_polyline (LineString): The LineString object to reverse.

    Returns:
        (LineString): A new LineString object with the coordinates in reverse order.

    """
    return LineString(list(shapely_polyline.coords)[::-1])


def get_azimuth_from_points(point1: Point, point2: Point) -> float:
    """
    Calculates the azimuth angle between two points.

    Args:
        point1 (Point): The first Point object.
        point2 (Point): The second Point object.

    Returns:
        (float): The azimuth angle in degrees.

    """
    angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
    return float(np.degrees(angle)) if angle >= 0 else float(np.degrees(angle) + 360)


def check_point_in_area(point_str: str, area: Polygon):
    point_to_test = Point([float(item) for item in point_str.split(",")])
    return point_to_test.within(area)


def cut(line: LineString, distance: float) -> List[LineString]:
    # todo: if 0 then its not working... sho
    if distance == 0:
        return [line]

    # todo: move to shapley helpers
    # Cuts a 3d line in two at a distance from its starting point
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coordinates = list(line.coords)
    for i, p in enumerate(coordinates):
        pd = line.project(Point(p))
        if pd == distance:
            return [LineString(coordinates[: i + 1]), LineString(coordinates[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            # todo: check if z present, if not switch and do not use z
            return [LineString(coordinates[:i] + [(cp.x, cp.y, cp.z)]), LineString([(cp.x, cp.y, cp.z)] + coordinates[i:])]


def cut_profile(line: LineString, measure_from: float, measure_to: float) -> LineString:
    if measure_from > measure_to:
        measure_from, measure_to = measure_to, measure_from
    if measure_from == 0:
        new_line = line
    else:
        new_line = cut(line, measure_from)[1]

    point = line.interpolate(measure_to)
    new_measure = new_line.project(point)
    result = cut(new_line, new_measure)[0]
    return result


def offset_linestring(line: LineString, distance: float, direction: str) -> LineString:
    # Extract coordinates from LineString
    coords = np.array(line.coords)

    # Calculate direction vector
    direction_vector = np.array([coords[-1][0] - coords[0][0], coords[-1][1] - coords[0][1]])
    direction_vector = direction_vector / np.linalg.norm(direction_vector)

    # Calculate perpendicular vector
    if direction == "up":
        perpendicular_vector = np.array([-direction_vector[1], direction_vector[0]])  # Rotate by 90 degrees clockwise
    elif direction == "down":
        perpendicular_vector = np.array([direction_vector[1], -direction_vector[0]])  # Rotate by 90 degrees counterclockwise
    else:
        raise ValueError("Direction must be 'up' or 'down'.")

    offset_coords = []
    for coord in coords:
        new_coord = coord + distance * perpendicular_vector
        offset_coords.append((new_coord[0], new_coord[1]))

    return LineString(offset_coords)


def extend_line(start_point, end_point, extension_meters, extend_from="both"):
    # todo: add typehints
    """
    Extends a line defined by start and end points by a certain number of meters in specified direction(s).

    :param start_point: Tuple (x, y) representing the start point of the line.
    :param end_point: Tuple (x, y) representing the end point of the line.
    :param extension_meters: Number of meters to extend the line.
    :param extend_from: Direction to extend the line ('start', 'end', 'both').
    :return: A Shapely LineString object representing the extended line.
    """
    # Convert points to Shapely Points
    start = Point(start_point)
    end = Point(end_point)

    # Calculate the direction vector and its magnitude
    dx = end.x - start.x
    dy = end.y - start.y
    length = math.sqrt(dx**2 + dy**2)

    # Normalize the direction vector
    dx_normalized = dx / length
    dy_normalized = dy / length

    # Initialize new start and end points as the original ones
    new_start = Point(start.x, start.y)
    new_end = Point(end.x, end.y)

    # Calculate the extension in terms of the line's coordinate system
    extension_dx = dx_normalized * extension_meters
    extension_dy = dy_normalized * extension_meters

    # Extend the line as specified
    if extend_from == "start" or extend_from == "both":
        new_start = Point(start.x - extension_dx, start.y - extension_dy)
    if extend_from == "end" or extend_from == "both":
        new_end = Point(end.x + extension_dx, end.y + extension_dy)

    # Create and return the extended LineString
    extended_line = LineString([new_start, new_end])
    return extended_line


def point_relative_to_linestring(linestring, point):
    # todo: add typehints
    """
    Determines if a point is to the left or right of a LineString considering its drawing direction.

    :param linestring: Shapely LineString object.
    :param point: Shapely Point object to check.
    :return: 'left', 'right', or 'on' indicating the point's position relative to the LineString.
    """
    # Ensure the LineString has at least two points to define a direction
    if len(linestring.coords) < 2:
        raise ValueError("LineString must have at least two points.")

    # Use the first segment of the LineString to determine direction
    start_point = Point(linestring.coords[0])
    direction_point = Point(linestring.coords[1])

    # Vector from start_point to direction_point
    vector_a = (direction_point.x - start_point.x, direction_point.y - start_point.y)

    # Vector from start_point to the input point
    vector_b = (point.x - start_point.x, point.y - start_point.y)

    # Cross product of vector_a and vector_b
    cross_product = vector_a[0] * vector_b[1] - vector_a[1] * vector_b[0]

    # Determine position based on the sign of the cross product
    if cross_product > 0:
        return "left"
    elif cross_product < 0:
        return "right"
    else:
        return "on"


def calculate_vector(linestring):
    """Calculate vector from a linestring."""
    start_point = np.array(linestring.coords[0])
    end_point = np.array(linestring.coords[-1])
    vector = end_point - start_point
    return vector


def normalize_vector(vector):
    """Normalize a vector."""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def are_linestrings_in_same_direction(linestrings):
    """Check if all linestrings are in the same direction."""
    vectors = [calculate_vector(ls) for ls in linestrings]
    normalized_vectors = [normalize_vector(v) for v in vectors]

    # Compare vectors by dot product
    reference_vector = normalized_vectors[0]
    for vector in normalized_vectors[1:]:
        dot_product = np.dot(reference_vector, vector)
        if dot_product < 0:  # Vectors are in opposite directions
            return False
    return True


def reproject_point_to_line(point: Point, line: LineString) -> Point:
    return line.interpolate(line.project(point))


# def shared_segments(line1: LineString, line2: LineString) -> Tuple[LineString, LineString]:
#     segments1 = [LineString((line1.coords[i], line1.coords[i + 1])) for i in range(len(line1.coords) - 1)]
#     segments2 = [LineString((line2.coords[i], line2.coords[i + 1])) for i in range(len(line2.coords) - 1)]
#
#     shared1 = [_ for _ in segments1 if _.intersects(line2)]
#     shared2 = [_ for _ in segments2 if _.intersects(line1)]
#
#     if len(shared1) != 1 or len(shared2) != 1:
#         raise ValueError("None, or more shared")
#
#     return shared1[0], shared2[0]
#
#
# def get_farthest_points(line1: LineString, line2: LineString) -> Tuple[Tuple[float, float], Tuple[float, float]]:
#     # Find the point on line1 farthest from line2
#     farthest_point_line1 = max(line1.coords, key=lambda p: line2.distance(Point(p[0], p[1])))
#
#     # Find the point on line2 farthest from line1
#     farthest_point_line2 = max(line2.coords, key=lambda p: line1.distance(Point(p[0], p[1])))
#
#     return farthest_point_line1, farthest_point_line2
