import hashlib
import logging

import prometheus_client
from apps.feedback.metrics_collectors import FeedbackCollector
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from .models import Feedback

logger = logging.getLogger(__name__)


def custom_404_view(request):
    return render(request, "404.html", status=404)


def custom_500_view(request):
    return render(request, "500.html", status=500)


def debug(request):
    import sys
    import traceback

    response = None
    try:
        print("try with template")
        response = render(request, "debug.html")
    except Exception:
        print("fail try with template")
        traceback.print_exception(*sys.exc_info())

    if not response:
        try:
            print("try no template")
            response = HttpResponse("OK")
        except Exception:
            print("fail try no template")
            traceback.print_exception(*sys.exc_info())
    return response


class FeedbackView(View):
    template = "feedback/bedankt.html"

    def get(
        self,
        request,
        meldr_nummer: str,
        meldr_hash: str,
        meldr_feedback_type: int,
    ):
        try:
            # Vergelijk hashes
            verwachte_hash = hashlib.sha256(
                (meldr_nummer + settings.SECRET_HASH_KEY).encode()
            ).hexdigest()
            if verwachte_hash != meldr_hash:
                logger.error("Feedback hashes don't match")
                return HttpResponseServerError(
                    "De hash komt niet overeen met de verwachte waarde.",
                    status=500,
                )

            # Bepaal feedback_type op basis van URL parameter
            if meldr_feedback_type == 0:
                feedback_type = "negatief"
            elif meldr_feedback_type == 1:
                feedback_type = "positief"
            else:
                logger.error(
                    f"Incorrect value for meldr_feedback_type: {meldr_feedback_type}"
                )
                return HttpResponseServerError(
                    f"Ongeldige waarde voor meldr_feedback_type: {meldr_feedback_type}.",
                    status=500,
                )
            # Update of create Feedback object
            feedback, _created = Feedback.objects.update_or_create(
                meldr_nummer=meldr_nummer,
                defaults={
                    "feedback_type": feedback_type,
                    "update_datum": timezone.now(),
                },
            )
            feedback.save()
            context = {"feedback": feedback}
            return render(request, self.template, context)

        except Exception as e:
            # Afhandelen onverwachte errors
            logger.error(f"An error occurred: {str(e)}")
            return HttpResponseServerError(
                "Er is een fout opgetreden bij het verwerken van uw verzoek.",
                status=500,
            )


class FeedbackMetricsView(View):
    def get(self, request):
        try:
            registry = prometheus_client.CollectorRegistry()
            registry.register(FeedbackCollector())
            metrics_page = prometheus_client.generate_latest(registry)
            return HttpResponse(
                metrics_page,
                content_type=prometheus_client.CONTENT_TYPE_LATEST,
            )
        except Exception as e:
            # Afhandelen onverwachte errors
            logger.error(f"An error occurred: {str(e)}")
            return HttpResponseServerError(
                "Er is een fout opgetreden bij het ophalen van de metrics.",
                status=500,
            )


# Gebruik custom error handlers
handler404 = "apps.views.custom_404_view"
handler500 = "apps.views.custom_500_view"
