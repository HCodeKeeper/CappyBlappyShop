from django.http import HttpRequest

def is_ajax(request : HttpRequest):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True
    return False