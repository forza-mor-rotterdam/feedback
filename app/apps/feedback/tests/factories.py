import factory
from apps.feedback.models import Feedback


class FeedbackFactory(factory.django.DjangoModelFactory):
    meldr_nummer = factory.Sequence(lambda n: f"2023-{str(n).zfill(6)}")
    feedback_type = "positief"

    class Meta:
        model = Feedback
        django_get_or_create = ["feedback_type"]
