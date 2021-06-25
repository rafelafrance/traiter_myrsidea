"""Test count trait matcher."""

import unittest

from tests.setup import test_traits


class TestCount(unittest.TestCase):
    """Test body part trait matcher."""

    def test_count_01(self):
        self.assertEqual(
            test_traits("""
                Gula with 4 setae on each side, most posterior longest. """),
            [{'part': 'gula seta side',
              'count_side_1': 4,
              'count_side_2': 4,
              'trait': 'seta_count',
              'start': 0,
              'end': 30}]
        )

    def test_count_02(self):
        self.assertEqual(
            test_traits(""" Gular plate lacking setae. """),
            [{'missing': True,
              'part': 'gular plate seta',
              'count': 0,
              'trait': 'seta_count',
              'start': 0,
              'end': 25}]
        )

    def test_count_03(self):
        self.assertEqual(
            test_traits(""" Gular plate with 3+2 setae, posterior pair longer. """),
            [{'part': 'gular plate seta',
              'count_side_1': 3,
              'count_side_2': 2,
              'trait': 'seta_count',
              'start': 0,
              'end': 26}]
        )

    def test_count_04(self):
        self.assertEqual(
            test_traits(""" Latero-ventral fringe with 8 setae. """),
            [{'part': 'lateroventral fringe seta',
              'count': 8,
              'trait': 'seta_count',
              'start': 0,
              'end': 34}]
        )
