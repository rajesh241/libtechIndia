"""Serializers for NREGA Module"""
from rest_framework import serializers, fields
from nrega.models import Location, Report, LibtechTag, TaskQueue

class LocationSerializer(serializers.ModelSerializer):
    """Serializer for module Location"""
    class Meta:
        """Meta Class"""
        model = Location
        fields = '__all__'

class LibtechTagSerializer(serializers.ModelSerializer):
    """Serializer for module LibtechTag"""
    class Meta:
        """Meta Class"""
        model = LibtechTag
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Report Model"""
    class Meta:
        """Meta Class"""
        model = Report
        fields = '__all__'
        optional_fields = ['finyear', ]



class TaskQueueSerializer(serializers.ModelSerializer):
    """Serializer for module TaskQueue"""
    class Meta:
        """Meta Class"""
        model = TaskQueue
        fields = '__all__'
