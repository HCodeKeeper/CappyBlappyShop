import re
import string
import random


class Registration:

    TOKEN_PATTERN = re.compile("[A-Z0-9-]{6}")

    @classmethod
    def get_email_token(cls, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @classmethod
    def validate_email_token_pattern(cls, token):
        return Registration.TOKEN_PATTERN.match(token)