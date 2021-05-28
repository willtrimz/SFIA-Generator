from django.conf import settings
from django.utils import translation

# Used to ensure force the admin site to be in english
# Implemented as admin did not need to be available in Welsh but was doing so automatically
# Leading to mismatch of Welsh UI but English model names
class AdminLocaleURLMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        if request.path.startswith('/admin'):
            request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG