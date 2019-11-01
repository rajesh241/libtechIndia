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
from datetime import datetime, timedelta
taskQueueThreshold = datetime.now() - timedelta(hours=12)
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
  parser.add_argument('-e', '--execute', help='Execute Cron Job', required=False,action='store_const', const=1)
  parser.add_argument('-ti1', '--testInput1', help='Test Input 1', required=False)
  parser.add_argument('-ti2', '--testInput2', help='Test Input 2', required=False)
  args = vars(parser.parse_args())
  return args


def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  if args['execute']:
    objs=TaskQueue.objects.filter(status="inProgress",updated__lte=taskQueueThreshold)
   # objs=TaskQueue.objects.filter(status="inProgress")
    for obj in objs:
      logger.info(obj.id)
      obj.status="inQueue"
      obj.priority=100
      obj.save()
  logger.info("...END PROCESSING") 
  exit(0)

if __name__ == '__main__':
  main()
