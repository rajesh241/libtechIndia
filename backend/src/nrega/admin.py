"""Defination for Admin Interface"""
from django.contrib import admin
from .models import Location, Report, LibtechTag
# Register your models here.
class LocationModelAdmin(admin.ModelAdmin):
    """Model Adminf or class Location"""
    list_display = ["id", "name", "english_name", "code", "crawl_ip"]
    list_filter = ["location_type", "scheme"]
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
admin.site.register(Location, LocationModelAdmin)
admin.site.register(Report, ReportModelAdmin)
admin.site.register(LibtechTag, LibtechTagModelAdmin)
