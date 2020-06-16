"""Defination for Admin Interface"""
from django.contrib import admin
from .models import Location, Report, LibtechTag, TaskQueue
# Register your models here.
class LocationModelAdmin(admin.ModelAdmin):
    """Model Adminf or class Location"""
    list_display = ["id", "name", "code", "accuracy"]
    list_filter = ["is_data_available", "location_type", "scheme"]
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
    list_display = ["id", "location", "report_type", "finyear"]
    list_filter = ["finyear", "report_type"]
    search_fields = ["location__code", "location__name"]
    readonly_fields = ["location"]
    class Meta:
        model = Report

class TaskQueueModelAdmin(admin.ModelAdmin):
    """Model Admin for Task Queue"""
    list_display = ["id", "location_code", "report_type", "status",
                    "process_name"]
    list_filter = ["status", "report_type", "is_error", "is_done"]
    search_fields = ["location_code"]
    class Meta:
        model = TaskQueue
admin.site.register(Location, LocationModelAdmin)
admin.site.register(Report, ReportModelAdmin)
admin.site.register(LibtechTag, LibtechTagModelAdmin)
admin.site.register(TaskQueue, TaskQueueModelAdmin)
