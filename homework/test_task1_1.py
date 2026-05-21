import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import unittest
from task1_1 import get_anagram_with_base_dictionary


class TestTask1(unittest.TestCase):

    def test_get_anagram_with_base_dictionary(self):
        self.assertEqual(
            get_anagram_with_base_dictionary("aaa"),
            ["aaa"],
        )
        self.assertEqual(
            get_anagram_with_base_dictionary(
                "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
            ),
            [],
        )
        self.assertEqual(
            get_anagram_with_base_dictionary(""),
            [],
        )
        self.assertEqual(
            get_anagram_with_base_dictionary("noqueryfound"),
            [],
        )
        self.assertEqual(
            get_anagram_with_base_dictionary("amphitheatres"),
            ["amphitheaters", "amphitheatres"],
        )


if __name__ == "__main__":
    unittest.main()
