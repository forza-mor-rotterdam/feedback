from apps.authenticatie.views import LoginView, LogoutView
from apps.feedback.views import (
    FeedbackMetricsView,
    FeedbackView,
    custom_404_view,
    custom_500_view,
    home,
)
from apps.health.views import healthz
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", home, name="home"),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path("metrics/", FeedbackMetricsView.as_view(), name="prometheus_metrics"),
    # URL pattern for https://feedback.forzamor.nl/vertel-het-ons/{meldr-nummer}/{hash}/1
    path(
        "vertel-het-ons/<str:meldr_nummer>/<str:meldr_hash>/<int:meldr_feedback_type>/",
        FeedbackView.as_view(),
        name="feedback",
    ),
    path("health/", include("health_check.urls")),
    path("healthz/", healthz, name="healthz"),
]

if not settings.ENABLE_DJANGO_ADMIN_LOGIN:
    urlpatterns += [
        path(
            "admin/login/",
            RedirectView.as_view(url="/login/?next=/admin/"),
            name="admin_login",
        ),
        path(
            "admin/logout/",
            RedirectView.as_view(url="/logout/?next=/"),
            name="admin_logout",
        ),
    ]

if settings.OIDC_ENABLED:
    urlpatterns += [
        path("oidc/", include("mozilla_django_oidc.urls")),
    ]

urlpatterns += [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", custom_404_view, name="404"),
        path("500/", custom_500_view, name="500"),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
