"""Defination for Admin Interface"""
from django.contrib import admin
from .models import Location
# Register your models here.
class LocationModelAdmin(admin.ModelAdmin):
    """Model Adminf or class Location"""
    list_display = ["id", "name", "state_short_code", "code", "crawl_ip"]
    list_filter = ["location_type", "scheme"]
    search_fields = ["code", "name"]
    readonly_fields = ["parent_location"]
    class Meta:
        model = Location


admin.site.register(Location, LocationModelAdmin)
