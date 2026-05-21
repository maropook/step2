import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import unittest
from task1_2_1 import create_query_substrings


class TestTask121(unittest.TestCase):

    def test_create_query_substrings(self):
        self.assertEqual(
            create_query_substrings("aaa"),
            ["a", "aa", "aaa"],
        )
        self.assertEqual(
            create_query_substrings("ab"),
            ["b", "a", "ab"],
        )
        self.assertEqual(
            create_query_substrings(""),
            [],
        )


if __name__ == "__main__":
    unittest.main()
