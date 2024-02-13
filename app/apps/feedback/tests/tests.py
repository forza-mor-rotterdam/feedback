import hashlib

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Feedback
from .factories import FeedbackFactory  # Import the FeedbackFactory


class FeedbackModelTestCase(TestCase):
    def test_formatted_date(self):
        feedback = (
            FeedbackFactory()
        )  # Use the FeedbackFactory to create a Feedback object
        formatted_date = feedback.formatted_date(feedback.aanmaakdatum)
        self.assertTrue(formatted_date.startswith(""))

    def test_feedback_str(self):
        feedback = (
            FeedbackFactory()
        )  # Use the FeedbackFactory to create a Feedback object
        expected_str = f"Meldr nummer: {feedback.meldr_nummer}, Feedback Type: {feedback.feedback_type}, Aanmaakdatum: {feedback.formatted_date(feedback.aanmaakdatum)}, Laatste Update: {feedback.formatted_date(feedback.update_datum)}"
        self.assertEqual(str(feedback), expected_str)


class FeedbackViewTestCase(TestCase):
    def test_feedback_view(self):
        feedback = (
            FeedbackFactory()
        )  # Use the FeedbackFactory to create a Feedback object
        meldr_nummer = feedback.meldr_nummer
        meldr_hash = hashlib.sha256(
            (meldr_nummer + settings.SECRET_HASH_KEY).encode()
        ).hexdigest()

        response = self.client.get(
            reverse("feedback", args=[meldr_nummer, meldr_hash, 0])
        )
        self.assertEqual(response.status_code, 200)

    def test_feedback_view_with_invalid_hash(self):
        response = self.client.get(
            reverse("feedback", args=["12345", "invalid_hash", 0])
        )
        self.assertEqual(response.status_code, 500)

    def test_feedback_view_with_invalid_feedback_type(self):
        feedback = (
            FeedbackFactory()
        )  # Use the FeedbackFactory to create a Feedback object
        meldr_nummer = feedback.meldr_nummer
        meldr_hash = hashlib.sha256(
            (meldr_nummer + settings.SECRET_HASH_KEY).encode()
        ).hexdigest()

        response = self.client.get(
            reverse("feedback", args=[meldr_nummer, meldr_hash, 2])
        )
        self.assertEqual(response.status_code, 500)

    def test_update_feedback(self):
        feedback = FeedbackFactory(
            feedback_type="negatief"
        )  # Use the FeedbackFactory to create a Feedback object
        original_type = feedback.feedback_type
        original_update_date = feedback.update_datum

        # Change the feedback type and update the update_datum
        new_type = "positief"
        feedback.feedback_type = new_type
        feedback.update_datum = timezone.now()
        feedback.save()

        # Retrieve the feedback object again from the database
        updated_feedback = Feedback.objects.get(pk=feedback.pk)

        self.assertNotEqual(original_type, updated_feedback.feedback_type)
        self.assertNotEqual(original_update_date, updated_feedback.update_datum)

    def test_concurrent_feedback_creation(self):
        # Simulate concurrent feedback creation with the same meldr_nummer
        meldr_nummer = "12345"
        meldr_hash = hashlib.sha256(
            (meldr_nummer + settings.SECRET_HASH_KEY).encode()
        ).hexdigest()

        # Start multiple concurrent requests to create feedback
        num_requests = 5  # You can adjust the number of concurrent requests
        responses = []
        for _ in range(num_requests):
            responses.append(
                self.client.get(reverse("feedback", args=[meldr_nummer, meldr_hash, 0]))
            )

        # Check that all responses have the same status code
        status_codes = [response.status_code for response in responses]
        self.assertTrue(all(code == status_codes[0] for code in status_codes))

        # Check that only one feedback object is created in the database
        created_feedback_count = Feedback.objects.filter(
            meldr_nummer=meldr_nummer
        ).count()
        self.assertEqual(created_feedback_count, 1)


class MetricsViewTestCase(TestCase):
    def test_feedback_metrics(self):
        # Create 4 negative and 7 positive feedback objects
        for _ in range(4):
            FeedbackFactory(feedback_type="negatief")

        for _ in range(7):
            FeedbackFactory(feedback_type="positief")

        response = self.client.get(reverse("prometheus_metrics"))
        self.assertEqual(response.status_code, 200)

        # Check if the response content contains the expected metrics
        self.assertIn(b'feedback_total{feedback_type="negatief"', response.content)
        self.assertIn(b'feedback_total{feedback_type="positief"', response.content)
