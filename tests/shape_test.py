import unittest

from src.shape import *
from src.pattern import *
from src.cum_pattern import *


class ShapeTest(unittest.TestCase):
    def test_to_pattern(self):
        self.assertEqual(Shape((0, 4, 7)).pattern, MARY)
        self.assertEqual(Shape((0, 16, 7)).pattern, MARY)
        self.assertEqual(Shape((0, 3, 8)).pattern, MARY)
        self.assertEqual(Shape((0, 15, 7)).pattern, MINNY)
        self.assertEqual(Shape((0, -3, 4)).pattern, MINNY)

    def test_to_cum_pattern(self):
        self.assertEqual(Shape((0, 4, 7)).cum_pattern, MAJOR)
        self.assertEqual(Shape((0, 16, 7)).cum_pattern, MAJOR)
        self.assertNotEqual(Shape((0, 3, 8)).cum_pattern, MAJOR)
        self.assertEqual(Shape((0, 15, 7)).cum_pattern, MINOR)
        self.assertNotEqual(Shape((0, -3, 4)).cum_pattern, MINOR)

    def test_addition(self):
        self.assertEqual(Shape((0, 4, 7)) + 11, Shape((0, 4, 7, 11)))
        self.assertEqual(Shape((0, 4, 7)) + Shape((11,)), Shape((0, 4, 7, 11)))
