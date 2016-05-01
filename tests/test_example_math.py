import unittest


class TestHelloExample(unittest.TestCase):
    def setUp(self):
        import youjo.math
        self.target = youjo.math

    def test_string(self):
        self.assertEqual(self.target.enum_prime(10), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_val(self):
        self.assertEqual(self.target.sleep_sort([6, 1, 7, 4, 3, 2, 4]), [1, 2, 3, 4, 4, 6, 7])