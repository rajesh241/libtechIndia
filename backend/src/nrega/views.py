import json
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.db.models import Count
from rest_framework import viewsets
from rest_framework import (generics, authentication, permissions,
                            status, mixins, exceptions)
from rest_framework.views import APIView
from rest_framework.response import Response
from nrega.models import Location, LibtechTag, Report, TaskQueue, Bundle
from nrega.mixins import HttpResponseMixin
from nrega.serializers import (LocationSerializer,
                               ReportSerializer,
                               TaskQueueSerializer,
                               BundleSerializer,
                          LibtechTagSerializer)
from nrega.utils import is_json, tag_locations



class BundleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the portfolio tickers
    associated with the user.
    """
    serializer_class = BundleSerializer
    queryset = Bundle.objects.all()

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

class TagLocationsAPIView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        tag = request.data.get('tag', None)
        locations = request.data.get('locations', None)
        recursive = request.data.get('recursive', True)
        if tag is None:
            raise exceptions.ValidationError("Tag is Required")
        my_tag = LibtechTag.objects.filter(name=tag).first()
        if my_tag is  None:
            raise exceptions.ValidationError("Tag Does not Exist!!")
        tag_locations(locations, my_tag, recursive=recursive)
        status = "Tagged"
        return Response({"status": status})

class ReportAggAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        filter_dict = {}
        libtech_tag__name = request.query_params.get('libtech_tag__name', None)
        report_type = request.query_params.get('report_type', None)
        location_type = request.data.get('location_type', None)
        if libtech_tag__name is not None:
            filter_dict["libtech_tag__name"] = libtech_tag__name
        if report_type is not None:
            filter_dict["report_type"] = report_type
        if location_type is not None:
            filter_dict["location_type"] = location_type
        queryset = Report.objects.filter(**filter_dict).values("report_type").annotate(total=Count('pk'))
        return Response({"results": queryset})
    
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



class ReportAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """API View for the Report Model"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ReportSerializer
    passed_id = None
    input_id = None
    search_fields = ('location__code')
    ordering_fields = ('code', 'id')
    filter_fields = ('report_type', 'location_type', 'libtech_tag__name',
                     'location_code', 'finyear', 'location',)
   # filterset_class = ReportFilter
    queryset = Report.objects.all()
    def get_object(self):
        input_id = self.input_id
        queryset = self.get_queryset()
        obj = None
        if input_id is not None:
            obj = get_object_or_404(queryset, id=input_id)
            #self.check_object_permissions(self.request, obj)
        return obj
    def get(self, request, *args, **kwargs):
        self.input_id = get_id_from_request(request)
        if self.input_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Post method would create a report object"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """put method will update the report object. All fields need to be
        present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """patch method will update the object, with the specified fields. All
        fields need not be present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            input_id = None
            if is_json(request.body):
                input_json_data = json.loads(request.body)
                report_type = input_json_data.get("report_type", None)
                finyear = input_json_data.get("finyear", "NA")
                location_code = input_json_data.get("location__code", None)
                location_scheme = input_json_data.get("location__scheme", None)
                location_id = input_json_data.get("location", None)
                if location_code is not None and location_scheme is not None:
                    objs = Report.objects.filter(report_type=report_type, finyear=finyear,
                                                location__code=location_code,
                                                location__scheme=location_scheme)
                elif location_id is not None:
                    objs = Report.objects.filter(report_type=report_type, finyear=finyear,
                                                 location__id=location_id)
                else:
                    objs = []
                if len(objs) == 1:
                    print("only one object found")
                    input_id = objs.first().id
            if input_id is None:
                data = json.dumps({"message":"Need to specify the ID for this method"})
                return self.render_to_response(data, status="404")
            self.input_id = input_id
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Will delete the retrieved object"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.destroy(request, *args, **kwargs)


class TaskQueueAPIView(HttpResponseMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.ListAPIView):
    """API View for the Report Model"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TaskQueueSerializer
    passed_id = None
    input_id = None
    search_fields = ('location_code')
    filter_fields = ('is_done', 'location_code', 'scheme', 'status',
                     'in_progress', 'task_type')
    ordering_fields = ('location_code', 'id', 'priority', 'updated')
    queryset = TaskQueue.objects.all()
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

    def post(self, request, *args, **kwargs):
        """Post method would create a report object"""
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """put method will update the report object. All fields need to be
        present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """patch method will update the object, with the specified fields. All
        fields need not be present"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Will delete the retrieved object"""
        self.input_id = get_id_from_request(request)
        if self.input_id is None:
            data = json.dumps({"message":"Need to specify the ID for this method"})
            return self.render_to_response(data, status="404")
        return self.destroy(request, *args, **kwargs)


