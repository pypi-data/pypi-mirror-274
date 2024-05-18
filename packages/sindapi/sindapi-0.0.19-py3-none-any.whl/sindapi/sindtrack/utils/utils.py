import math
from typing import List

def generate_heading_from_position(x_values: List[float], y_values: List[float]):
    heading = []
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        if i == len(x_values) - 1:
            break

        rad = math.atan2(y_values[i + 1] - y, x_values[i + 1] - x)
        if rad < 0:
            rad += 2 * math.pi
        heading.append(rad)
    heading.append(heading[-1])
    return heading