"""This module is for crawling all nrega locations"""
import os
import pandas as pd
import argparse
import urllib.parse as urlparse
from urllib.parse import urljoin
import requests
import django
import time
from django.utils.text import slugify
from commons import logger_fetch, is_english
from defines import DJANGO_SETTINGS
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS)
django.setup()
from nrega.models import Location, Report, LibtechTag, Bundle
from nrega.serializers import report_post_save_operation
from nrega.bundle import create_bundle
from core.utils import send_slack_message
def args_fetch():
    '''
    Paser for the argument list that returns the args list
    '''

    parser = argparse.ArgumentParser(description=('This script will crawl',
                                                  'nrega locations from nic'))
    parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
    parser.add_argument('-cb', '--createBundle', help='createBundle',
                        required=False, action='store_const', const=1)
    parser.add_argument('-t', '--test', help='test',
                        required=False, action='store_const', const=1)
    parser.add_argument('-f', '--fixfilepath', help='fix broken file paths',
                        required=False, action='store_const', const=1)
    parser.add_argument('-lt', '--location_type', help='location type', required=False)
    parser.add_argument('-slt', '--setLocationTag', help='set Location Tags',
                        required=False, action='store_const', const=1)
    parser.add_argument('-tid', '--tagID', help='location tag id', required=False)
    parser.add_argument('-fn', '--fileName', help='File Name', required=False)
    parser.add_argument('-e', '--export', help='export',
                        required=False, action='store_const', const=1)
    parser.add_argument('-ir', '--importReports', help='export',
                        required=False, action='store_const', const=1)
    parser.add_argument('-i', '--import', help='export',
                        required=False, action='store_const', const=1)
    args = vars(parser.parse_args())
    return args


def main():
    """Main Module of this program"""
    args = args_fetch()
    logger = logger_fetch(args.get('log_level'))
    if args['test']:
        send_slack_message("Testing from scripts")
        exit(0)
        logger.info("Testing test script")
        objs = Bundle.objects.all()
        for obj in objs:
            obj.is_bundle_created = True
            obj.save()
    if args["createBundle"]:
        message = ''
        instance = Bundle.objects.filter(is_bundle_created=False,
                                         is_error=False).first()
        if instance is None:
            logger.info("no bundle to be created!")
        if instance is not None:
          report_type_array = instance.report_types.split(",")
          qs = Report.objects.filter(report_type__in=report_type_array)
          if instance.libtech_tags is not None:
              libtech_tag_array = instance.libtech_tags.split(",")
              libtech_tag_object_array = []
              for tag in libtech_tag_array:
                  obj = LibtechTag.objects.filter(name = tag).first()
                  if obj is not None:
                      libtech_tag_object_array.append(obj)
              qs = qs.filter(libtech_tag__in=libtech_tag_object_array)
          if instance.location_type is not None:
              qs = qs.filter(location_type = instance.location_type)
          if instance.location_code is not None:
              qs = qs.filter(location_code = instance.location_code)
          try:
              bundle_url = create_bundle(instance, qs)
              logger.info(f"Bundle created wtih url {bundle_url}")
              is_error = False
              message = f"Created Bundle for bundle id {instance.id} for sample {libtech_tag_array} for report types {instance.report_types} has been created and the it can be downloaded at {bundle_url}"
          except:
              bundle_url = ""
              is_error = True
              message = f"Created Bundle for bundle id {instance.id} for {libtech_tag_array} for report types {instance.report_types} has failed for unknown reasons"
          send_slack_message(message)
          if(is_error == True):
              instance.is_error = True
              instance.save()
          else:
              instance.bundle_url = bundle_url
              instance.is_bundle_created = True
              instance.save()
          

if __name__ == '__main__':
    main()
