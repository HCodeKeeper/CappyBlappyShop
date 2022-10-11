from custom_exceptions.session import EmptyTemporalRegistrationStorage
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError
from .api import *
from services.session import TemporalRegistrationStorage
from services.account import add_user_to_db
from helpers.account import Registration
from django.db.utils import DatabaseError


def get_login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return render(request, "login.html")


def get_registration_page(request):
    return render(request, "registration.html")


def register_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        token = Registration.get_email_token()
        storage = TemporalRegistrationStorage(request)
        storage.put(email, username, password, token)
        print(storage.get().get_token())

        return render(request, "verification_await.html")
    return HttpResponseNotAllowed


def get_token_verification_page(request):
    return render(request, "verification.html")


def verificate(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        if not Registration.validate_email_token_pattern(token):
            return HttpResponseBadRequest("Your token is invalid", content_type='text/plain')
        else:
            try:
                registration_data = TemporalRegistrationStorage(request).get()
            except EmptyTemporalRegistrationStorage:
                raise
            else:
                try:
                    stored_token = registration_data.get_token()
                except EmptyTemporalRegistrationStorage:
                    return HttpResponseBadRequest("Your token is different from what we sent", content_type='text/plain')
                else:
                    if token == stored_token:
                        try:
                            add_user_to_db(registration_data)
                        except DatabaseError as e:
                            raise DatabaseError("Couldn't add user", content_type='text/plain') from e
                            return HttpResponseServerError()
                        else:
                            # Succeeded
                            return redirect(reverse("account"))

    return HttpResponseNotAllowed


def account(request):
    return HttpResponse()
