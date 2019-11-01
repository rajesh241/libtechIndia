from django.http import HttpResponse
import time
import datetime
import os
from django.http import HttpResponseRedirect
from django.conf import settings
#from mysite.settings import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET, REGION_NAME
import boto3
from boto3.session import Session
from botocore.client import Config
from pathlib import Path
import json
from config.defines import LIBTECH_AWS_ACCESS_KEY_ID,LIBTECH_AWS_SECRET_ACCESS_KEY,LIBTECH_AWS_BUCKET_NAME,AWS_S3_REGION_NAME
AWS_DATA_BUCKET="libtech-india-data"
AWS_DATA_BUCKET_BASEURL="https://libtech-india-data.s3.ap-south-1.amazonaws.com/"


def download_reports_zip(modeladmin, request, queryset):
    curTimeStamp=str(int(time.time()))
    dateString=datetime.date.today().strftime("%B_%d_%Y_%I_%M")
    baseDir="/tmp/genericReports/%s_%s" % (dateString,curTimeStamp)
    s='' 
    for obj in queryset:
      if obj.location:
        filepath="%s/%s" % (baseDir,obj.location.slug)
      else:
        filepath=baseDir
      if hasattr(obj, 'finyear'):
        filename="%s_%s.csv" % (obj,obj.finyear)
      else:
        filename="%s.csv" % (obj)
      #cmd="mkdir -p %s && cd %s && wget -O %s %s " %(filepath,filepath,filename,obj.reportFile.url) 
      cmd="mkdir -p %s && cd %s && wget  %s " %(filepath,filepath,obj.excelURL) 
      os.system(cmd)
      s+="\n"
    cmd="cd %s && zip -r %s.zip *" % (baseDir,baseDir)
    os.system(cmd)
    in_file = open("%s.zip" % baseDir, "rb") # opening for [r]eading as [b]inary
    zipdata = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()


    cloudFilename="temp/%s_%s.zip" % (dateString,curTimeStamp)
   # boto3.setup_default_session(profile_name=AWS_PROFILE_NAME)

    boto3.setup_default_session(
      aws_access_key_id=LIBTECH_AWS_ACCESS_KEY_ID,
      aws_secret_access_key=LIBTECH_AWS_SECRET_ACCESS_KEY,
      region_name=AWS_S3_REGION_NAME
  )
    s3 = boto3.resource('s3', region_name='ap-south-1')
    s3.Bucket(AWS_DATA_BUCKET).put_object(ACL='public-read',Key=cloudFilename, Body=zipdata)
    publicURL="%s%s" % (AWS_DATA_BUCKET_BASEURL,cloudFilename)
#    with open("/tmp/test.csv","w") as f:
#      f.write(s)
    return HttpResponseRedirect(publicURL)
    
download_reports_zip.short_description = "Download Selected Reports as Zip"

