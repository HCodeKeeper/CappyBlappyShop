from django.contrib.auth.models import User
from django.db.utils import DatabaseError
from .session import RegistrationData


def add_user_to_db(registration_data: RegistrationData):
    try:
        User.objects.create_user(registration_data.username, registration_data.email, registration_data.password)
    except DatabaseError as e:
        raise
