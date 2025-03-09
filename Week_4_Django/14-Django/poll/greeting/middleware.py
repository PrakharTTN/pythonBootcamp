from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# BLOCKED_IPS = ["127.0.0.1", "192.168.1.1"]
BLOCKED_IPS = []


class RestrictIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if ip in BLOCKED_IPS:
            return HttpResponse("Access denied", status=403)
        return self.get_response(request)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(
            f"Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}"
        )
        return self.get_response(request)


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Processing request: {request.path}")

        response = self.get_response(request)

        print(f"Processing response: {response.status_code}")

        return response
