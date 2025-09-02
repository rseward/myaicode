import unittest

class TestSimple(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(1, 1)

    def test_simple2(self):
        self.assertEqual(10, 10)

    def test_error(self):
        #answer = 10/0
        self.assertEqual(1, 2)

if __name__ == "__main__":
    unittest.main()
