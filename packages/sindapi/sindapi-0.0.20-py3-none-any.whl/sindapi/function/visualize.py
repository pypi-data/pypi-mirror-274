import numpy as np

from matplotlib import pyplot as plt
from pathlib import Path
from matplotlib.collections import LineCollection

from ..sindmap.map_api import SinDStaticMap
from ..sindmap.stretch.stretch import Stretch
from ..sindmap.lane.lane_segment import Lane
from ..sindmap.intersection.intersection import Intersection, IntersectionType
from ..sindmap.utils.map_primitives import Point, Polyline

def draw_polyline(polyline: Polyline, color='green', linestyle='--'):
    plt.plot(polyline.xy[:, 0], polyline.xy[:, 1], color=color, linestyle=linestyle)


def draw_arrow(x, y, color):
    for i in range(len(x) - 1):
        dx = x[i + 1] - x[i]
        dy = y[i + 1] - y[i]
        plt.arrow(x[i], y[i], dx, dy, head_width=0.5, head_length=0.5, fc=color, ec=color)

def draw_lane(lane: Lane, draw_right=True, draw_left=True, right_color='black', left_color='black',
              draw_type='line', linestyle='-', interval=0):
    r_x = [p.x for p in lane.right_lane_boundary.waypoints]
    r_y = [p.y for p in lane.right_lane_boundary.waypoints]
    l_x = [p.x for p in lane.left_lane_boundary.waypoints]
    l_y = [p.y for p in lane.left_lane_boundary.waypoints]
    if interval:
        r_x, r_y, l_x, l_y = r_x[::interval], r_y[::interval], l_x[::interval], l_y[::interval]

    if draw_type == 'line':
        if draw_right:
            plt.plot(r_x, r_y, color=right_color, linestyle=linestyle)
        if draw_left:
            plt.plot(l_x, l_y, color=left_color, linestyle=linestyle)
    elif draw_type == 'arrow':
        if draw_right:
            draw_arrow(r_x, r_y, right_color)
        if draw_left:
            draw_arrow(l_x, l_y, left_color)
    else:
        ValueError

def draw_map(sm: SinDStaticMap, direct_draw=False, dpi=100):
    plt.figure(dpi=dpi)
    for stretch in sm.vector_stretches.values():
        for lane in stretch.vector_lanes.values():
            draw_lane(lane, draw_type='line')

    for intersection in sm.vector_intersections.values():
        if intersection.type == IntersectionType.Straight or intersection.type == IntersectionType.LeftTurn:
            continue
        for lane in intersection.vector_lanes.values():
            if lane.id == 1:
                draw_lane(lane, draw_type='line', draw_right=False, linestyle='--')
            if lane.id == len(intersection.vector_lanes):
                draw_lane(lane, draw_type='line', draw_left=False, linestyle='--')

    if direct_draw:
        plt.show()