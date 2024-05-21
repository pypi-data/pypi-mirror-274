import unittest
from wordify.converter import IntegerConverter, DecimalConverter


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.integer_converter = IntegerConverter(121)
        self.decimal_converter = DecimalConverter(121.021)

    def test_integer_converter(self):
        self.assertEqual(self.integer_converter.convert(), "one hundred twenty one")

    def test_decimal_converter(self):
        self.assertEqual(self.decimal_converter.convert(), "one hundred twenty one point zero two one")


if __name__ == '__main__':
    unittest.main()
