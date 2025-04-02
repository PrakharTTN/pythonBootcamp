import logging

logger = logging.getLogger("__name__")


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user:
            logger.info(f"Request: {request.method} {request.path} from {request.user}")
        return self.get_response(request)
