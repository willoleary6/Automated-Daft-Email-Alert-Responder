from unittest import TestCase
from BasicObject import BasicObject


class TestBasicObject(TestCase):
    def setUp(self):
        self.object = BasicObject(2, 2)


class testInit(TestBasicObject):
    def test_get_result(self):
        self.assertEqual(
            self.object.get_result(),
            0
        )


class testOperators(TestBasicObject):
    def test_multiply_operands(self):
        self.object.multiply_operands()
        self.assertEqual(
            self.object.get_result(),
            4
        )

    def test_divide_operands(self):
        self.object.divide_operands()
        self.assertEqual(
            self.object.get_result(),
            1
        )

    def test_add_operands(self):
        self.object.add_operands()
        self.assertEqual(
            self.object.get_result(),
            4
        )
