import hashlib
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from .models import Feedback

logger = logging.getLogger(__name__)


def http_404(request):
    return render(
        request,
        "404.html",
    )


def http_500(request):
    return render(
        request,
        "500.html",
    )


class FeedbackView(View):
    template_name_exists = "feedback/bestaand.html"
    template_name_new = "feedback/nieuw.html"

    def get(
        self, request, meldr_nummer: str, meldr_hash: str, feedback_type: int
    ):
        try:
            verwachte_hash = hashlib.sha256((meldr_nummer + settings.SECRET_HASH_KEY).encode()).hexdigest()
            if verwachte_hash != meldr_hash:
                return HttpResponse(
                    "De hash komt niet overeen met de verwachte waarde."
                )

            if bestaande_feedback := Feedback.objects.filter(
                meldr_nummer=meldr_nummer
            ).first():
                context = {
                    "feedback": bestaande_feedback,
                }
                return render(request, self.template_name_exists, context)
            else:
                # No feedback entry with the same meldr_num found, create a new one
                # Determine the feedback type based on the URL parameter
                if feedback_type == 0:
                    feedback_type = "negatief"
                elif feedback_type == 1:
                    feedback_type = "positief"
                else:
                    # Handle an unexpected value for feedback_type
                    return HttpResponse("Ongeldige waarde voor feedback_type.")

                # Create a new feedback object
                nieuwe_feedback = Feedback(
                    meldr_nummer=meldr_nummer, feedback_type=feedback_type
                )
                nieuwe_feedback.save()
                context = {"feedback": nieuwe_feedback}
                return render(request, self.template_name_new, context)

        except Exception as e:
            # Handle unexpected errors
            logger.error(f"An error occurred: {str(e)}")
            return HttpResponse(
                "Er is een fout opgetreden bij het verwerken van uw verzoek."
            )
