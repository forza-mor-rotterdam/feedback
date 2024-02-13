from django.db import models
from django.utils import timezone


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ("positief", "Positief"),
        ("negatief", "Negatief"),
    ]

    meldr_nummer = models.CharField(max_length=20, unique=True)
    feedback_type = models.CharField(
        max_length=10,
        choices=FEEDBACK_TYPES,
        default="negatief",
    )
    aanmaakdatum = models.DateTimeField(
        auto_now_add=True
    )  # Datum en tijd van aanmaak automatisch invullen
    update_datum = models.DateTimeField(default=timezone.now)

    def formatted_date(self, date: timezone.datetime) -> str:
        return date.strftime("%d-%m-%Y %H:%M:%S")

    def __str__(self) -> str:
        return f"Meldr nummer: {self.meldr_nummer}, Feedback Type: {self.feedback_type}, Aanmaakdatum: {self.formatted_date(self.aanmaakdatum)}, Laatste Update: {self.formatted_date(self.update_datum)}"

    class Meta:
        ordering = ("aanmaakdatum",)
        verbose_name_plural = "Feedback"
