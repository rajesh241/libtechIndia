from django.contrib import admin
from .models import Location, LibtechTag

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


admin.site.register(Location, LocationModelAdmin)
admin.site.register(LibtechTag, LibtechTagModelAdmin)
