import json
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


from .drivable_area import DrivableArea
from .pedestrian_crossing import PedestrianCrossing
from .stretch.stretch import Stretch
from .intersection.intersection import Intersection
from .lane.lane_segment import Lane, LaneSegment
from .traffic_light.traffic_light import TrafficLight
from .utils.map_primitives import Point, Polyline
from .utils.utils import point_in_box


@dataclass
class SinDStaticMap:
    city_name: str
    vector_drivable_areas: Dict[int, DrivableArea]
    vector_pedestrian_crossings: Dict[int, PedestrianCrossing]
    vector_stretches: Dict[int, Stretch]
    vector_intersections: Dict[int, Intersection]
    vector_lane_segments: Dict[int, LaneSegment]
    map_id: Optional[str] = None
    split_distance: float = None
    segment_point_num: int = None

    @classmethod
    def from_cfg(cls, config_path):
        with config_path.open('r') as file:
            config = yaml.safe_load(file)

        cls.split_distance = config['split_distance']
        cls.segment_point_num = config['segment_point_num']

    @classmethod
    def from_json(cls, map_data_path: Path):
        with map_data_path.open('r') as file:
            map_data = json.load(file)
        return map_data

    @classmethod
    def build(cls, sind_path: Path) -> 'SinDStaticMap':
        sind_map_path = sind_path / 'map'
        cls.from_cfg(sind_map_path / 'config.yaml')
        map_data = cls.from_json(sind_map_path / 'static_map.json')

        vector_stretches = cls.build_stretches(map_data['stretch'])
        vector_intersections, vector_stretches = cls.build_intersections(map_data['intersection'], vector_stretches)
        vector_drivable_areas = cls.build_drivable_areas()
        vector_pedestrian_crossings = cls.build_pedestrian_crossings()
        vector_lane_segments = cls.get_lane_segments(vector_stretches, vector_intersections)

        return cls(
            city_name=sind_path.stem,
            vector_stretches=vector_stretches,
            vector_intersections=vector_intersections,
            vector_lane_segments=vector_lane_segments,
            vector_drivable_areas=vector_drivable_areas,
            vector_pedestrian_crossings=vector_pedestrian_crossings
        )

    @classmethod
    def build_drivable_areas(cls):
        return {0: DrivableArea.build()}

    @classmethod
    def build_stretches(cls, stretches_data: List[Dict]) -> Dict[int, Stretch]:
        vector_stretches = {}
        for _, data in enumerate(stretches_data):
            data.update({
                'split_distance': cls.split_distance,
                'segment_point_num': cls.segment_point_num
            })
            stretch = Stretch.build(data)
            vector_stretches[stretch.id] = stretch

        return vector_stretches

    @classmethod
    def build_intersections(cls, intersections_data: List[Dict],
                            vector_stretches: Dict[int, Stretch]) -> Dict[int, Intersection]:
        vector_intersections = {}
        for _, data in enumerate(intersections_data):
            data.update({
                'split_distance': cls.split_distance,
                'segment_point_num': cls.segment_point_num,
                'vector_stretches': vector_stretches
            })
            intersection, vector_stretches = Intersection.build(data)
            vector_intersections[intersection.id] = intersection

        return vector_intersections, vector_stretches

    @classmethod
    def build_pedestrian_crossings(cls):
        return {0: PedestrianCrossing.build()}

    @classmethod
    def get_lane_segments(cls, vector_stretches, vector_intersections):
        lane_segments = {}
        for _, stretch in vector_stretches.items():
            for _, lane in stretch.vector_lanes.items():
                for _, segment in lane.vector_lane_segments.items():
                    lane_segments[segment.unique_id] = segment

        for _, intersection in vector_intersections.items():
            for _, lane in intersection.vector_lanes.items():
                for _, segment in lane.vector_lane_segments.items():
                    lane_segments[segment.unique_id] = segment

        return lane_segments

    def locate_point_lane_segment(self, point: Point):
        for stretch in self.vector_stretches.values():
            right_lane = stretch.vector_lanes[len(stretch.vector_lanes)]
            left_lane = stretch.vector_lanes[1]
            corners = []
            corners.append(right_lane.get_start_point()[0])
            corners.append(right_lane.get_end_point()[0])
            corners.append(left_lane.get_end_point()[1])
            corners.append(left_lane.get_start_point()[1])

            if not point_in_box(point, corners):
                continue

            for lane in stretch.vector_lanes.values():
                corners = []
                corners.append(lane.get_start_point()[0])
                corners.append(lane.get_end_point()[0])
                corners.append(lane.get_end_point()[1])
                corners.append(lane.get_start_point()[1])

                if not point_in_box(point, corners):
                    continue

                for segment in lane.vector_lane_segments.values():
                    corners = []
                    corners.append(segment.right_lane_segment_boundary.waypoints[0])
                    corners.append(segment.right_lane_segment_boundary.waypoints[-1])
                    corners.append(segment.left_lane_segment_boundary.waypoints[-1])
                    corners.append(segment.left_lane_segment_boundary.waypoints[0])

                    if not point_in_box(point, corners):
                        continue
                    return segment.unique_id

        return None

    def is_point_in_intersection(self, point: Point):
        for stretch in self.vector_stretches.values():
            right_lane = stretch.vector_lanes[len(stretch.vector_lanes)]
            left_lane = stretch.vector_lanes[1]
            corners = []
            corners.append(right_lane.get_start_point()[0])
            corners.append(right_lane.get_end_point()[0])
            corners.append(left_lane.get_end_point()[1])
            corners.append(left_lane.get_start_point()[1])

            if point_in_box(point, corners):
                return False

        return True

    def get_reference(self, start_section_id, start_lane_id, end_section_id, end_lane_id):
        start_section = self.vector_stretches[start_section_id]
        end_section = self.vector_stretches[end_section_id]
        start_lane = start_section.vector_lanes[start_lane_id]
        end_lane = end_section.vector_lanes[end_lane_id]

        lane_adj = list(set(start_lane.successors) & set(end_lane.predecessors))[0]
        intersection_id = lane_adj.section_id
        intersection = self.vector_intersections[intersection_id]
        inter_lane_id = lane_adj.lane_id
        inter_lane = intersection.vector_lanes[inter_lane_id]

        right_boundary = start_lane.right_lane_boundary + inter_lane.right_lane_boundary + end_lane.right_lane_boundary
        left_boundary = start_lane.left_lane_boundary + inter_lane.left_lane_boundary + end_lane.left_lane_boundary
        reference = [Point(x=(p1.x + p2.x)/2, y=(p1.y + p2.y)/2)
                     for p1, p2 in zip(right_boundary.waypoints, left_boundary.waypoints)]
        return Polyline(waypoints=reference)

    def get_section_reference(self, start_section_id, end_section_id):
        start_section = self.vector_stretches[start_section_id]
        end_section = self.vector_stretches[end_section_id]
        inter_section_id = list(set(start_section.successors) & set(end_section.predecessors))[0]
        inter_section = self.vector_intersections[inter_section_id]

        left_boundary = (start_section.vector_lanes[1].left_lane_boundary +
                          inter_section.vector_lanes[1].left_lane_boundary +
                          end_section.vector_lanes[1].left_lane_boundary)

        return left_boundary



@dataclass
class SinDDynamicMap:
    city_name: str
    traffic_lights: Dict[int, TrafficLight]
    map_id: Optional[str]


    def get_traffic_light_control(self, section_id: int, timestep: int):
        for traffic_light in self.traffic_lights.values():
            control_state = traffic_light.get_control_state(section_id, timestep)
            if control_state is not None:
                return control_state

        return None



