from django.test import TestCase
from django.contrib import auth

from .models import User

# Create your tests here.
class AuthTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create_superuser("admin222@test.com", "sss", "1234-12-12", "123456789")
        self.u.is_staff = True
        self.u.is_supseruser = True
        self.u.is_admin = True
        self.u.is_active = True
        self.u.save()
        
    def testlogin(self):
        self.client.login(username="admin222@test.com", password="123456789")
        