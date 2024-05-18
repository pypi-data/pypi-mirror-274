from dataclasses import dataclass
from typing import List, Optional, Dict

from ..lane.lane_segment import Lane, LaneSegment
from ..utils.map_primitives import Polyline

@dataclass
class Stretch:
    id: int     # 2 digits
    predecessors: List[int]
    successors: List[int]
    vector_lanes: Dict[int, Lane]
    opposite_stretch_id: Optional[int] = None


    @classmethod
    def build(cls, stretch_data: dict) -> 'Stretch':
        Lane.set_shared_param(stretch_data['split_distance'], stretch_data['segment_point_num'])

        vector_lanes = cls.get_vector_lanes(stretch_data)
        stretch_data.update({'vector_lanes': vector_lanes})
        return cls(id=stretch_data['id'],
                   predecessors=stretch_data['predecessors'],
                   successors=stretch_data['successors'],
                   vector_lanes=stretch_data['vector_lanes'],
                   opposite_stretch_id=stretch_data['opposite_stretch_id']
        )

    @classmethod
    def get_vector_lanes(cls, stretch_data: dict) -> Dict[int, Lane]:
        vector_lanes = {}
        for lane_data in stretch_data.get('lanes'):
            lane = Lane.build(lane_data)

            attr_data = {
                'section_id': stretch_data['id'],
                'is_intersection': False
            }
            lane.add_attributes(attr_data)

            vector_lanes[lane.id] = lane

        return vector_lanes

    def get_vertex(self):
        right_start_vertex = self.vector_lanes[len(self.vector_lanes)].right_lane_boundary.waypoints[0]
        right_end_vertex = self.vector_lanes[len(self.vector_lanes)].right_lane_boundary.waypoints[-1]
        left_end_vertex = self.vector_lanes[1].left_lane_boundary.waypoints[-1]
        left_start_vertex = self.vector_lanes[1].left_lane_boundary.waypoints[0]
        return right_start_vertex, right_end_vertex, left_end_vertex, left_start_vertex

