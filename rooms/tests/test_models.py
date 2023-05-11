from django.test import TestCase
from ..models import Room


class ModelsTestCase(TestCase):

    def setUp(self):
        self.room = Room.objects.create(name='foo', description='some text', slug='bar')

    def test_room_model(self):
        d = self.room
        self.assertTrue(isinstance(d, Room))
        self.assertEqual(str(d), 'foo')
