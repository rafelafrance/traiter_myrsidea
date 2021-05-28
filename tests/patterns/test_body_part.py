"""Test body part trait matcher."""

import unittest

from tests.setup import test_traits


class TestBodyPart(unittest.TestCase):
    """Test body part trait matcher."""

    def test_body_part_01(self):
        self.assertEqual(
            test_traits('Body entirely whitish, thorax and abdomen'),
            [{'body_part': 'body', 'trait': 'body_part', 'start': 0, 'end': 4},
             {'body_part': 'thorax', 'trait': 'body_part', 'start': 23, 'end': 29},
             {'body_part': 'abdomen', 'trait': 'body_part', 'start': 34, 'end': 41}]
        )
