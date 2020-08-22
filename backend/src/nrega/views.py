import json
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, generics, permissions
from nrega.models import Location, LibtechTag
from nrega.mixins import HttpResponseMixin
from nrega.serializers import (LocationSerializer,
                          LibtechTagSerializer)
from nrega.utils import is_json

def get_id_from_request(request):
    """Small function to retrieve the Id from request
    It can either take id from get parameters
    or it can retrieve id from the input Json data
    """
    url_id = request.GET.get('id', None)
    input_json_id = None
    if is_json(request.body):
        input_json_data = json.loads(request.body)
        input_json_id = input_json_data.get("id", None)
    input_id = url_id or input_json_id or None
    return input_id

class LibtechTagAPIView(HttpResponseMixin,
                      mixins.RetrieveModelMixin,
                      generics.ListAPIView):
    """API view Class for Libtech Tag. This defines only get method"""
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, xIsAdminOwnerOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LibtechTagSerializer
    passed_id = None
    input_id = None
    search_fields = ('name')
    ordering_fields = ('name', 'id')
    filter_fields = ('name', 'id')
    queryset = LibtechTag.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


class LocationAPIView(HttpResponseMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.ListAPIView):
    """API view Class for Location. This defines only get method"""
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly, xIsAdminOwnerOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LocationSerializer
    passed_id = None
    input_id = None
    search_fields = ('name')
    ordering_fields = ('name', 'id')
    filter_fields = ('name', 'code', 'scheme', 'location_type', 'state_code',
                     'district_code', 'block_code', 'panchayat_code',
                     'parent_location__code', 'libtech_tag',
                     'libtech_tag__name')
    queryset = Location.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        """patch method will update the object, with the specified fields. All
        fields need not be present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.partial_update(request, *args, **kwargs)


