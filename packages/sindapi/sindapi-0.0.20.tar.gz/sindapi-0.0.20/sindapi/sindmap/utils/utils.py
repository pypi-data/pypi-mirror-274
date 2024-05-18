
from typing import List

from .map_primitives import Point


def sign(p1: Point, p2: Point, p3: Point):
    return (p1.x - p3.x) * (p2.y - p3.y) - \
        (p2.x - p3.x) * (p1.y - p3.y)


def is_point_on_line(p: Point, p1: Point, p2: Point):
    if p1.x == p2.x:
        return p.x == p1.x

    k = (p2.y - p1.y) / (p2.x - p1.x)

    return p.y == p1.y + k * (p.x - p1.x)

def point_in_triangle(point: Point, corners: List[Point]) -> bool:
    if point in corners:
        return True
    if is_point_on_line(point, corners[0], corners[1])\
            or is_point_on_line(point, corners[1], corners[2])\
            or is_point_on_line(point, corners[2], corners[0]):
        return True

    d1 = sign(point, corners[0], corners[1])
    d2 = sign(point, corners[1], corners[2])
    d3 = sign(point, corners[2], corners[0])

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)


def point_in_box(point: Point, corners: List[Point]) -> bool:
    triangle1 = corners[:3]
    triangle2 = [corners[i] for i in [2, 3, 0]]

    is_in1 = point_in_triangle(point, triangle1)
    is_in2 = point_in_triangle(point, triangle2)

    return is_in1 or is_in2

def split_unique_id(segment_id: str):
    return int(segment_id[0:2]), int(segment_id[2:4]), int(segment_id[4:8])

