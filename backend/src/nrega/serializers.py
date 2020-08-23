from rest_framework import serializers, fields
from nrega.models import Location, LibtechTag, Report

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


    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        print("I am in validate method")
        return data

    def create(self, validated_data):
        """Over riding teh create method of serializer"""
        print("I am in create function")
        obj = Report.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        """Overriding the default instance method"""
        print("I am in update method")
        for key,value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
