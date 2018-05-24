from datetime import datetime
from typing import Tuple, List

from django.test import SimpleTestCase

from livestock.utils import linear_interpolation, linear_interpolation_datetime


class TestLivestockUtils(SimpleTestCase):
    """
    Unit testing Livestock app utils package.

    Using :class:`SimpleTestCase` since our tests don't have any database
    access and in results our tests would be running much faster.

    Note: If you're going to tests anything that requires database access,
    be sure subclass the test suite from :class:`TestCase`.
    """
    def test_linear_interpolation(self) -> None:
        """
        if an animal weighs 101 pounds on May 1, and 105 pounds on May 5, if
        we use linear interpolation we can estimate that it is
        gaining 1 pound per day between those two dates.
        So on May 3, its estimated weight would be 103 pounds.
        """
        weight_records: List[Tuple[int, int]] = [(1, 101), (5, 105), ]
        may_3: int = 3
        expected: int = float(103)

        self.assertEqual(linear_interpolation(weight_records, x=may_3), expected)

    def test_linear_interpolation_datetime_points(self) -> None:
        """Testing if the points are in datetime."""
        weight_records: List[Tuple[datetime, int]] = ((datetime(2018, 5, 1), 101), (datetime(2018, 5, 5), 105), )
        may_3: datetime = datetime(2018, 5, 3)
        expected: int = float(103)

        self.assertEqual(linear_interpolation_datetime(weight_records, x=may_3), expected)

    def test_linear_interpolation_more_than_2_points(self) -> None:
        """Testing interpolation when having more than 2 points."""
        points: List[Tuple[int, int]] = [(1, 101), (2, 102), (4, 104), (5, 105), ]

        self.assertEqual(linear_interpolation(points, x=3), 103.0)

        points: List[Tuple[int, int]] = [(1, 108), (2, 107), (4, 114), (5, 90), (6, 95), (7, 115), ]

        self.assertEqual(linear_interpolation(points, x=3), 93.9)
        self.assertEqual(linear_interpolation(points, x=8), 97.4)
        self.assertEqual(linear_interpolation(points, x=15), 102.3)
        self.assertEqual(linear_interpolation(points, x=28), 111.4)
