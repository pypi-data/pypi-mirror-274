
from enum import Enum, unique
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from ..stretch.stretch import Stretch
from ..intersection.intersection import Intersection



@unique
class SignalType(int, Enum):
    """All traffic lights are assigned one of the signal type labels."""
    UNKNOWN: int = 0
    GREEN: int = 1
    RED: int = 2
    YELLOW: int = 3

    @classmethod
    def from_int(cls, number: int) -> 'SignalType':
        """Converts a number to SignalType."""
        if number == 0:
            return SignalType.RED
        elif number == 1:
            return SignalType.GREEN
        elif number == 2:
            return SignalType.UNKNOWN
        elif number == 3:
            return SignalType.YELLOW
        raise ValueError(f"No SignalType found for number {number}")


@dataclass
class LightState:
    """Bundles all state information associated with an object at a fixed point in time.

    Attributes:
        timestep: Time step corresponding to this object state [0, num_scenario_timesteps).
        signal_type: SignalType of the light
        remaining_seconds: Number of seconds remaining
    """

    timestep: int
    signal_type: SignalType
    remaining_seconds: int



@dataclass
class TrafficLight:
    id: int
    controlled_stretches: List[int]
    controlled_intersections: List[int]
    light_states: List[LightState]

    def get_control_state(self, section_id: int, timestep: int):
        if section_id not in self.controlled_stretches:
            return None

        if timestep > len(self.light_states) - 1:
            return None
        control_state = self.light_states[timestep].signal_type
        return control_state
