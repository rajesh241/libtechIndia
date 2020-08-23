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


def report_post_save_operation(obj):
    """Report  Post save operation"""
    obj.location_code = obj.location.code
    obj.location_type = obj.location.location_type
    myTags = obj.libtech_tag.all()
    for tag in myTags:
        obj.libtech_tag.remove(tag)
    myTags = obj.location.libtech_tag.all()
    for tag in myTags:
        obj.libtech_tag.add(tag)
    obj.save()
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
        return data

    def create(self, validated_data):
        """Over riding teh create method of serializer"""
        obj = Report.objects.create(**validated_data)
        report_post_save_operation(obj)
        return obj

    def update(self, instance, validated_data):
        """Overriding the default instance method"""
        cur_report_url = validated_data.get("report_url", None)
        if cur_report_url is not None:
            if (cur_report_url != instance.report_url):
                p = {}
                p['updated'] = instance.updated.strftime("%Y-%m-%d")
                p['report_url'] = instance.report_url
                if instance.archive_reports is None:
                    instance.archive_reports = [p]
                else:
                    instance.archive_reports.append(p)
        for key,value in validated_data.items():
            setattr(instance, key, value)
         
        instance.save()
        report_post_save_operation(instance)
        return instance
