import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View

logger = logging.getLogger(__name__)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if settings.OIDC_ENABLED:
            return redirect("/oidc/authenticate/")
        if settings.ENABLE_DJANGO_ADMIN_LOGIN:
            return redirect(f"/admin/login/?next={request.GET.get('next', '/admin')}")

        return HttpResponse("Er is geen login ingesteld")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if settings.OIDC_ENABLED:
            return redirect("/oidc/logout/")
        if settings.ENABLE_DJANGO_ADMIN_LOGIN:
            return redirect(f"/admin/logout/?next={request.GET.get('next', '/')}")

        return HttpResponse("Er is geen logout ingesteld")
