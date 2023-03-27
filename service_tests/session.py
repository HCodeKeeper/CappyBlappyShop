from django.test import TestCase
from django.test.client import RequestFactory
from .helpers import insert_session
from custom_exceptions.session import InvalidTokenFormatException, EmptyTemporalRegistrationStorage
from helpers.account import TokenGenerator
from services.session import (
    TemporalPasswordUpdateTokenStorage,
    TemporalRegistrationStorage,
)


class RegistrationStorage(TestCase):
    def setUp(self) -> None:
        self.mock_request = RequestFactory().get('/mock_path/')
        insert_session(self.mock_request, lambda mock_request: None)

        self.storage = TemporalRegistrationStorage(self.mock_request)

    def _insert_data(self, username, password, email, token):
        self.storage.put(email, username, password, token)

    def test_no_keys_before_inserted_credits(self):
        self.assertEqual(self.storage.exists(), False)

    def test_raises_exception_when_getting_data_before_inserting(self):
        self.assertRaises(EmptyTemporalRegistrationStorage, self.storage.get)

    def test_update_token_without_credits(self):
        self.assertRaises(EmptyTemporalRegistrationStorage, self.storage.update_token)

    def test_update_token(self):
        token = TokenGenerator.get_token()
        self._insert_data('username', 'password', 'email@gmail.com', token)
        self.storage.update_token()
        new_token = self.storage.get().get_token()
        self.assertNotEqual(token, new_token)

    def test_update_invalid_token_format(self):
        self.assertRaises(
            InvalidTokenFormatException,
            self._insert_data, 'username', 'password', 'email@gmail.com', 'T0K$en'
        )

    def test_update_token(self):
        token = TokenGenerator.get_token()
        username, password, email = ('username', 'password', 'email@gmail.com')
        self._insert_data(username, password, email, token)
        stored_data = self.storage.get()
        self.assertEqual(
            (stored_data.username, stored_data.password, stored_data.email, stored_data.token),
            (username, password, email, token)
        )

    def test_clean(self):
        username, password, email = ('username', 'password', 'email@gmail.com')
        token = TokenGenerator.get_token()
        self._insert_data(username, password, email, token)
        self.storage.clean()
        self.assertRaises(EmptyTemporalRegistrationStorage, self.storage.get)


class TokenStorageShouldStore(TestCase):
    def setUp(self) -> None:
        self.mock_request = RequestFactory().get('/mock_path/')
        insert_session(self.mock_request, lambda mock_request: None)

        self.storage = TemporalPasswordUpdateTokenStorage(self.mock_request)
        self.token = TokenGenerator.get_token()

    def _put(self):
        self.storage.put(self.token)

    def test_get(self):
        self._put()
        self.assertEqual(self.storage.get(), self.token)
