from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save,post_save

# Create your models here.
 
class Location(models.Model):
  name=models.CharField(max_length=256)
  nicURL=models.URLField(max_length=2048,blank=True,null=True)
  displayName=models.CharField(max_length=2048)
  locationType=models.CharField(max_length=64)
  nameInLocalLanguage=models.BooleanField(default=False)
  englishName=models.CharField(max_length=256,null=True,blank=True)
  code=models.CharField(max_length=20,unique=True,db_index=True)
  parentLocation=models.ForeignKey('self',on_delete=models.SET_NULL,blank=True,null=True)
  slug=models.SlugField(blank=True) 
  crawlIP=models.CharField(max_length=256,null=True,blank=True)
  stateShortCode=models.CharField(max_length=2,null=True,blank=True)
  stateCode=models.CharField(max_length=2,null=True,blank=True)
  stateName=models.CharField(max_length=256,null=True,blank=True)
  districtCode=models.CharField(max_length=4,null=True,blank=True)
  districtName=models.CharField(max_length=256,null=True,blank=True)
  blockCode=models.CharField(max_length=7,null=True,blank=True)
  blockName=models.CharField(max_length=256,null=True,blank=True)
  panchayatCode=models.CharField(max_length=10,null=True,blank=True)
  panchayatName=models.CharField(max_length=256,null=True,blank=True)
  filepath=models.CharField(max_length=2048,null=True,blank=True)
  isNIC=models.BooleanField(default=True)
  remarks=models.TextField(blank=True,null=True)
  priority=models.PositiveSmallIntegerField(default=0)
  class Meta:
    db_table = 'location'
  def __str__(self):
    return self.code

class Report(models.Model):
  location=models.ForeignKey('Location',on_delete=models.CASCADE)
  reportType=models.CharField(max_length=256)
  reportURL=models.URLField(max_length=2048,blank=True,null=True)
  excelURL=models.URLField(max_length=2048,blank=True,null=True)
  code=models.CharField(max_length=256,db_index=True,blank=True,null=True)
  finyear=models.CharField(max_length=2,blank=True)
  created=models.DateTimeField(auto_now_add=True)
  updated=models.DateTimeField(auto_now=True)
  class Meta:
    unique_together = ('location','reportType','finyear')  
    db_table = 'report'
  def __str__(self):
    return self.location.code+"_"+self.location.name+"-"+self.reportType

class TaskQueue(models.Model):
  report=models.ForeignKey('Report',on_delete=models.CASCADE,null=True,blank=True)
  reportType=models.CharField(max_length=256)
  locationCode=models.CharField(max_length=20)
  finyear=models.CharField(max_length=2,null=True)
  status=models.CharField(max_length=256,default='inQueue')
  isError=models.BooleanField(default=False)
  isDone=models.BooleanField(default=False)
  response=models.CharField(max_length=256,null=True,blank=True)
  created=models.DateTimeField(auto_now_add=True)
  updated=models.DateTimeField(auto_now=True)
  class Meta:
    db_table = 'taskQueue'
  def __str__(self):
    return self.locationCode+"_"+self.reportType

class Test(models.Model):
  name=models.CharField(max_length=256)
  address=models.CharField(max_length=256)
  isAdult=models.BooleanField(default=False)
  class Meta:
    db_table = 'test'
  def __str__(self):
    return self.name

class NREGANICError(models.Model):
  errorType=models.CharField(max_length=256)
  code=models.CharField(max_length=256)
  remarks=models.TextField(blank=True,null=True)
  created=models.DateTimeField(auto_now_add=True)
  updated=models.DateTimeField(auto_now=True)
  class Meta:
    db_table = 'nregaNICError'
  def __str__(self):
    return self.errorType
 
def createslug(instance):
  try:
    myslug=slugify(instance.name)[:50]
  except:
    myslug=slugify(instance.code)[:50]
  if myslug == '':
    if hasattr(instance, 'code'):
      myslug="%s-%s" % (instance.__class__.__name__ , str(instance.code))
    else:
      myslug="%s-%s" % (instance.__class__.__name__ , str(instance.id))
  return myslug


def location_post_save_receiver(sender,instance,*args,**kwargs):
  myslug=createslug(instance)
  if instance.slug != myslug:
    instance.slug = myslug
    instance.save()
post_save.connect(location_post_save_receiver,sender=Location)
