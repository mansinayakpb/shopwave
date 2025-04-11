from django.conf import settings
from django.contrib.auth import logout
from django.utils import timezone


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the auto logout feature is enabled
        auto_logout_enabled = getattr(settings, 'AUTO_LOGOUT_ENABLED', True)

        # Proceed only if auto logout is enabled
        if auto_logout_enabled and request.user.is_authenticated:
            now = timezone.now()
            last_activity = request.session.get('last_activity')

            if last_activity is None:
                request.session['last_activity'] = now.timestamp()
            else:
                if (now.timestamp() - last_activity) > 60:  # 3 minutes
                    logout(request)
                    request.session.flush()

            request.session['last_activity'] = now.timestamp()

        response = self.get_response(request)
        return response