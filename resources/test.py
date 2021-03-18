"""
Test Resources.
"""
import unittest

class TestHashing(unittest.TestCase):

    def test_dictionary_present(self):
        from resources.english import english_words

        # Dictionary used
        self.assertEqual(321129,len(english_words()))

    def test_highway_present(self):
        from resources.highway import highway_map

        # Dictionary used
        self.assertEqual(2305 + 2826 + 2,len(highway_map()))

if __name__ == '__main__':
    unittest.main()
