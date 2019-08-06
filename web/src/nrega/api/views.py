import json
from django.views.generic import View
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins,generics,permissions

from nrega.models import Location,Report,CrawlQueue
from nrega.mixins import HttpResponseMixin
from nrega.crawler.code.commons import getAvailableReports
from accounts.api.permissions import IsOwnerOrReadOnly,IsAdminOwnerOrReadOnly
from .mixins import CSRFExemptMixin
from .utils import is_json
from .serializers import LocationSerializer,ReportSerializer,CrawlQueueSerializer

def getID(request):
  urlID=request.GET.get('id',None)
  inputJsonData={}
  if is_json(request.body):
    inputJsonData=json.loads(request.body)
  inputJsonID=inputJsonData.get("id",None)
  inputID = urlID or inputJsonID or None
  return inputID


class LocationAPIView(HttpResponseMixin,
                           mixins.RetrieveModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsAdminOwnerOrReadOnly]
  serializer_class = LocationSerializer
  passedID=None
  inputID=None
  search_fields= ('name')
  ordering_fields=('name','id')
  filter_fields=('name','code','locationType','parentLocation__code')
  queryset=Location.objects.all()
  def get_object(self):
    inputID=self.inputID
    queryset=self.get_queryset()
    obj=None
    if inputID is not None:
      obj=get_object_or_404(queryset,id=inputID)
      self.check_object_permissions(self.request,obj)
    return obj
  def get(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is not None:
      return self.retrieve(request,*args,**kwargs)
    return super().get(request,*args,**kwargs)

class ReportOrCreateAPIView(HttpResponseMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsAdminOwnerOrReadOnly]
  serializer_class = ReportSerializer
  passedID=None
  inputID=None
  search_fields= ('code')
  ordering_fields=('code','id')
  filter_fields=('reportType','location__code','finyear')
  queryset=Report.objects.all()
  def validate_queryParams(self,request):
    message=""
    query_params=request.query_params
    print("I am in validate Query Parameters")
    print(query_params)
    locationCode=query_params.get("location__code",None)
    reportType=query_params.get("reportType",None)
    finyear=query_params.get("finyear",None)
    if locationCode is None:
      message="Location not specified hence no report has been requested"
      return message
    l=Location.objects.filter(code=locationCode).first()
    if l is None:
       message=f"Could not find any location with {locationCode}. Please use valid locationCode"
       return message
    availableReports=getAvailableReports(l)
    print(availableReports)
    if reportType not in availableReports:
       message=f"{reportType} does not match any standard report. Kindly use one of the following reporttypes {availableReports}"
       return message
    ## Now since the location and Report has been validated lets check. 
    myReport=Report.objects.filter(finyear=finyear,reportType=reportType,location=l).first()
    if myReport is None:
      message=f"The requested report is not avialable and the crawl has been initiatied. You can request for the same report after some time"
      cq=CrawlQueue.objects.filter(reportType=reportType,finyear=finyear,locationCode=l.code,status='inQueue').first()
      if cq is None:
        cq=CrawlQueue.objects.create(reportType=reportType,finyear=finyear,locationCode=l.code)
    else:
      message=f"Download : {myReport.reportURL}"
    return message

  def get(self,request,*args,**kwargs):
    queryset=self.filter_queryset(self.queryset)
    print(queryset)
    if len(queryset) == 0:
      message=self.validate_queryParams(request)
      data={'message':message}
      return JsonResponse(data)
    else:
      self.inputID=getID(request)
      if self.inputID is not None:
        return self.retrieve(request,*args,**kwargs)
      return super().get(request,*args,**kwargs)
  def post(self,request,*args,**kwargs):
    return self.create(request,*args,**kwargs)


class ReportAPIView(HttpResponseMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsAdminOwnerOrReadOnly]
  serializer_class = ReportSerializer
  passedID=None
  inputID=None
  search_fields= ('code')
  ordering_fields=('code','id')
  filter_fields=('reportType','location__code','finyear')
  queryset=Report.objects.all()
  def get_object(self):
    inputID=self.inputID
    queryset=self.get_queryset()
    obj=None
    if inputID is not None:
      obj=get_object_or_404(queryset,id=inputID)
      self.check_object_permissions(self.request,obj)
    return obj
  def get(self,request,*args,**kwargs):
    queryset=self.filter_queryset(self.queryset)
    print(queryset)
    self.inputID=getID(request)
    if self.inputID is not None:
      return self.retrieve(request,*args,**kwargs)
    return super().get(request,*args,**kwargs)
  def post(self,request,*args,**kwargs):
    return self.create(request,*args,**kwargs)

class CrawlQueueAPIView(HttpResponseMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsAdminOwnerOrReadOnly]
  serializer_class = CrawlQueueSerializer
  passedID=None
  inputID=None
  search_fields= ('report__location','report__reportType')
  ordering_fields=('updated','id')
  filter_fields=('report__reportType','report__location__code','report__finyear')
  queryset=CrawlQueue.objects.all()
  def get_object(self):
    inputID=self.inputID
    queryset=self.get_queryset()
    obj=None
    if inputID is not None:
      obj=get_object_or_404(queryset,id=inputID)
      self.check_object_permissions(self.request,obj)
    return obj
  def get(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is not None:
      return self.retrieve(request,*args,**kwargs)
    return super().get(request,*args,**kwargs)
  def post(self,request,*args,**kwargs):
    return self.create(request,*args,**kwargs)

'''
class PanchayatCrawlInfoAPIView(HttpResponseMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsAdminOwnerOrReadOnly]
  serializer_class = PanchayatCrawlInfoSerializer
  passedID=None
  inputID=None
  search_fields= ('code')
  ordering_fields=('code','id')
  filter_fields=('id','code')
  queryset=PanchayatCrawlInfo.objects.all()
  def get_object(self):
    inputID=self.inputID
    queryset=self.get_queryset()
    obj=None
    if inputID is not None:
      obj=get_object_or_404(queryset,id=inputID)
      self.check_object_permissions(self.request,obj)
    return obj
  def get(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is not None:
      return self.retrieve(request,*args,**kwargs)
    return super().get(request,*args,**kwargs)

  def post(self,request,*args,**kwargs):
    return self.create(request,*args,**kwargs)

  def put(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.update(request,*args,**kwargs)

  def delete(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.destroy(request,*args,**kwargs)

'''
