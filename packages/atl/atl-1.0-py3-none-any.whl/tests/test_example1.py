import unittest
from atl.example1 import example1_greet, example1_add

class TestModule1ExampleFunctions(unittest.TestCase):

    def test_example1_greet(self):
        self.assertEqual(example1_greet(), "Hello from Module 1!")

    def test_example1_add(self):
        self.assertEqual(example1_add(1, 2), 3)
        self.assertEqual(example1_add(-1, 1), 0)
        self.assertEqual(example1_add(-1, -1), -2)

if __name__ == '__main__':
    unittest.main()