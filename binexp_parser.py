#!/usr/bin/python3
import os
from os.path import join as osjoin

import unittest

from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'operator'])

class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """
    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """
        self.val = prefix_list.pop(0)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = False
            self.right = False
        else:
            self.type = NodeType.operator
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def infix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'
    def postfix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    def additive_identity(self):
        """
        Reduce additive identities
        x + 0 = x
        """
        # IMPLEMENT ME!
        if self is None:
            return None
        if self.val== '+':

            left = self.left.additive_identity()
            right = self.right.additive_identity()

            if left.val== '0':
                return right
            if right.val == '0':
                return left
            return self('+',left,right)
        else:
            return self
        pass
                        
    def multiplicative_identity(self):
        """
        Reduce multiplicative identities
        x * 1 = x
        """
        # IMPLEMENT ME!
        if self is None:
            return None
        if self.val == '*':
            left = self.left.multiplicative_identity()
            right = self.right.multiplicative_identity()

            if left.val == '1':
                return right
            if right.val == '1':
                return left
            else:
                return self 
        pass
    
    
    def mult_by_zero(self):
        """
        Reduce multiplication by zero
        x * 0 = 0
        """
        # Optionally, IMPLEMENT ME! (I'm pretty easy)
        if self is None:
            return None 
        if self.value == '0':
            left = self.left.mult_by_zero()
            right = self.right.mult_by_zero()
            if left.val == "0":
                return left
            if right.val == "0":
                return right

        pass      

    def simplify_binops(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        self.additive_identity()
        self.multiplicative_identity()
        self.mult_by_zero()
        return self

class MyTests(unittest.TestCase):
    testbench_dir = 'testbench'

    def run_test_from_file(self, test_type, test_name):
        """
        Run a test case using input and output files.
        """
        input_file = os.path.join(self.testbench_dir, test_type, 'inputs', test_name)
        output_file = os.path.join(self.testbench_dir, test_type, 'outputs', test_name)

        # Read input and output files
        with open(input_file, 'r') as infile, open(output_file, 'r') as outfile:
            inputs = infile.read().splitlines()
            expected_outputs = outfile.read().splitlines()

            # Run tests for each line
            for input_expr, expected_output in zip(inputs, expected_outputs):
                tokens = input_expr.split()
                tree = BinOpAst(tokens)
                simplified_tree = tree.simplify_binops()
                result = simplified_tree.prefix_str()
                self.assertEqual(result, expected_output, f"Failed for input {input_expr}: expected {expected_output}, got {result}")

    def test_arith_id(self):
        self.run_test_from_file('arith_id', 'simple')

    def test_mult_id(self):
        self.run_test_from_file('mult_id', 'simple')

    def test_mult_by_zero(self):
        self.run_test_from_file('mult_by_zero', 'simple')

    def test_constant_fold(self):
        self.run_test_from_file('constant_fold', 'simple')

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
