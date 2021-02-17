"""
Make a stack from binary values.
Keep track of value as a (potentially infinite) value. By setting
the empty value to 1, we do not have to keep track of how many bits
are present.
"""

class BinaryStack:
    def __init__(self):
        self.value = 1     # Empty is the bit sequence "1"
    
    def pop(self):
        if self.value == 1:
            raise "Empty Stack"
    
        val = self.value % 2
        self.value = self.value >> 1
        return val == 1
    
    def push(self, b):
        self.value = self.value << 1
        if b:
            self.value += 1
        
    def is_empty(self):
        return self.value == 1
    