import unittest

class TestHashing(unittest.TestCase):

    def test_binary_stack(self):
        from preface.binary_stack import BinaryStack
        
        bs = BinaryStack() 
        self.assertTrue(bs.is_empty())
        
        bs.push(True)
        self.assertFalse(bs.is_empty())
        self.assertEqual(True, bs.pop())
        self.assertTrue(bs.is_empty())

        bs.push(False)
        bs.push(True)
        bs.push(False)
        bs.push(True)
        self.assertFalse(bs.is_empty())
        self.assertEqual(True, bs.pop())
        self.assertEqual(False, bs.pop())
        self.assertEqual(True, bs.pop())
        self.assertEqual(False, bs.pop())
        self.assertTrue(bs.is_empty())
                
    def test_binary_stack_stress(self):
        from preface.binary_stack import BinaryStack
        
        bs = BinaryStack()
        for _ in range(1000):
            bs.push(True)
            self.assertFalse(bs.is_empty())
        print(bs.value)
        for _ in range(1000):
            self.assertEqual(True, bs.pop())
        self.assertTrue(bs.is_empty())           
       
if __name__ == '__main__':
    unittest.main()