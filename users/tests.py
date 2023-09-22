from django.test import TestCase
from .models import User
from django.db.utils import IntegrityError
from django.contrib.auth import login
import django
class Mytest(TestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create(username='test1', email='mahdiazimi007m@gmail.com', password='test')
        self.u2 = User.objects.create(username='test2', email='mahdiazimi007mm@gmail.com')
        pass
    def test_user_create(self):
        self.assertEquals(2,2)
        u1 = User.objects.get(username=self.u1.username)
        u2 = User.objects.get(username=self.u2.username)
        self.assertEquals(u1, self.u1)
        with self.assertRaises(IntegrityError):
            User.objects.create(username='s', email='mahdiazimi007m@gmail.com')



