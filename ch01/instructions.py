"""Produce Python byte code for function.

https://github.com/python/cpython/blob/c96d00e88ead8f99bb6aa1357928ac4545d9287c/Python/bltinmodule.c

Shows how to disassemble Python byte code.
"""
import dis

def f():
    """Sample code to be disassembled."""
    A=[13, 2, 18, 7, 50]
    if len(A) == 0:
        return None
    return max(A)

#######################################################################
if __name__ == '__main__':
    dis.dis(f)
