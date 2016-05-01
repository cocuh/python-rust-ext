import unittest


class TestHelloExample(unittest.TestCase):
    def setUp(self):
        import youjo.hello
        self.target = youjo.hello

    def test_string(self):
        self.assertEqual(self.target.run(), "hello youjo!")
    
    def test_val(self):
        self.assertEqual(self.target.val(), 42)