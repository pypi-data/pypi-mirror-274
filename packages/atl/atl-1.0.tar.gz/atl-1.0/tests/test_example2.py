import unittest
from atl.example2 import (
    example2_greet,
    example2_subtract,
    example2_depending_on_example1_add
)

class TestModule2ExampleFunctions(unittest.TestCase):

    def test_example2_greet(self):
        self.assertEqual(example2_greet(), "Hello from Module 2!")

    def test_example2_subtract(self):
        self.assertEqual(example2_subtract(5, 3), 2)
        self.assertEqual(example2_subtract(3, 5), -2)
        self.assertEqual(example2_subtract(0, 0), 0)

    def test_example2_depending_on_example1_add(self):
        self.assertEqual(example2_depending_on_example1_add(2, 3), 5)
        self.assertEqual(example2_depending_on_example1_add(-1, 1), 0)
        self.assertEqual(example2_depending_on_example1_add(-1, -1), -2)

if __name__ == '__main__':
    unittest.main()