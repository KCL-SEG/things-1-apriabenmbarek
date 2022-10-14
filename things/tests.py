from django.test import TestCase
from .models import Thing
from django.core.exceptions import ValidationError

class ThingModelTestCase(TestCase):
    def setUp(self):
        self.thing = Thing(
            name='Apple',
            description='Round green fruit',
            quantity=3
        )

    def create_second_thing(self):
        self.new_thing = Thing(
            name='Banana',
            description='Long yellow fruit',
            quantity=4
        )
        return self.new_thing

    def test_name_must_be_unique(self):
        second_thing = self.create_second_thing()
        self.thing.name = second_thing.name
        self._assert_thing_is_invalid()

    def test_name_must_not_be_blank(self):
        self.thing.name = ''
        self._assert_thing_is_invalid()

    def test_name_may_have_30_characters(self):
        self.thing.name = 'x' * 30
        self._assert_thing_is_valid()

    def test_name_must_not_have_more_than_30_characters(self):
        self.thing.name = 'x' * 31
        self._assert_thing_is_invalid()

    def test_description_need_not_be_unique(self):
        second_thing = self.create_second_thing()
        self.thing.description = second_thing.description
        self._assert_thing_is_valid()

    def test_description_may_be_blank(self):
        self.thing.description = ''
        self._assert_thing_is_valid()

    def test_description_may_have_120_characters(self):
        self.thing.description = 'x' * 120
        self._assert_thing_is_valid()

    def test_description_must_not_have_more_than_120_characters(self):
        self.thing.name = 'x' * 121
        self._assert_thing_is_invalid()

    def test_quantity_need_not_be_unique(self):
        second_thing = self.create_second_thing()
        self.thing.quantity = second_thing.quantity
        self._assert_thing_is_valid()

    def test_quantity_may_be_0(self):
        self.thing.quantity = 0
        self._assert_thing_is_valid()

    def test_quantity_must_not_be_less_than_0(self):
        self.thing.quantity = -1
        self._assert_thing_is_invalid()

    def test_quantity_may_be_100(self):
        self.thing.quantity = 100
        self._assert_thing_is_valid()

    def test_quantity_must_not_be_more_than_100(self):
        self.thing.quantity = 101
        self._assert_thing_is_invalid()

    def _assert_thing_is_valid(self):
        try:
            self.thing.full_clean()
        except (ValidationError):
            self.fail("Test thing should be valid.")

    def _assert_thing_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.thing.full_clean()
