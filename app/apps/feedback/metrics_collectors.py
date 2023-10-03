from apps.feedback.models import Feedback
from django.db.models import Count
from prometheus_client.core import CounterMetricFamily


class FeedbackCollector(object):
    def collect(self):
        c = CounterMetricFamily(
            "feedback_total",
            "Feedback aantallen",
            labels=["feedback_type", "update_datum"],
        )
        feedbacken = (
            Feedback.objects.order_by("feedback_type")
            .values("feedback_type")
            .annotate(count=Count("feedback_type"))
        )
        print(feedbacken)
        for m in feedbacken:
            c.add_metric(
                [
                    m.get("feedback_type"),
                ],
                m.get("count"),
            )
        print(f"=== {c} ===")
        yield c
