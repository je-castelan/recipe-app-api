from django.test import TestCase
from app.calc import add, div


class CalcTests(TestCase):

    def test_add_numbers(self):
        self.assertEqual(add(3, 8), 11)
        self.assertEqual(div(12, 4), 3)
        self.assertEqual(div(12, 0), 0)
