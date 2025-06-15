import unittest

from src.util import *


class UtilTests(unittest.TestCase):
    def test_rotate_12bit_bitmask_right(self):
        self.assertEqual(
            rotate_12bit_bitmask_left(int16(2048 + 512), 1), int16(1024 + 1)
        )

    def test_tetris_12bit_bitmask(self):
        self.assertEqual(tetris_12bit_bitmask(int16(32 + 16)), int16(2 + 1))
        self.assertEqual(tetris_12bit_bitmask(int16(32 + 1)), int16(32 + 1))

    def test_tetris_64bit_bitmask(self):
        self.assertEqual(tetris_64bit_bitmask(int64(32 + 16)), int64(2 + 1))
        self.assertEqual(tetris_64bit_bitmask(int64(32 + 1)), int64(32 + 1))

    def test_get_all_12bit_bitmask_rotations(self):
        self.assertCountEqual(
            get_all_12bit_bitmask_rotations(int16(16 + 4)),
            [
                int16(4 + 1),
                int16(4 + 1) << int16(1),
                int16(4 + 1) << int16(2),
                int16(4 + 1) << int16(3),
                int16(4 + 1) << int16(4),
                int16(4 + 1) << int16(5),
                int16(4 + 1) << int16(6),
                int16(4 + 1) << int16(7),
                int16(4 + 1) << int16(8),
                int16(4 + 1) << int16(9),
                (int16(1) << int16(10)) + int16(1),
                (int16(1) << int16(11)) + int16(2),
            ],
        )

    def test_get_normal_form_12bit_bitmask(self):
        self.assertEqual(get_normal_form_12bit_bitmask(int16(64 + 16)), int16(4 + 1))
        self.assertEqual(get_normal_form_12bit_bitmask(int16(4 + 1)), int16(4 + 1))
        self.assertEqual(get_normal_form_12bit_bitmask(int16(1024 + 1)), int16(4 + 1))

    def test_inner_intervals_to_cum_pattern_bitmask(self):
        self.assertEqual(inner_intervals_to_cum_pattern_bitmask([2, 10]), int16(4 + 1))
        self.assertEqual(
            inner_intervals_to_cum_pattern_bitmask([10, 2]), int16(1024 + 1)
        )

    def test_intervals_from_root_to_cum_pattern_bitmask(self):
        self.assertEqual(
            intervals_from_root_to_cum_pattern_bitmask([1, 3]), int16(8 + 2)
        )
        self.assertEqual(
            intervals_from_root_to_cum_pattern_bitmask([0, 10]), int16(1024 + 1)
        )

    def test_shape_bitmask_to_cum_pattern_bitmask(self):
        self.assertEqual(
            shape_bitmask_and_offset_to_cum_pattern_bitmask(
                int64(1 << 0) | int64(1 << 7) | int64(1 << 16), 0
            ),
            int64(1 << 0) | int64(1 << 4) | int64(1 << 7),
        )
        self.assertEqual(
            shape_bitmask_and_offset_to_cum_pattern_bitmask(
                int64(1 << 0) | int64(1 << 7) | int64(1 << 16), 2
            ),
            int64(1 << 2) | int64(1 << 6) | int64(1 << 9),
        )

    def test_get_set_bit_indices(self):
        self.assertEqual(
            get_set_bit_indices(int64(1 << 0) | int64(1 << 7) | int64(1 << 16)),
            [0, 7, 16],
        )

    def test_is_12bit(self):
        self.assertFalse(is_12bit(int16(8000)))
        self.assertTrue(is_12bit(int16(5)))
