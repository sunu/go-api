from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin

from lang.admin import TranslationAdmin
from .models import (
    Dref,
    DrefFile,
    DrefOperationalUpdate,
    DrefFinalReport,
)


@admin.register(DrefFile)
class DrefFileAdmin(admin.ModelAdmin):
    search_fields = ("file",)


@admin.register(Dref)
class DrefAdmin(CompareVersionAdmin, TranslationAdmin, admin.ModelAdmin):
    search_fields = ("title",)
    list_display = (
        "title",
        "national_society",
        "disaster_type",
        "ns_request_date",
        "submission_to_geneva",
        "status",
    )
    autocomplete_fields = (
        "created_by",
        "modified_by",
        "field_report",
        "national_society",
        "disaster_type",
        "users",
        "event_map",
        "images",
        "budget_file",
        "cover_image",
        "country",
        "district",
        "supporting_document",
        "assessment_report",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "created_by",
                "modified_by",
                "field_report",
                "national_society",
                "disaster_type",
                "event_map",
                "budget_file",
                "cover_image",
                "country",
                "supporting_document",
                "assessment_report",
            )
            .prefetch_related(
                "planned_interventions",
                "needs_identified",
                "national_society_actions",
                "users",
                "district",
                "images",
            )
        )


@admin.register(DrefOperationalUpdate)
class DrefOperationalUpdateAdmin(CompareVersionAdmin, TranslationAdmin, admin.ModelAdmin):
    list_display = ("title", "national_society", "disaster_type")
    autocomplete_fields = (
        "national_society",
        "disaster_type",
        "images",
        "users",
        "event_map",
        "images",
        "budget_file",
        "cover_image",
        "dref",
        "country",
        "assessment_report",
        "photos",
        "district",
    )
    list_filter = ["dref"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "created_by",
                "modified_by",
                "national_society",
                "disaster_type",
                "event_map",
                "budget_file",
                "cover_image",
                "country",
                "assessment_report",
            )
            .prefetch_related("planned_interventions", "needs_identified", "national_society_actions", "users")
        )


@admin.register(DrefFinalReport)
class DrefFinalReportAdmin(CompareVersionAdmin, admin.ModelAdmin):
    list_display = ("title", "national_society", "disaster_type")
    autocomplete_fields = (
        "national_society",
        "disaster_type",
        "photos",
        "dref",
    )
    list_filter = ["dref"]
    search_fields = ["title", "national_society__name"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "created_by",
                "modified_by",
                "national_society",
                "disaster_type",
                "event_map",
                "cover_image",
                "country",
                "assessment_report",
            )
            .prefetch_related("planned_interventions", "needs_identified", "national_society_actions", "users")
        )
