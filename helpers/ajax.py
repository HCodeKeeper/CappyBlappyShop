from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from typing import Callable, TypeVar


def process_ajax(func: Callable[[HttpRequest, ...], TypeVar('JsonLike')], method='GET') -> JsonResponse:
    def wrapper(request, *args, **kwargs):
        if not is_ajax(request):
            return HttpResponseBadRequest('Ajax header isn\'t found')
        else:
            if request.method == method:
                json = func(request, *args, **kwargs)
                return JsonResponse(json)
            return JsonResponse({'status': 'Invalid request'}, status=400)
    return wrapper


def is_ajax(request: HttpRequest):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True
    return False
