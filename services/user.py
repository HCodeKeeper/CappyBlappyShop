from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned


# Used by abandoned review service
def get_name_by_id(_id):
    try:
        user = User.objects.get(id=_id)
    except User.DoesNotExist or MultipleObjectsReturned:
        raise
    else:
        name = f"{user.first_name} {user.last_name}"
    return name
