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
from commons import loggerFetch
import django
from django.core.wsgi import get_wsgi_application
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import F,Q,Sum,Count
os.environ.setdefault("DJANGO_SETTINGS_MODULE", djangoSettings)
django.setup()

from nrega.models import Location
scheme='pds'
def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='These scripts will initialize the Database for the district and populate relevant details')
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-i', '--import', help='import Json Data', required=False,action='store_const', const=1)
  parser.add_argument('-e', '--export', help='import Json Data', required=False,action='store_const', const=1)
  parser.add_argument('-t', '--test', help='Test Loop', required=False,action='store_const', const=1)
  parser.add_argument('-c', '--crawl', help='crawl Locations ', required=False,action='store_const', const=1)
  parser.add_argument('-lt', '--locationType', help='Location Type to be crawled can take values of state,district,block,panchayat', required=False)
  parser.add_argument('-sc', '--stateCode', help='restricts the crawling to the specified stateCode', required=False)
  args = vars(parser.parse_args())
  return args


  logger.info("...END PROCESSING") 
  exit(0)


def crawlPDSDistrictBlocks(logger,locationType):
  if locationType == 'district':
    url="https://aahar.jharkhand.gov.in/secc_cardholders/searchRationResults"
    r=requests.get(url)
    if r.status_code == 200:
      myhtml=r.content
      mysoup=BeautifulSoup(myhtml,"lxml")
      districtSelect=mysoup.find("select",id="SeccCardholderRgiDistrictCode")
      options=districtSelect.findAll('option')
      stateLocation=Location.objects.filter(code='34',scheme=scheme).first()
      for option in options:
        districtName=option.text
        districtCode=option['value']
        if option['value'] != "":
          code=option['value']
          name=option.text
          logger.info("District Name %s Code %s " % (option.text,option['value']))
          myLocation=Location.objects.filter(code=code,scheme=scheme).first()
          if myLocation is None:
            myLocation=Location.objects.create(code=code,scheme=scheme)
          myLocation.locationType='pdsDistrict'
          myLocation.parentLocation=stateLocation
          myLocation.stateCode='34'
          myLocation.stateName='JHARKHAND'
          myLocation.name=name
          myLocation.englishName=name
          myLocation.districtCode=code
          myLocation.districtName=name
          myLocation.displayName="Jharkhand-%s" % (name)
          myLocation.save()
  #Now for Crawling Blocks
  if locationType == 'village':
    objs=Location.objects.filter(locationType='pdsBlock',scheme=scheme)
    for obj in objs:
      url="https://aahar.jharkhand.gov.in/secc_cardholders/searchRationResults"
      r=requests.get(url)
      if r.status_code == 200:
        cookies=r.cookies
        headers = {
         'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'en-GB,en;q=0.5',
         'Connection': 'keep-alive',
         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
         'Host': 'aahar.jharkhand.gov.in',
         'Referer': 'https://aahar.jharkhand.gov.in/secc_cardholders/searchRation',
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:45.0) Gecko/20100101 Firefox/45.0',
         'X-Prototype-Version': '1.6.1_rc2',
         'X-Requested-With': 'XMLHttpRequest',
         'X-Update': 'SeccCardholderRgiBlockCode',
       }

        data = {
         'data[SeccCardholder][rgi_district_code]': obj.districtCode
        }

        r = requests.post('https://aahar.jharkhand.gov.in/secc_cardholders/getRgiBlock', headers=headers, cookies=cookies, data=data)
        data = {
          'data[SeccCardholder][rgi_block_code]': obj.blockCode
        }
        headers['X-Update']='SeccCardholderRgiVillageCode'
        response = requests.post('https://aahar.jharkhand.gov.in/secc_cardholders/getRgiVillages', headers=headers, cookies=cookies, data=data)
        myhtml=response.content
        mysoup=BeautifulSoup(myhtml,"lxml")
        options=mysoup.findAll('option')
        for option in options:
          if option['value'] != "":
            code=option['value']
            name=option.text
            logger.info(f"{name}-{code}")
            myLocation=Location.objects.filter(code=code,scheme=scheme).first()
            if myLocation is None:
              myLocation=Location.objects.create(code=code,scheme=scheme)
            myLocation.locationType='pdsVillage'
            myLocation.parentLocation=obj
            myLocation.stateCode=obj.stateCode
            myLocation.stateName=obj.stateName
            myLocation.districtCode=obj.districtCode
            myLocation.districtName=obj.districtName
            myLocation.blockCode=obj.blockCode
            myLocation.blockName=obj.blockName
            myLocation.name=name
            myLocation.englishName=name
            myLocation.displayName="Jharkhand-%s-%s-%s" % (obj.parentLocation.name,obj.name,name)
            myLocation.save()

       #headers['X-Update']='SeccCardholderDealerId'
       #response = requests.post('https://aahar.jharkhand.gov.in/secc_cardholders/getRgiDealer', headers=headers, cookies=cookies, data=data)
       #myhtml=response.content
       #mysoup=BeautifulSoup(myhtml,"lxml")
       #options=mysoup.findAll('option')
       #for option in options:
       #  if option['value'] != "":
       #    code=option['value']
       #    name=option.text
       #    logger.info(f"{name}-{code}")
       #    myLocation=Location.objects.filter(code=code,scheme=scheme).first()
       #    if myLocation is None:
       #      myLocation=Location.objects.create(code=code,scheme=scheme)
       #    myLocation.locationType='pdsDealer'
       #    myLocation.parentLocation=obj
       #    myLocation.stateCode=obj.stateCode
       #    myLocation.stateName=obj.stateName
       #    myLocation.districtCode=obj.districtCode
       #    myLocation.districtName=obj.districtName
       #    myLocation.blockCode=obj.blockCode
       #    myLocation.blockName=obj.blockName
       #    myLocation.name=name
       #    myLocation.englishName=name
       #    myLocation.displayName="Jharkhand-%s-%s-%s" % (obj.parentLocation.name,obj.name,name)
       #    myLocation.save()

            

      
  if locationType == 'block':
    myDistricts=Location.objects.filter(locationType='pdsDistrict',scheme=scheme)
    for obj in myDistricts:
      url="https://aahar.jharkhand.gov.in/secc_cardholders/searchRationResults"
      r=requests.get(url)
      if r.status_code == 200:
        cookies=r.cookies
        headers = {
         'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
         'Accept-Encoding': 'gzip, deflate, br',
         'Accept-Language': 'en-GB,en;q=0.5',
         'Connection': 'keep-alive',
         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
         'Host': 'aahar.jharkhand.gov.in',
         'Referer': 'https://aahar.jharkhand.gov.in/secc_cardholders/searchRation',
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:45.0) Gecko/20100101 Firefox/45.0',
         'X-Prototype-Version': '1.6.1_rc2',
         'X-Requested-With': 'XMLHttpRequest',
         'X-Update': 'SeccCardholderRgiBlockCode',
       }

        data = {
         'data[SeccCardholder][rgi_district_code]': obj.districtCode
        }

        response = requests.post('https://aahar.jharkhand.gov.in/secc_cardholders/getRgiBlock', headers=headers, cookies=cookies, data=data)
        myhtml=response.content
        mysoup=BeautifulSoup(myhtml,"lxml")
        blockSelect=mysoup.find("select",id="SeccCardholderRgiBlockCode")
        options=mysoup.findAll('option')
        for option in options:
          if option['value'] != "":
            code=option['value']
            name=option.text
            logger.info(f"{name}-{code}")
            myLocation=Location.objects.filter(code=code,scheme=scheme).first()
            if myLocation is None:
              myLocation=Location.objects.create(code=code,scheme=scheme)
            myLocation.locationType='pdsBlock'
            myLocation.parentLocation=obj
            myLocation.stateCode=obj.stateCode
            myLocation.stateName=obj.stateName
            myLocation.districtCode=obj.districtCode
            myLocation.districtName=obj.districtName
            myLocation.name=name
            myLocation.englishName=name
            myLocation.blockCode=code
            myLocation.blockName=name
            myLocation.displayName="Jharkhand-%s-%s" % (obj.name,name)
            myLocation.save()
 
def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  if args['crawl']:
    logger.info("Crawling PDS Locations")
    locationType=args['locationType']
    crawlPDSDistrictBlocks(logger,locationType)

if __name__ == '__main__':
  main()
