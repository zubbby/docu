# myapp/middleware.py

from django.http import HttpResponseForbidden

BLACKLISTED_IPS = ['66.249.93.7', '66.249.83.128']  # List of blacklisted IPs

class BlockedIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client's IP address
        ip = request.META.get('REMOTE_ADDR')

        # Check if the IP is in the blacklist
        if ip in BLACKLISTED_IPS:
            return HttpResponseForbidden("Access Denied")

        # Continue processing the request
        response = self.get_response(request)
        return response
