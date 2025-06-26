# Django
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseNotFound

class Redirect404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if isinstance(response, HttpResponseNotFound):
            if request.user.is_authenticated:
                return redirect('dashboard:index')
            return redirect(reverse('users:users_web:web_auth:auth_email_password'))
        return response
