from rest_framework import serializers, fields
from nrega.models import Location, LibtechTag

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


