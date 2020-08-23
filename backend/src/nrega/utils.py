"""Simple utility functions for views"""
import json
from nrega.models import Location, Report

def is_json(json_data):
    """Determines if the passed data in json format"""
    try:
        real_json = json.loads(json_data)
        valid_json = True
    except ValueError:
        valid_json = False
    return valid_json

def tag_location_reports(location_obj, tag):
    """Will tag all reports of the given location"""
    objs = Report.objects.filter(location=location_obj)
    for obj in objs:
        obj.libtech_tag.add(tag)
def tag_locations(locations, tag, recursive=True):
    """This function will tag the locations recursively"""
    lowest_location_type = 'panchayat'
    objs = Location.objects.filter(code__in = locations)
    for obj in objs:
        obj.libtech_tag.add(tag)
        tag_location_reports(obj, tag)
    if len(objs) > 0:
        current_location_type = objs[0].location_type
    while (current_location_type != lowest_location_type):
        new_objs = []
        for obj in objs:
            child_objs = Location.objects.filter(parent_location = obj)
            new_objs.extend(child_objs)
        objs = new_objs
        if len(objs) == 0:
            break
        for obj in objs:
            obj.libtech_tag.add(tag)
            tag_location_reports(obj, tag)
        current_location_type = objs[0].location_type


