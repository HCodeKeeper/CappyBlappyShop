from custom_exceptions.session import EmptyTemporalRegistrationStorage
from helpers.account import Registration


class TemporalRegistrationStorage:
    KEY = "temporal_registration_data"

    def __init__(self, request):
        self.key = TemporalRegistrationStorage.KEY
        self.request = request
        self.session = request.session
        self.assert_keyword_exist()
        self.storage = self.session[self.key]

    def assert_keyword_exist(self):
        if not self.request.session.get(self.key, False):
            self.request.session[self.key] = {}
            self.request.session.modified = True

    def put(self, email, username, password, token):
        self.request.session[self.key] = {
            "email": email,
            "username": username,
            "password": password,
            "token": token
        }
        self.session.modified = True

    def get(self):
        return TemporalRegistrationData.create_from_storage(self)

    def clean(self):
        self.request.session[self.key] = {}
        self.request.session.modified = True

    def exists(self):
        if not all(map(lambda key: self.request.session[self.key].get(key, False), ["email", "username", "password", "token"])):
            return False
        return True

    def update_token(self):
        if not self.exists():
            raise EmptyTemporalRegistrationStorage("Tried to update token, although registration data doesn't exist")
        self.request.session[self.key]["token"] = Registration.get_email_token()


class RegistrationData:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password


class TemporalRegistrationData(RegistrationData):
    def __init__(self, email, username, password, token):
        super().__init__(email, username, password)
        self.token = token

    def get_token(self):
        return self.token

    @classmethod
    def create_from_storage(cls, storage: TemporalRegistrationStorage):
        data = storage.request.session[storage.key]
        if not storage.exists():
            raise EmptyTemporalRegistrationStorage("Tried to retrieve registration data, although it doesn't exist in the session")
        return TemporalRegistrationData(data["email"], data["username"], data["password"], data["token"])
