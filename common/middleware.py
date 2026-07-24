from django.http import HttpResponseForbidden
from django.conf import settings

class ClientIPRestrictionMiddleware:
    """
    Middleware to restrict API access to specific client IP addresses or prefixes.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract the real client IP, considering reverse proxies
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        if not ip:
            return HttpResponseForbidden("Access Denied: Client IP address cannot be determined.")

        # Check if IP restriction is enabled
        restrict_ips = getattr(settings, 'RESTRICT_IPS', True)
        if not restrict_ips:
            return self.get_response(request)

        # Load configurations from settings
        allowed_ips = getattr(settings, 'ALLOWED_CLIENT_IPS', ['127.0.0.1', '::1'])
        allowed_prefixes = getattr(settings, 'ALLOWED_CLIENT_IP_PREFIXES', ['192.168.1.'])

        # Check if the client IP is allowed
        is_allowed = False
        if ip in allowed_ips:
            is_allowed = True
        else:
            for prefix in allowed_prefixes:
                if ip.startswith(prefix):
                    is_allowed = True
                    break

        if not is_allowed:
            return HttpResponseForbidden(f"Access Denied: IP {ip} is not whitelisted.")

        return self.get_response(request)
