import os
import sys
import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import pandas as pd
fileDir = os.path.dirname(os.path.realpath(__file__))
rootDir=fileDir+"/../../../"
sys.path.insert(0, rootDir)
from config.defines import djangoSettings
print(djangoSettings)
from commons import loggerFetch
import django
from django.core.wsgi import get_wsgi_application
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import F,Q,Sum,Count
os.environ.setdefault("DJANGO_SETTINGS_MODULE", djangoSettings)
django.setup()

from nrega.models import Location,Report,TaskQueue

def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='These scripts will initialize the Database for the district and populate relevant details')
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-t', '--test', help='Test Loop', required=False,action='store_const', const=1)
  parser.add_argument('-ti1', '--testInput1', help='Test Input 1', required=False)
  parser.add_argument('-ti2', '--testInput2', help='Test Input 2', required=False)
  args = vars(parser.parse_args())
  return args


def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  if args['test']:
    state_codes = []
    column_headers = ["code", "report_type", "finyear", "report_url"]
    states = Location.objects.filter(locationType='state')
    for state in states:
      state_codes.append(state.code)
 #   state_codes = ["34"]
    for state_code in state_codes:
      csv_array = []
      report_types = ["NICRejectedTransactionsCoBankURL",
                      "NICRejectedTransactionsPostURL",
                      "NICRejectedTransactionsURL"]
      for report_type in report_types:
        objs = Report.objects.filter(reportType=report_type,
                                     location__stateCode = state_code)
        for obj in objs:
          logger.info(obj.location.code)
          a = [obj.location.code, report_type, obj.finyear, obj.reportURL]
          csv_array.append(a)
      df = pd.DataFrame(csv_array, columns=column_headers)
      df.to_csv(f"dump/{state_code}.csv")
    exit(0)
    objs=TaskQueue.objects.all().order_by("-id")
    for obj in objs:
      logger.info(obj.id)
      obj.delete()
    exit()
    objs=Report.objects.filter(finyear='')
    j=len(objs)
    logger.info(f"number of objects {j}")
    for obj in objs:
      logger.info(f"{j}   {obj.id}")
      j=j-1
      obj.finyear='NA'
      obj.save()
    exit(0)
    obj.finyear=None
    obj.save()
    exit(0)
    ltArray=[1]
    objs=Location.objects.filter(libtechTag__in=ltArray)
    s=''
    for obj in objs:
      logger.info(obj.code)
      s+=f"'{obj.code}',"
    logger.info(s)
    exit(0)
    objs=TaskQueue.objects.filter(status="inQueue")
    for obj in objs:
      obj.status="inQueue"
      obj.priority=100
      obj.save()
    exit(0)
    logger.info("executing test loop")
    objs=Location.objects.all().order_by("-id")
    for obj in objs:
      logger.info(obj.id)
      obj.save()
    exit(0)
    reportType=args['testInput1']
    code=args['testInput2']
    l=Location.objects.filter(code=code).first()
    myReport=Report.objects.create(reportType=reportType,location=l,finyear="")
  logger.info("...END PROCESSING") 
  exit(0)

if __name__ == '__main__':
  main()
