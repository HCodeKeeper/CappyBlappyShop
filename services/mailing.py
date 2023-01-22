from django.shortcuts import reverse
from cappy_blappy_shop.settings import DOMAIN


def get_registration_token_html(token):
    html = f'''
<h1>To submit your registration,</h1><p1> click on this <a href="{DOMAIN + reverse("get_token_verification_page")}">link</a></p1>
<h3>And enter this token:</h3><br><h1>{token}</h1>
'''
    return html


def get_password_update_token_html(token):
    html = f'''
<h1>To update your password,</h1>
<h3>And enter this token:</h3><br><h1>{token}</h1>
'''
    return html
