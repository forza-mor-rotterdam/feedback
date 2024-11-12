from apps.feedback.views import (
    FeedbackMetricsView,
    FeedbackView,
    custom_404_view,
    custom_500_view,
    debug,
)
from apps.health.views import healthz
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django_db_schema_renderer.urls import schema_urls
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path("debug/", debug, name="debug"),
    path(
        "",
        RedirectView.as_view(
            url="admin/",
            permanent=False,
        ),
        name="redirect-to-django-admin",
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
    path("db-schema/", include((schema_urls, "db-schema"))),
    path("plate/", include("django_spaghetti.urls")),
]

if settings.OIDC_ENABLED:
    urlpatterns += [
        path(
            "admin/login/",
            RedirectView.as_view(
                url="/oidc/authenticate/?next=/admin/",
                permanent=False,
            ),
            name="admin_login",
        ),
        path(
            "admin/logout/",
            RedirectView.as_view(
                url="/oidc/logout/?next=/admin/",
                permanent=False,
            ),
            name="admin_logout",
        ),
    ]

urlpatterns += [
    path("admin/", admin.site.urls),
    path("oidc/", include("mozilla_django_oidc.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("404/", custom_404_view, name="404"),
        path("500/", custom_500_view, name="500"),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
