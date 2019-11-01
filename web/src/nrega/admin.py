from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Location,Report,TaskQueue,Test,LibtechDataStatus,LibtechTag
from .actions import download_reports_zip

class testModelAdmin(admin.ModelAdmin):
  list_display=["id","name","address","isAdult"]
  class Meta:
    model=Test

class libtechTagModelAdmin(admin.ModelAdmin):
  list_display=["id","name","slug"]
  class Meta:
    model=LibtechTag

class locationModelAdmin(ImportExportModelAdmin):
  list_display = ["name","stateShortCode","code","crawlIP","priority"]
  list_filter = ["locationType","scheme"]
  search_fields=["code","name"]
  readonly_fields = ["parentLocation"]
  class Meta:
    model=Location

class reportModelAdmin(admin.ModelAdmin):
  actions = [download_reports_zip]
  list_display = ["id","location","reportType","finyear","updated"]
  list_filter = ["reportType","finyear"]
  search_fields=["location__code","location__name"]
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
  list_display = ["id","locationCode","reportType","priority","status","updated","duration","processName"]
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
admin.site.register(LibtechTag,libtechTagModelAdmin)
