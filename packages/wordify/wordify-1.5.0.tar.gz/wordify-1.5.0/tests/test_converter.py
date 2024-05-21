import unittest
from wordify.converter import IntegerConverter, DecimalConverter


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.integer_converter = IntegerConverter()
        self.decimal_converter = DecimalConverter()

    def test_integer_converter(self):
        self.integer_converter.set_number(121)
        self.assertEqual(self.integer_converter.convert(), "one hundred twenty one")

    def test_decimal_converter(self):
        self.decimal_converter.set_number(121.021)
        self.assertEqual(self.decimal_converter.convert(), "one hundred twenty one point zero two one")


if __name__ == '__main__':
    unittest.main()
