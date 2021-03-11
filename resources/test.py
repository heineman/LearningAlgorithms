"""Test Resources."""
import unittest

class TestHashing(unittest.TestCase):

    def test_binary_stack(self):
        from resources.english import english_words
        
        # Dictionary used
        self.assertEquals(321165,len(english_words()))
       
if __name__ == '__main__':
    unittest.main()