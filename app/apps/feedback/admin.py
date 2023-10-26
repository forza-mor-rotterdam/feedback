from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("meldr_nummer", "feedback_type", "aanmaakdatum")
    list_filter = ("feedback_type", "aanmaakdatum")
    search_fields = ("meldr_nummer",)


AdminSite.site_title = "Feedback Admin"
AdminSite.site_header = "Feedback Admin"
AdminSite.index_title = "Feedback Admin"


admin.site.register(Feedback, FeedbackAdmin)
