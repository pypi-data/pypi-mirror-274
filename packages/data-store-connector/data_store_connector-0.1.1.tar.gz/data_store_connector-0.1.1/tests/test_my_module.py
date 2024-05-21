import unittest
from my_module import hello

class TestMyModule(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), None)
