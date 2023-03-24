from typing import Callable
from django.contrib.sessions.middleware import SessionMiddleware


def insert_session(request, requested_view: Callable):
    session_middleware = SessionMiddleware(requested_view)
    session_middleware.process_request(request)
