from custom_exceptions.session import EmptyTemporalRegistrationStorage
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError
from django.urls import reverse_lazy
from .api import *
from services.session import TemporalRegistrationStorage, TemporalPasswordUpdateTokenStorage
from services.account import *
from services.account import update_password as update_account_password
from helpers.account import TokenGenerator
from django.db.utils import DatabaseError
from services import mailing
from smtplib import SMTPException
from django.db import transaction
from user_profiles.models import Profile
from helpers.validators import validate_phone_nubmer


def get_login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return render(request, "login.html")


def get_registration_page(request):
    return render(request, "registration.html")


def register_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        if lookup_user(email) is not None:
            return render(request, "registration_invalid.html")
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        token = TokenGenerator.get_token()
        storage = TemporalRegistrationStorage(request)
        storage.put(email, username, password, token)

        try:
            is_token_sent = mailing.send_registration_token(email, token)
        except SMTPException:
            raise
        return render(request, "verification_await.html")
    return HttpResponseNotAllowed


def get_token_verification_page(request):
    return render(request, "verification.html")


@transaction.atomic
def verificate(request):
    if request.method == 'POST':
        token = request.POST.get('token', '').upper()
        if not TokenGenerator.validate_token_pattern(token):
            return HttpResponseBadRequest("Your token is invalid", content_type='text/plain')
        else:
            try:
                registration_storage = TemporalRegistrationStorage(request)
                registration_data = registration_storage.get()
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
                            register(registration_data)
                        except DatabaseError as e:
                            raise DatabaseError("Couldn't add user", content_type='text/plain') from e
                            return HttpResponseServerError()
                        else:
                            registration_storage.clean()
                            # Succeeded
                            return redirect(reverse("account"))

    return HttpResponseNotAllowed


# Forgot password views
def update_password_email(request):
    return render(request, "update_password_email.html")


def update_password(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        if lookup_user(email) is None:
            return HttpResponseBadRequest("Invalid credits. Your email isn't attached to any account in our service.",
                                          content_type="text/plain")
        else:
            try:
                token = TokenGenerator.get_token()
                storage = TemporalPasswordUpdateTokenStorage(request)
                storage.put(token)
                mailing.send_password_update_token(email, token)
            except SMTPException:
                raise
            return render(request, "update_password.html", context={'email': email})

    return HttpResponseBadRequest()


def update_password_perform(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        token = request.POST.get('token').upper()
        storage = TemporalPasswordUpdateTokenStorage(request)
        try:
            token_stored = storage.get()
            if token != token_stored:
                return HttpResponseBadRequest("Invalid token. Token that you sent is different from one we store",
                                              content_type="text/plain")
            else:
                update_account_password(email, password)
                return redirect(reverse('login_page'))
        except DatabaseError:
            raise
            return HttpResponseServerError()
    return HttpResponseBadRequest()


@login_required(login_url=reverse_lazy('login_page'))
def account(request):
    username = request.user.get_username()
    profile = Profile.objects.get(user__username=username)
    return render(request, 'account.html', context={
        "first_name": profile.first_name,
        "second_name": profile.second_name,
        "email": profile.email,
        "premium_active": profile.has_premium,
        "telephone": profile.telephone.number
    })


@login_required(login_url=reverse_lazy('login_page'))
def get_edit_profile_page(request):
    return render(request, "change_profile_credits.html")


@login_required(login_url=reverse_lazy('login_page'))
def edit_profile(request):
    if request.method == 'POST':
        profile = get_profile_from_request(request)
        first_name = request.POST.get("first_name")
        second_name = request.POST.get("second_name")
        telephone = request.POST.get("telephone")
        if not validate_phone_nubmer(telephone):
            return HttpResponseBadRequest("Your telephone number is invalid", content_type="text/plain")
        update_profile(profile, first_name, second_name, telephone)

        return redirect(reverse('account'))
    return HttpResponseBadRequest()
