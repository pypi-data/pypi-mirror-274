# <Copyright 2022, Argo AI, LLC. Released under the MIT license.>

"""Primitive types for vector maps (point, polyline)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List
import numpy as np

from sindapi.utils.typing import NDArrayFloat


@dataclass
class Point:
    """Represents a single 2-d point."""

    x: float
    y: float

    @property
    def xy(self) -> NDArrayFloat:
        """Return (3,) vector."""
        return np.array([self.x, self.y])

    def __eq__(self, other: object) -> bool:
        """Check for equality with another Point object."""
        if not isinstance(other, Point):
            return False

        return all([self.x == other.x, self.y == other.y])

    def distance_to(self, other: 'Point') -> float:
        """Calculate the Euclidean distance to another Point."""
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass
class Polyline:
    """Represents an ordered point set with consecutive adjacency."""

    waypoints: List[Point]

    @property
    def xy(self) -> NDArrayFloat:
        """Return (N,2) array representing ordered waypoint coordinates."""
        return np.vstack([wpt.xy for wpt in self.waypoints])

    def __eq__(self, other: object) -> bool:
        """Check for equality with another Polyline object."""
        if not isinstance(other, Polyline):
            return False

        if len(self.waypoints) != len(other.waypoints):
            return False

        return all([wpt == wpt_ for wpt, wpt_ in zip(self.waypoints, other.waypoints)])

    def __len__(self) -> int:
        """Return the number of waypoints in the polyline."""
        return len(self.waypoints)

    def __add__(self, other: 'Polyline') -> 'Polyline':
        """Concatenate two Polylines."""
        combined_waypoints = self.waypoints + other.waypoints
        return Polyline(combined_waypoints)


@dataclass
class LaneAdj:
    section_id: int
    lane_id: int

    def __eq__(self, other):
        if isinstance(other, LaneAdj):
            return (self.section_id == other.section_id) and (self.lane_id == other.lane_id)
        return False

    def __hash__(self):
        return hash((self.section_id, self.lane_id))


@dataclass
class LaneSegmentAdj:
    section_id: int
    lane_id: int
    segment_id: int


