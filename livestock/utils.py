"""Livestock utils package."""
from collections import OrderedDict
from datetime import datetime
from typing import Tuple, Union, List, Dict, Iterable

from random import shuffle

Number = Union[int, float]


def linear_interpolation(points: List[Tuple[Number, Number]], x: Number) -> Number:
    """
    In mathematics, linear interpolation is a method of curve fitting using
    linear polynomials to construct new data points within the range of a
    discrete set of known data points.

    Wikipedia: https://en.wikipedia.org/wiki/Linear_interpolation
    """
    flat_points: OrderedDict[Number, Number] = OrderedDict(sorted({i[0]: i[1] for i in points}.items()))

    idx_left, idx_right = nearest(list(flat_points.keys()), x)
    x0, y0 = idx_left, flat_points[idx_left]
    x1, y1 = idx_right, flat_points[idx_right]

    return (y0 * (1 - ((x - x0) / (x1 - x0)))) + (y1 * ((x - x0) / (x1 - x0)))


# Keeping helper method out of the original method in order to leave the
# actual functions be clean and easier to maintain.
def linear_interpolation_datetime(points: List[Tuple[datetime, Number]], x: datetime) -> Number:
    """Helper linear interpolation method to handle date points in datetime."""
    return linear_interpolation(
        points=[(int(i[0].timestamp()), i[1]) for i in points],
        x=x.timestamp()
    )


def nearest(array: List[Number], pivot: Number) -> Iterable[Number]:
    """Return the closes point in the array off given pivot."""
    if len(array) == 2:
        return array[0], array[1]

    left: Number = None
    right: Number = None

    for i in array:
        if pivot > i:
            right = i
        if pivot < i:
            left = i

    if left is None:
        right_idx: int = array.index(right)
        _, left = nearest(array, array[right_idx])

    if right is None:
        left_idx: int = array.index(left)
        right, _ = nearest(array, array[left_idx])

    return left, right
