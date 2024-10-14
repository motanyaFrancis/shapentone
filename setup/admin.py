# Register your models here.
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE

from setup.models import (
    CategorySetup,
    CircuitSetup,
    EquipmentSetup,
    ExerciseSetup,
    IntensitySetup,
    LevelSetup,
    NumberSeries,
    NumberSeriesLine,
    Policy,
    ProgramSetup,
    Setup,
    WorkoutSetup,
)


class PrayerRequestInline(admin.TabularInline):
    model = NumberSeriesLine
    extra = 1


class NoSeriesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sample_no",
        "last_used_no",
        "last_date_used",
        "default_no",
        "manual_no",
    )
    search_fields = ("name",)
    readonly_fields = ("last_used_no", "sample_no")
    list_filter = ("default_no", "manual_no")
    inlines = [
        PrayerRequestInline,
    ]


admin.site.register(NumberSeries, NoSeriesAdmin)


class SetupAdmin(admin.ModelAdmin):
    list_display = (
        "ID",
        "site_name",
        "front_end_domain",
    )
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "site_name",
                    "front_end_domain",
                    "front_end_port",
                    "registration_allowed",
                )
            },
        ),
        (
            "Numbering",
            {
                "fields": (
                    "member_nos",
                    "invoice_nos",
                )
            },
        ),
    )


admin.site.register(Setup, SetupAdmin)


class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("datetime", "subject", "recipients", "success")
    search_fields = ("subject", "message")
    list_filter = ("success",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# admin.site.register(EmailLog, EmailLogAdmin)


class ProgramSetupAdmin(admin.ModelAdmin):
    list_display = ["title"]


admin.site.register(ProgramSetup, ProgramSetupAdmin)


class WorkoutSetupAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]


admin.site.register(WorkoutSetup, WorkoutSetupAdmin)


class CircuitSetupAdmin(admin.ModelAdmin):
    list_display = [
        "title",
    ]


admin.site.register(CircuitSetup, CircuitSetupAdmin)


class ExerciseSetupAdmin(admin.ModelAdmin):
    list_display = ['title', 'thumbnail',]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    search_fields = ['title']
    list_per_page = 40

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "exercise_setup":
            kwargs["queryset"] = ExerciseSetup.objects.order_by("title")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def admin_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj}" width="150px"  />'.format(self.image.url))


admin.site.register(ExerciseSetup, ExerciseSetupAdmin)


class CategorySetupAdmin(admin.ModelAdmin):
    list_display = ["title"]


admin.site.register(CategorySetup)


class EquipmentSetupAdmin(admin.ModelAdmin):
    list_display = [
        "title",
    ]


admin.site.register(EquipmentSetup, EquipmentSetupAdmin)


class LevelSetupAdmin(admin.ModelAdmin):
    list_display = [
        "title",
    ]


admin.site.register(LevelSetup)
admin.site.register(IntensitySetup)


class PolicyAdmin(admin.ModelAdmin):
    list_display = ["title", "slug"]
    list_filter = [
        "title",
    ]
    readonly_fields = [
        "slug",
    ]


admin.site.register(Policy, PolicyAdmin)
