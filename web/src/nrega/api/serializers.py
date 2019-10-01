from rest_framework import serializers,fields
from nrega.models import Location,Report,TaskQueue,Test,NREGANICError,LibtechDataStatus

class TestSerializer(serializers.ModelSerializer):
  class Meta:
    model=Test
    fields = '__all__'

class NREGANICErrorSerializer(serializers.ModelSerializer):
  class Meta:
    model=NREGANICError
    fields = '__all__'

class LibtechDataStatusSerializer(serializers.ModelSerializer):
  class Meta:
    model=LibtechDataStatus
    fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model=Location
    fields = '__all__'
  # fields=[
  #   'id',
  #   'name',
  #   'slug',
  #   'code',
  #   'stateShortCode',
  #   'crawlIP'
  #   ]

class ReportSerializer(serializers.ModelSerializer):
  class Meta:
    model=Report
    fields = '__all__'
   #fields=[
   #  'id',
   #  'location',
   #  'reportType',
   #  'finyear',
   #  'reportURL',

   #  ]

class TaskQueueSerializer(serializers.ModelSerializer):
  
  class Meta:
    model=TaskQueue
    fields = '__all__'

