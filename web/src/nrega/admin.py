from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Location,Report,TaskQueue,Test,LibtechDataStatus

class testModelAdmin(admin.ModelAdmin):
  list_display=["id","name","address","isAdult"]
  class Meta:
    model=Test

class locationModelAdmin(ImportExportModelAdmin):
  list_display = ["name","stateShortCode","code","crawlIP","priority"]
  list_filter = ["locationType"]
  search_fields=["code"]
  readonly_fields = ["parentLocation"]
  class Meta:
    model=Location

class reportModelAdmin(admin.ModelAdmin):
  list_display = ["id","location","reportType","finyear","updated"]
  list_filter = ["reportType","finyear"]
  search_fields=["location"]
  readonly_fields = ["location"]
  class Meta:
    model=Report

class libtechDataStatusModelAdmin(admin.ModelAdmin):
  list_display = ["id","__str__","finyear","accuracy","updated"]
  list_filter = ["finyear"]
  search_fields=["ocation__code","location__name"]
  readonly_fields = ["location"]
  class Meta:
    model=LibtechDataStatus

class taskQueueModelAdmin(admin.ModelAdmin):
  list_display = ["id","reportType","priority","status","updated","isDone"]
  list_filter = ["reportType","status"]
  search_fields=["report__location__code","report__reportType"]
  readonly_fields = ["report"]
  class Meta:
    model=TaskQueue

admin.site.register(TaskQueue,taskQueueModelAdmin)
admin.site.register(Location,locationModelAdmin)
admin.site.register(Report,reportModelAdmin)
admin.site.register(LibtechDataStatus,libtechDataStatusModelAdmin)
admin.site.register(Test,testModelAdmin)
