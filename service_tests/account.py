from django.db import DatabaseError

from custom_exceptions.account import ProfileAlreadyExistException
from services.account import (
    register,
    add_user_to_db,
    add_profile_to_user,
    add_telephone_with_profile,
    update_profile,
    update_password,
    lookup_user,
    get_profile_from_request,
    RegistrationCreditsCachingHandler,
    RegistrationTokenSendingHandler
)
from services.session import RegistrationData
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class AccountCase(TestCase):
    def test_register(self):
        email, username, password = 'email@gmail.com', 'username', 'password'
        registration_data = RegistrationData(email, username, password)
        register(registration_data)
        self.assertIsNotNone(User.objects.get(email=email))

    def test_register_with_duplicate(self):
        email, username, password = 'email@gmail.com', 'username', 'password'
        registration_data = RegistrationData(email, username, password)
        register(registration_data)
        self.assertRaises(DatabaseError, register,  registration_data=registration_data)

    def test_update_password(self):
        email, username, password = 'email@gmail.com', 'username', 'password'
        registration_data = RegistrationData(email, username, password)
        register(registration_data)
        new_password = 'bruh'
        update_password(email, new_password)
        user = User.objects.get(email=email)
        self.assertIs(check_password(new_password, user.password), True)

