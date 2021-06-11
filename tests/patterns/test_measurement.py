"""Test measurement trait matcher."""

import unittest

from tests.setup import test_traits


class TestMeasurement(unittest.TestCase):
    """Test body part trait matcher."""

    def test_measurement_01(self):
        self.assertEqual(
            test_traits("""
            Measurements (n = 4). HL 0.29–0.31, PAW 0.32–
                0.34, OW 0.41–0.44, PW 0.25–0.27, PSPL 0.10, MTW
                0.35–0.40, MSPL 0.14–0.16, AWIV 0.46–0.55, ANW
                0.17–0.18, TL 1.31–1.39 mm.
            """),
            [{'n': 4, 'trait': 'sample', 'start': 14, 'end': 19},
             {'measurement': 'head length',
              'low': 0.29,
              'high': 0.31,
              'trait': 'measurement',
              'start': 22,
              'end': 34},
             {'measurement': 'preantennal width',
              'low': 0.32,
              'high': 0.34,
              'trait': 'measurement',
              'start': 36,
              'end': 50},
             {'measurement': 'ow',
              'low': 0.41,
              'high': 0.44,
              'trait': 'measurement',
              'start': 52,
              'end': 64},
             {'measurement': 'prothorax width',
              'low': 0.25,
              'high': 0.27,
              'trait': 'measurement',
              'start': 66,
              'end': 78},
             {'measurement': 'pspl',
              'low': 0.1,
              'trait': 'measurement',
              'start': 80,
              'end': 89},
             {'measurement': 'metathorax width',
              'low': 0.35,
              'high': 0.4,
              'trait': 'measurement',
              'start': 91,
              'end': 104},
             {'measurement': 'mspl',
              'low': 0.14,
              'high': 0.16,
              'trait': 'measurement',
              'start': 106,
              'end': 120},
             {'measurement': 'abdomen width at tergite 4',
              'low': 0.46,
              'high': 0.55,
              'trait': 'measurement',
              'start': 122,
              'end': 136},
             {'measurement': 'anus width',
              'low': 0.17,
              'high': 0.18,
              'trait': 'measurement',
              'start': 138,
              'end': 151},
             {'measurement': 'total length',
              'low': 1.31,
              'high': 1.39,
              'units': 'mm',
              'trait': 'measurement',
              'start': 153,
              'end': 169}]
        )

    def test_measurement_02(self):
        self.assertEqual(
            test_traits(""" ls5 0.04–0.05, """),
         [{'measurement': 'labial seta 5',
           'low': 0.04,
           'high': 0.05,
           'trait': 'measurement',
           'start': 0,
           'end': 13}]
        )

    def test_measurement_03(self):
        self.assertEqual(
            test_traits("""
             Dorsal head seta 10 (dhs10), 0.046–0.058 long; dhs11,
             0.084–0.100 long, ratio dhs10/11 0.5–0.6.
             """),
            [{'measurement': 'dorsal head seta 10',
              'low': 0.046,
              'high': 0.058,
              'trait': 'measurement',
              'start': 0,
              'end': 40},
             {'measurement': 'dorsal head seta 11',
              'low': 0.084,
              'high': 0.1,
              'trait': 'measurement',
              'start': 47,
              'end': 65},
             {'low': 0.5,
              'high': 0.6,
              'ratio': 'dhs10/11',
              'trait': 'ratio',
              'start': 78,
              'end': 94}]
        )
