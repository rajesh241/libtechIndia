import json
import datetime
from django.views.generic import View
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins,generics,permissions
from django.db.models import Q
from nrega.models import Location,Report,TaskQueue,Test,NREGANICError,LibtechDataStatus
from nrega.mixins import HttpResponseMixin
from nrega.crawler.code.commons import getAvailableReports
from accounts.api.permissions import IsOwnerOrReadOnly,IsAdminOwnerOrReadOnly
from .mixins import CSRFExemptMixin
from .utils import is_json
from .serializers import LocationSerializer,ReportSerializer,TaskQueueSerializer,TestSerializer,NREGANICErrorSerializer,LibtechDataStatusSerializer

def getCurrentFinYear():
  now = datetime.datetime.now()
  month=now.month
  if now.month > 3:
    year=now.year+1
  else:
    year=now.year
  return year% 100

def getDefaultStartFinYear():
  endFinYear=getCurrentFinYear()
  startFinYear = str ( int(endFinYear) -1 )
  return startFinYear

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
  filter_fields=('name','code','locationType','parentLocation__code','stateCode','districtCode','blockCode')
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

def get_serialized(queryset):
#    queryset = Report.objects.filter(id__lte=100)
    serializer = ReportSerializer(queryset, many=True)
    data = serializer.data
    return data
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
    data=None
    query_params=request.query_params
    locationCode=query_params.get("location__code",None)
    reportType=query_params.get("reportType",None)
    startFinYear=query_params.get("startFinYear",None)
    priority=query_params.get("priority",100)
    endFinYear=query_params.get("endFinYear",None)
    if locationCode is None:
      message="Location not specified hence no report has been requested"
      return message,data
    l=Location.objects.filter(code=locationCode).first()
    if l is None:
       message=f"Could not find any location with {locationCode}. Please use valid locationCode"
       return message,data
    availableReports=getAvailableReports(l)
    if reportType not in availableReports:
       message=f"{reportType} does not match any standard report. Kindly use one of the following reporttypes {availableReports}"
       return message,data
    ## Now since the location and Report has been validated lets check. 
    if(request.user.is_anonymous):
      message=f"The requested report is not avialable and the crawl cannot be initiated as system is unable to authenticate you. \n Kindly pass the authentication token in the headers of the request"
      return message,data

    cq=TaskQueue.objects.filter(reportType=reportType,startFinYear=startFinYear,endFinYear=endFinYear,locationCode=l.code,status='inQueue').first()
    if cq is None:
      cq=TaskQueue.objects.create(reportType=reportType,locationCode=l.code,startFinYear=startFinYear,endFinYear=endFinYear)
    cq.priority=priority
    cq.save()
    message=f"The crawl has been initiatiated with Task ID {cq.id}"
#   myReport=None 
#   if myReport is None:
#     else: 
#       message=f"The requested report is not avialable and the crawl has been initiatied. You can request for the same report after some time"
#   else:
#     message=f"Download : {myReport.reportURL}"
#   print("I am here once again")
    if startFinYear is None:
      startFinYear=getDefaultStartFinYear()
    if endFinYear is None:
      endFinYear=getCurrentFinYear()
    queryset=Report.objects.filter(reportType=reportType,location=l).filter(  Q(Q (finyear__gte=startFinYear) & Q (finyear__lte=endFinYear)) | Q(finyear = ''))
    data=get_serialized(queryset)
    return message,data

  def get(self,request,*args,**kwargs):
    queryset=self.filter_queryset(self.queryset)
    print(queryset)
    if len(queryset) >= 0:
      message,data1=self.validate_queryParams(request)
      if data1 is None:
        data={"message":message}
      else:
        data={"message":message,"data":data1}
      return JsonResponse(data)
    else:
      self.inputID=getID(request)
      if self.inputID is not None:
        return self.retrieve(request,*args,**kwargs)
      return super().get(request,*args,**kwargs)
  def post(self,request,*args,**kwargs):
    return self.create(request,*args,**kwargs)

