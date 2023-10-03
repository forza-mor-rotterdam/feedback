from django.contrib import admin

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("meldr_nummer", "feedback_type", "aanmaakdatum")
    list_filter = ("feedback_type", "aanmaakdatum")
    search_fields = ("meldr_nummer",)


admin.site.register(Feedback, FeedbackAdmin)
