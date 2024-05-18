# <Copyright 2022, Argo AI, LLC. Released under the MIT license.>

"""Classes that define the data schema for Argoverse motion forecasting scenarios."""

from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Optional, Tuple, Dict

from ..sindmap.map_api import SinDDynamicMap
from ..sindmap.traffic_light.traffic_light import SignalType
from ..utils.typing import NDArrayFloat

##########################
# Track-level Data Classes
##########################

@unique
class TrackCategory(Enum):
    """All tracks are categorized with one of four labels, depending on data quality and scenario generation criteria.

    Members:
        TRACK_FRAGMENT: Track that has only a few frames in the observation frame. - can not be used
        UNSCORED_TRACK: Track that has over half of the frames missing in the observation/prediction frame. - can be used for contextual input.
        SCORED_TRACK: Track that only has a few frames missing in the observation frame. CAN BE USED FOR PREDICTION
        FOCAL_TRACK: Whole tracks - used in the multi-agent prediction task.
    """

    TRACK_FRAGMENT: int = 0
    UNSCORED_TRACK: int = 1
    SCORED_TRACK: int = 2
    FOCAL_TRACK: int = 3

@unique
class ObjectType(str, Enum):
    """All tracks are assigned one of the following object type labels."""

    CAR: str = "car"
    TRUCK: str = "truck"
    BUS: str = "bus"
    MOTORCYCLE: str = "motorcycle"
    BICYCLE: str = "bicycle"
    TRICYCLE: str = "tricycle"
    PEDESTRIAN: str = "pedestrian"

@unique
class CrossType(str, Enum):
    """All tracks(except pedestrian) are assigned one of the following cross type labels."""

    STRAIGHTCROSS: str = "StraightCross"
    LEFTTURN: str = "LeftTurn"
    RIGHTTURN: str = "RightTurn"
    OTHERS: str = "Others"

@unique
class ViolationType(str, Enum):
    """All tracks(except pedestrian) are assigned one of the following cross type labels."""

    NO_VIOLATION: str = "No violation of traffic lights"
    RED_LIGHT_RUNNING: str = "red-light running"
    YELLOW_LIGHT_RUNNING: str = "yellow-light running"

@dataclass
class ObjectState:
    """Bundles all state information associated with an object at a fixed point in time.

    Attributes:
        observed: Boolean indicating if this object state falls in the observed segment of the scenario.
        timestep: Time step corresponding to this object state [0, num_scenario_timesteps).
        position: (x, y) Coordinates of center of object bounding box.
        heading: Heading associated with object bounding box (in radians, defined w.r.t the map coordinate frame).
        velocity: (x, y) Instantaneous velocity associated with the object (in m/s).
    """

    observed: bool
    timestep: int
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    acceleration: Tuple[float, float]
    heading: float
    traffic_light_control: SignalType


@dataclass
class ObjectAttribute:
    length: float
    width: float
    crosstype: CrossType
    violation: ViolationType



@dataclass()
class Track:
    """Bundles all data associated with an SinD track.

    Attributes:
        track_id: Unique ID associated with this track.
        object_states: States for each timestep where the track object had a valid observation.
        object_type: Inferred type for the track object.
        category: Assigned category for track - used as an indicator for prediction requirements and data quality.
    """

    track_id: str
    object_states: List[ObjectState]
    object_type: ObjectType
    category: TrackCategory
    object_attribute: Optional[ObjectAttribute] = None



#############################
# Scenario-level data classes
#############################


@dataclass()
class SinDScenario:
    """Bundles all data associated with an SinD scenario.

    Attributes:
        scenario_id: Unique ID associated with this scenario.
        timestamps_ms: All timestamps_ms associated with this scenario.
        tracks: All tracks associated with this scenario.
        focal_track_id: The track ID associated with the focal agent of the scenario.
        city_name: The name of the city associated with this scenario.
        map_id: The map ID associated with the scenario (used for internal bookkeeping).
        record_id: ID of the slice used to generate the scenario (used for internal bookkeeping).
    """

    scenario_id: int
    record_id: str
    timestamps_ms: List[float]
    tracks: Dict[str, Track]
    focal_track_id: str
    city_name: str
    dynamic_map: Optional[SinDDynamicMap] = None
    map_id: Optional[str] = None