class LibtechDataStatusAPIView(HttpResponseMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly]
  serializer_class = LibtechDataStatusSerializer
  passedID=None
  inputID=None
  search_fields= ('location__code','finyear')
  ordering_fields=('location__code','id')
  filter_fields=('location__stateCode','location__code','finyear','location__locationType')
  queryset=LibtechDataStatus.objects.all()
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

  def patch(self,request,*args,**kwargs):
    self.inputID=getID(request)
    print(request.POST)
    if self.inputID is None:
      inputID=None
      if is_json(request.body):
        inputJsonData=json.loads(request.body)
        reportType=inputJsonData.get("reportType",None)
        finyear=inputJsonData.get("finyear","")
        locationCode=inputJsonData.get("location__code",None)
        objs=Report.objects.filter(reportType=reportType,finyear=finyear,location__code=locationCode)
        if len(objs) == 1:
          print("only one object found")
          inputID=objs.first().id
      if inputID is None:
        data=json.dumps({"message":"Need to specify the ID for this method"})
        return self.render_to_response(data,status="404")
      self.inputID=inputID
    return self.partial_update(request,*args,**kwargs)

  def delete(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.destroy(request,*args,**kwargs)



class ReportAPIView(HttpResponseMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly]
  serializer_class = ReportSerializer
  passedID=None
  inputID=None
  search_fields= ('code')
  ordering_fields=('code','id')
  filter_fields=('reportType','location__stateCode','location__code','finyear','location__locationType')
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

  def patch(self,request,*args,**kwargs):
    self.inputID=getID(request)
    print(request.POST)
    if self.inputID is None:
      inputID=None
      if is_json(request.body):
        inputJsonData=json.loads(request.body)
        reportType=inputJsonData.get("reportType",None)
        finyear=inputJsonData.get("finyear","")
        locationCode=inputJsonData.get("location__code",None)
        objs=Report.objects.filter(reportType=reportType,finyear=finyear,location__code=locationCode)
        if len(objs) == 1:
          print("only one object found")
          inputID=objs.first().id
      if inputID is None:
        data=json.dumps({"message":"Need to specify the ID for this method"})
        return self.render_to_response(data,status="404")
      self.inputID=inputID
    return self.partial_update(request,*args,**kwargs)

  def delete(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.destroy(request,*args,**kwargs)


class ReportAPIView1(HttpResponseMixin,
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


class TaskQueueAPIView1(HttpResponseMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly]
  serializer_class = TaskQueueSerializer
  passedID=None
  inputID=None
  search_fields= ('report__location','report__reportType')
  ordering_fields=('updated','id')
  filter_fields=('report__reportType','report__location__code','report__finyear')
  queryset=TaskQueue.objects.all()
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

class TaskQueueGetTask(HttpResponseMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticated]
  serializer_class = TaskQueueSerializer
  passedID=None
  inputID=None
  search_fields= ('report__location','report__reportType')
  ordering_fields=('updated','id')
  filter_fields=('report__reportType','report__location__code','report__finyear')
  queryset=TaskQueue.objects.all()
  def get_object(self):
    obj=TaskQueue.objects.filter(status='inQueue').first()
    obj=TaskQueue.objects.all().first()
    if obj is not None:
      obj.status='inProgress'
      obj.save()
    return obj
  def get(self,request,*args,**kwargs):
    return self.retrieve(request,*args,**kwargs)
class TaskQueueAPIView(HttpResponseMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly]
  serializer_class = TaskQueueSerializer
  passedID=None
  inputID=None
  search_fields= ('reportType','locationCode')
  ordering_fields=('reportType','id','updated','priority')
  filter_fields=('id','reportType','locationCode','finyear','status','isDone')
  queryset=TaskQueue.objects.all()
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

  def patch(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.partial_update(request,*args,**kwargs)

  def delete(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.destroy(request,*args,**kwargs)

class NREGANICErrorAPIView(HttpResponseMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly]
  serializer_class = NREGANICErrorSerializer
  passedID=None
  inputID=None
  search_fields= ('errorType','code')
  ordering_fields=('id')
  filter_fields=('errorType','code')
  queryset=Test.objects.all()
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

  def patch(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.partial_update(request,*args,**kwargs)

  def delete(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.destroy(request,*args,**kwargs)


class TestAPIView(HttpResponseMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           generics.ListAPIView):
  permission_classes=[permissions.IsAuthenticatedOrReadOnly]
  serializer_class = TestSerializer
  passedID=None
  inputID=None
  search_fields= ('name')
  ordering_fields=('name','id')
  filter_fields=('id','name')
  queryset=Test.objects.all()
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

  def patch(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.partial_update(request,*args,**kwargs)

  def delete(self,request,*args,**kwargs):
    self.inputID=getID(request)
    if self.inputID is None:
      data=json.dumps({"message":"Need to specify the ID for this method"})
      return self.render_to_response(data,status="404")
    return self.destroy(request,*args,**kwargs)


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

  def patch(self,request,*args,**kwargs):
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
