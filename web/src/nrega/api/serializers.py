from rest_framework import serializers
from nrega.models import Location,Report,CrawlQueue


class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model=Location
    fields=[
      'id',
      'name',
      'slug',
      'code',
      'stateShortCode',
      'crawlIP'
      ]

class ReportSerializer(serializers.ModelSerializer):
  class Meta:
    model=Report
    fields=[
      'id',
      'location',
      'reportType',
      'finyear',
      'reportURL',

      ]

class CrawlQueueSerializer(serializers.ModelSerializer):
  class Meta:
    model=CrawlQueue
    fields=[
      'id',
      'report',
      'status',

      ]

