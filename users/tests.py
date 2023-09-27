from django.test import TestCase, TransactionTestCase
from .models import User
from django.db.utils import IntegrityError
from django.contrib.auth import login
import django
from captcha.views import CaptchaStore

class Mytest(TransactionTestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(username='test1', email='mahdiazimi007m@gmail.com', password='Test0996')
        self.u2 = User.objects.create_user(username='test2', email='mahdiazimi007mm@gmail.com', password='Test0996')
        self.u3 = User.objects.create_user(username='test3', email='test@gmail.com', password='Test0996', phone_number='09963001880')
        self.u4 = User.objects.create_user(username='test4', email='test4@gmail.com',  password='Test0996', phone_number='09963001881')
        self.u5 = User.objects.create_user(username='test5', email='test5@gmail.com',  password='Test0996', phone_number='09963001882')
    def test_user_create(self):
        self.assertEquals(2,2)
        u1 = User.objects.get(pk=self.u1.pk)
        u2 = User.objects.get(pk=self.u2.pk)
        u3 = User.objects.get(pk=self.u3.pk)
        u4 = User.objects.get(pk=self.u4.pk)
        u5 = User.objects.get(pk=self.u5.pk)
        self.assertEquals(u1, self.u1)
        self.assertEquals(u2, self.u2)
        self.assertEquals(u1.profile, self.u1.profile)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='u2', email='mahdiazimi007m@gmail.com', password='test')
            User.objects.create_user(username='u4', email='sadasd@gmail.com', password='test')
            User.objects.create(username='u5', email='sdfsdf@gmail.com', password='test', phone_number='09963001880')
        self.assertEquals(u2.profile, self.u2.profile)
        self.assertEquals(u3, self.u3)
        self.assertEquals(u3.profile, self.u3.profile)
        self.assertEquals(u4, self.u4)
        self.assertEquals(u4.profile, self.u4.profile)
        self.assertEquals(u5.is_superuser, False)
        self.assertEquals(u5.is_staff, False)
        self.assertEquals(u5.is_active, True)

    # def test_register_view(self):
    #     captcha = CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())
    #     instance1 = self.client.post('/register/', {'username': 'test6',
    #                                                 'email': 'sadfsadasd@gmail.com',
    #                                                 'password1': 'Test0996',
    #                                                 'password2': 'Test0996',
    #                                                 })
    #     u6 = User.objects.get(username='test6')
    #     self.assertEquals(instance1.status_code, 200)
    #     self.assertEquals(u6.is_active, False)
    #     self.assertEquals(u6.is_staff, False)
    #     self.assertEquals(u6.is_superuser, False)
    #     with self.assertRaises(IntegrityError):
    #         instance2 = self.client.post('/register/', {'username': 'test6', 'email': 'sadfsadasd@gmail.com',
    #                                                     'password1': 'Test0996',
    #                                                     'password2': 'Test0996'})
    #     instance3 = self.client.post('/register/', {'username': 'test7', 'email': 'saadfsadasd@gmail.com',
    #                                                     'password1': 'test0996',
    #                                                     'password2': 'test0996'})
    #     self.assertEquals(instance3.status_code, 400)
    #     instance4 = self.client.post('/register/', {'username': 'test7', 'email': 'saadfsadasd@gmail.com',
    #                                                 'password1': 'TTTTTTTTTTT',
    #                                                 'password2': 'TTTTTTTTTTT'})
    #     self.assertEquals(instance4.status_code, 400)
    #
    #     instance5 = self.client.post('/register/', {'username': 'test7', 'email': 'saadfsadas#@d@gmail.com',
    #                                                 'password1': 'Test0996',
    #                                                 'password2': 'Test0996'})
    #     self.assertEquals(instance5.status_code, 400)

    def test_login_view(self):
        self.client.login(username=self.u1.username, password=self.u1.password)
        self.client.login(email=self.u1.email, password=self.u1.password)
        instance6 = self.client.post('/login/', {'username': self.u1.username, 'password': "Test0996"})
        instance7 = self.client.post('/login/', {'username': self.u1.email, 'password': "Test0996"})
        instance8 = self.client.post('/login/', {'username': self.u1.email, 'password': "Test09966"})
        self.assertEquals(instance6.status_code, 302)
        self.assertEquals(instance7.status_code, 302)
        self.assertEquals(instance8.status_code, 400)

    def test_logout(self):
        instance9 = self.client.get('/logout/')
        self.assertEquals(instance9.status_code, 302)
