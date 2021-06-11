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
             {'measure': 'head length',
              'low': 0.29,
              'high': 0.31,
              'trait': 'measurement',
              'start': 22,
              'end': 34},
             {'measure': 'preantennal width',
              'low': 0.32,
              'high': 0.34,
              'trait': 'measurement',
              'start': 36,
              'end': 50},
             {'measure': 'ow',
              'low': 0.41,
              'high': 0.44,
              'trait': 'measurement',
              'start': 52,
              'end': 64},
             {'measure': 'prothorax width',
              'low': 0.25,
              'high': 0.27,
              'trait': 'measurement',
              'start': 66,
              'end': 78},
             {'measure': 'pspl',
              'low': 0.1,
              'trait': 'measurement',
              'start': 80,
              'end': 89},
             {'measure': 'metathorax width',
              'low': 0.35,
              'high': 0.4,
              'trait': 'measurement',
              'start': 91,
              'end': 104},
             {'measure': 'mspl',
              'low': 0.14,
              'high': 0.16,
              'trait': 'measurement',
              'start': 106,
              'end': 120},
             {'measure': 'abdomen width at tergite 4',
              'low': 0.46,
              'high': 0.55,
              'trait': 'measurement',
              'start': 122,
              'end': 136},
             {'measure': 'anus width',
              'low': 0.17,
              'high': 0.18,
              'trait': 'measurement',
              'start': 138,
              'end': 151},
             {'measure': 'total length',
              'low': 1.31,
              'high': 1.39,
              'units': 'mm',
              'trait': 'measurement',
              'start': 153,
              'end': 169}]
        )
