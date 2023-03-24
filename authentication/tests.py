from django.test import TestCase
from django.contrib.auth.models import User
from user_profiles.models import Profile
from django.test.client import Client, RequestFactory
from django.shortcuts import reverse


"""
Registration views aren't tested, because every complicated view uses token sending through emailing
"""


class AddUserMixin:
    def setUp(self) -> None:
        self.user = User.objects.create_user('test_username', 'test@gmail.com')
        self.user_unhashed_password = '1234'
        self.user.set_password(self.user_unhashed_password)
        self.user.save()
        self.profile = Profile.objects.create(user=self.user, email='for_notifications@gmail.com')


class AuthenticationShouldLogin(AddUserMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()

    def test_login_page(self):
        response = self.client.get(reverse('login_page'), follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_page_when_already_authenticated(self):
        self.client.login(username=self.user.username, password=self.user_unhashed_password)
        response = self.client.get(reverse('login_page'), follow=True)
        self.assertTemplateUsed(response, 'index.html')

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': self.user.username,
            'password': self.user_unhashed_password
        }, follow=True)
        self.assertTemplateUsed(response, 'account.html')

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'invalid',
            'password': 'invalid'
        }, follow=True)
        self.assertTemplateUsed(response, 'login_data_invalid.html')

    def test_logout(self):
        self.client.login(username=self.user.username, password=self.user_unhashed_password)
        response = self.client.post(reverse('logout'), follow=True)
        self.assertTemplateUsed(response, 'index.html')
