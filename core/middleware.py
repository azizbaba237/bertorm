from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from .models import UserLoginHistory

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = reverse('core:login')
        self.exempt_urls = [
            reverse('core:login'),
            reverse('core:logout'),
            reverse('core:password_reset'),
            '/',  # Accueil
            # Ajoutez d'autres URLs publiques si nécessaire
        ]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            if request.path not in self.exempt_urls:
                return redirect(f"{self.login_url}?next={request.path}")
        return None

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            UserLoginHistory.objects.create(
                user=request.user,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip