from django.utils.deprecation import MiddlewareMixin

class LoginUserAgentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required Middleware"
        if request.user.is_authenticated:
            from file_protector.apps.users.models import UserAgentHistory
            UserAgentHistory.objects.create(
                user=request.user,
                agent=request.META.get("HTTP_USER_AGENT", "")
            )
            return None