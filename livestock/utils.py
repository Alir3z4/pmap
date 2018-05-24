"""Livestock utils package."""
from typing import Tuple, Union, List

Number = Union[int, float]


def linear_interpolation(points: List[Tuple[Number, Number]], x) -> Number:
    """
    In mathematics, linear interpolation is a method of curve fitting using
    linear polynomials to construct new data points within the range of a
    discrete set of known data points.

    Wikipedia: https://en.wikipedia.org/wiki/Linear_interpolation
    """
    interps: List[Number] = []
    for p0, p1 in zip(points[:-1], points[1:]):
        x0, y0 = p0[0], p0[1]
        x1, y1 = p1[0], p1[1]

        interp = (y0 * (1 - ((x - x0) / (x1 - x0)))) + (y1 * ((x - x0) / (x1 - x0)))
        interps.append(interp)

    return sum(interps) / len(interps)
