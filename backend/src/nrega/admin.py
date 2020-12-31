from django.contrib import admin
from .models import Location, LibtechTag, Report, TaskQueue, Bundle
from .actions import reset_in_progress
# Register your models here.

class LocationModelAdmin(admin.ModelAdmin):
    """Model Adminf or class Location"""
    list_display = ["id", "name", "code", "accuracy"]
    list_filter = ["libtech_tag__name", "location_type", "scheme", "state_name"]
    search_fields = ["code", "name"]
    readonly_fields = ["parent_location"]
    class Meta:
        model = Location

class LibtechTagModelAdmin(admin.ModelAdmin):
    """Model Admin for class LibtetechTag"""
    list_display = ["id", "name"]
    class Meta:
        model = LibtechTag


class ReportModelAdmin(admin.ModelAdmin):
    """Model Adminf or class Report"""
    list_display = ["id", "location", "report_type", "updated",
                    "health", "finyear"]
    list_filter = ["health", "location_type", "finyear", "report_type"]
    search_fields = ["location__code", "location__name"]
    readonly_fields = ["location"]
    class Meta:
        model = Report
    def get_ordering(self, request):
                return ['-updated']

class TaskQueueModelAdmin(admin.ModelAdmin):
    """Model Admin for Task Queue"""
    actions = [reset_in_progress]
    list_display = ["id", "location_code", "report_type", "status",
                    "process_name"]
    list_filter = ["in_progress", "status", "report_type", "is_error", "is_done"]
    search_fields = ["location_code"]
    class Meta:
        model = TaskQueue


class BundleModelAdmin(admin.ModelAdmin):
    """Model Admin for class LibtetechTag"""
    list_display = ["id", "title"]
    class Meta:
        model = Bundle
admin.site.register(Location, LocationModelAdmin)
admin.site.register(LibtechTag, LibtechTagModelAdmin)
admin.site.register(Report, ReportModelAdmin)
admin.site.register(TaskQueue, TaskQueueModelAdmin)
admin.site.register(Bundle, BundleModelAdmin)
