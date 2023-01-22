from smtplib import SMTPException
from celery import shared_task
from django.core.mail import send_mail
from services.mailing import get_registration_token_html, get_password_update_token_html
from cappy_blappy_shop.settings import EMAIL_HOST_USER


@shared_task
def send_registration_token(user_email, token):
    html_message = get_registration_token_html(token)
    try:
        is_sent = bool(send_mail("ClappyBlappyShop: Submit your registration", "",
                                 recipient_list=[user_email], html_message=html_message, from_email=EMAIL_HOST_USER))
    except SMTPException:
        raise
    return is_sent


@shared_task
def send_password_update_token(user_email, token):
    html_message = get_password_update_token_html(token)
    try:
        is_sent = bool(send_mail("ClappyBlappyShop: Complete updating your password", "",
                                 recipient_list=[user_email], html_message=html_message, from_email=EMAIL_HOST_USER))
    except SMTPException:
        raise
    return is_sent
