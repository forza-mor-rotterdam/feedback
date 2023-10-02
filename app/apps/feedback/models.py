from django.db import models


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ("positief", "Positief"),
        ("negatief", "Negatief"),
    ]

    meldr_nummer = models.CharField(max_length=20)
    feedback_type = models.CharField(
        max_length=10,
        choices=FEEDBACK_TYPES,
        default="negatief",
    )
    aanmaakdatum = models.DateTimeField(
        auto_now_add=True
    )  # Datum en tijd van aanmaak automatisch invullen

    def formatted_date(self):
        return self.aanmaakdatum.strftime("%d-%m-%Y %H:%M:%S")

    def __str__(self) -> str:
        return f"Meldr nummer: {self.meldr_nummer}, Feedback Type: {self.feedback_type}, Aanmaakdatum: {self.formatted_date()}"

    class Meta:
        ordering = ("aanmaakdatum",)
        verbose_name_plural = "Feedback"
