from django.test import TestCase
from django.test.client import Client
from authentication.tests import AddUserMixin
from django.shortcuts import reverse


class AccountShouldBeChanged(AddUserMixin, TestCase):
    def setUp(self) -> None:
        super(AccountShouldBeChanged, self).setUp()
        self.client = Client()

    def test_account_page(self):
        self.client.login(username=self.user.username, password=self.user_unhashed_password)
        response = self.client.get(reverse('account'))
        self.assertTemplateUsed(response, 'account.html')

    def test_account_page_when_unauthenticated(self):
        response = self.client.get(reverse('account'), follow=True)
        self.assertTemplateUsed(response, 'login.html')

    def test_edit_profile_page(self):
        self.client.login(username=self.user.username, password=self.user_unhashed_password)
        response = self.client.get(reverse('get_edit_profile_page'))
        self.assertTemplateUsed(response, 'change_profile_credits.html')

    def test_edit_profile(self):
        self.client.login(username=self.user.username, password=self.user_unhashed_password)
        first_name, second_name, telephone = "First", "Second", "380101236868"
        response = self.client.post(reverse('edit_profile'), {
            "first_name": first_name,
            "second_name": second_name,
            "telephone": telephone
        }, follow=True)

        # Profile in test and in update method are different references
        self.profile.refresh_from_db()

        self.assertTemplateUsed(response, 'account.html')
        self.assertEqual(first_name, self.profile.first_name)
        self.assertEqual(second_name, self.profile.second_name)
        self.assertEqual(telephone, self.profile.telephone.number)
