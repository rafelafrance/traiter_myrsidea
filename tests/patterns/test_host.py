"""Test host trait matcher."""

import unittest

from tests.setup import test_traits


class TestHost(unittest.TestCase):
    """Test body part trait matcher."""

    def test_host_01(self):
        self.assertEqual(
            test_traits("""
                The purpose of this paper is to describe two species of chewing lice
                found on the Swainson's warbler—Limnothlypis swainsonii (Audubon, 1834)
                """),
            [{'host_common_name': "swainson's warbler",
              'trait': 'host_common_name',
              'start': 82,
              'end': 100},
             {'host_species': 'limnothlypis swainsonii',
              'trait': 'host_species',
              'start': 101,
              'end': 124}]
        )
