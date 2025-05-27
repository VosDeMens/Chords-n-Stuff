import unittest

from src.util import *


class UtilTests(unittest.TestCase):
    def test_create_all_rotations(self):
        self.assertSetEqual(
            get_all_rotations((1, 2, 3)), {(1, 2, 3), (2, 3, 1), (3, 1, 2)}
        )
        self.assertSetEqual(
            get_all_rotations((1, 2, 3, 4)),
            {(1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, 3)},
        )

    def test_rotate_by(self):
        self.assertTupleEqual(rotate_by((1, 2, 3), 0), (1, 2, 3))
        self.assertTupleEqual(rotate_by((1, 2, 3), 1), (2, 3, 1))
        self.assertTupleEqual(rotate_by((1, 2, 3), 2), (3, 1, 2))
        self.assertTupleEqual(rotate_by((1, 2, 3), 3), (1, 2, 3))

    def test_get_minimal_rotation(self):
        self.assertTupleEqual(get_minimal_rotation((1, 2, 3)), (1, 2, 3))
        self.assertTupleEqual(get_minimal_rotation((4, 5, 1)), (1, 4, 5))
        self.assertTupleEqual(get_minimal_rotation((6, 5, 1)), (1, 6, 5))
        self.assertTupleEqual(get_minimal_rotation((6, 5, 7)), (5, 7, 6))
        self.assertTupleEqual(get_minimal_rotation((1, 3, 1, 2)), (1, 2, 1, 3))

    def test_get_inner_intervals(self):
        self.assertTupleEqual(get_inner_intervals((0, 4, 7)), (4, 3))
        self.assertTupleEqual(get_inner_intervals((0, 7, 4)), (7, -3))
        self.assertTupleEqual(get_inner_intervals((0, 3, 6, 9)), (3, 3, 3))
        self.assertTupleEqual(get_inner_intervals((0, 2, 4)), (2, 2))
        self.assertTupleEqual(get_inner_intervals((0, 7, 4)), (7, -3))
        self.assertTupleEqual(get_inner_intervals((-1, -3, 5)), (-2, 8))
        self.assertTupleEqual(get_inner_intervals(()), ())

    def test_get_intervals_from_root(self):
        self.assertEqual(get_intervals_from_root((3, 4, 5)), (0, 3, 7))
        self.assertEqual(get_intervals_from_root((3, 4, 5), 1), (1, 4, 8))
        self.assertEqual(get_intervals_from_root(()), ())

        with self.assertRaises(AssertionError):
            get_intervals_from_root((3, 3, 3))
