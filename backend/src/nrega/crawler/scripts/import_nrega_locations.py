"""This module is for crawling all nrega locations"""
import os
import pandas as pd
import argparse
import urllib.parse as urlparse
from urllib.parse import urljoin
import requests
import django
from django.utils.text import slugify
from commons import logger_fetch, is_english
from defines import DJANGO_SETTINGS, STATE_SHORT_CODE_DICT
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS)
django.setup()
from nrega.models import Location, Report
from nrega.serializers import report_post_save_operation

def args_fetch():
    '''
    Paser for the argument list that returns the args list
    '''

    parser = argparse.ArgumentParser(description=('This script will crawl',
                                                  'nrega locations from nic'))
    parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
    parser.add_argument('-c', '--crawl', help='crawl',
                        required=False, action='store_const', const=1)
    parser.add_argument('-f', '--fixfilepath', help='fix broken file paths',
                        required=False, action='store_const', const=1)
    parser.add_argument('-lt', '--location_type', help='location type', required=False)
    parser.add_argument('-e', '--export', help='export',
                        required=False, action='store_const', const=1)
    parser.add_argument('-ir', '--importReports', help='export',
                        required=False, action='store_const', const=1)
    parser.add_argument('-i', '--import', help='export',
                        required=False, action='store_const', const=1)
    args = vars(parser.parse_args())
    return args

report_urls = [
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/02/andhra-pradesh_02_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/03/arunachal-pradesh_03_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/04/assam_04_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/33/chhattisgarh_33_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/05/bihar_05_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/13/himachal-pradesh_13_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/12/haryana_12_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/11/gujarat_11_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/16/kerala_16_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/14/jammu-and-kashmir_14_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/15/karnataka_15_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/34/jharkhand_34_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/20/manipur_20_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/21/meghalaya_21_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/17/madhya-pradesh_17_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/22/mizoram_22_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/18/maharashtra_18_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/23/nagaland_23_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/28/sikkim_28_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/26/punjab_26_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/24/odisha_24_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/30/tripura_30_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/29/tamil-nadu_29_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/27/rajasthan_27_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/35/uttranchal_35_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/01/andaman-and-nicobar_01_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/07/dadra_07_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/32/west-bengal_32_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/08/daman_08_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/10/goa_10_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/19/lakshadweep_19_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/25/pondicherry_25_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/06/chandigarh_06_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/31/uttar-pradesh_31_nrega_locations_22082020.csv",
    "https://libtech-india-data.s3.ap-south-1.amazonaws.com/data/samples/on_demand/nrega/nrega_locations/36/telangana_36_nrega_locations_22082020.csv"
]
def get_display_name(my_location):
    display_name = my_location.state_name
    if my_location.district_name != '':
        display_name = f"{display_name}-{my_location.district_name}"
    if my_location.block_name != '':
        display_name = f"{display_name}-{my_location.block_name}"
    if my_location.panchayat_name != '':
        display_name = f"{display_name}-{my_location.panchayat_name}"
    return display_name
def main():
    """Main Module of this program"""
    args = args_fetch()
    logger = logger_fetch(args.get('log_level'))
    if args['import']:
        logger.info("Processing import")
        #url = "https://backend.libtech.in/api/public/report?report_type=nrega_locations"
        #res = requests.get(url)
        #data = res.json()
        #logger.info(data)
        #results = data.get("results")
        #for obj in results:
        #    print(obj.get('report_url'))
        for url in report_urls:
            logger.info(f"url is {url}")
            dataframe = pd.read_csv(url,  dtype=str)
            dataframe = dataframe.fillna("")
            total = len(dataframe)
            for index, row in dataframe.iterrows():
                logger.info(f"current processing {total}")
                total = total - 1
                name = row.pop('name')
                code = row.pop('code')
                location_type = row.pop('location_type')
                parent_location_code = row.pop('parent_location_code')
                parent_location = Location.objects.filter(code=parent_location_code).first()
                if parent_location is None:
                    logger.info("ERROR ERROR!")
                    logger.info(row)
                    logger.info(f"count not find parent_location {parent_location_code}")
                    exit(0)
                my_location = Location.objects.filter(code=code).first()
                if my_location is None:
                    my_location = Location.objects.create(code=code, name=name,
                                                          location_type=location_type)
                my_location.name = name
                my_location.location_type = location_type
                my_location.parent_location = parent_location
                
                for key, value in row.items():
                    setattr(my_location, key, value)
                my_location.display_name = get_display_name(my_location)
                my_location.save()
#                setattr(my_location, name_param.lower(), name)

    logger.info("...END PROCESSING")
    if args['importReports']:
        logger.info(f"Importing reports")
        filename = "/tmp/reports.csv"
        dataframe = pd.read_csv(filename,  dtype=str)
        dataframe = dataframe.fillna("")
        total = len(dataframe)
        for index, row in dataframe.iterrows():
            logger.info(f"current processign {total}")
            total = total - 1
            location_code = row.get("code")
            my_location = Location.objects.filter(code=location_code).first()
            if my_location is None:
                logger.info(f"Location not found {row}")
                continue
            finyear = row.get("finyear")
            if finyear == "":
                finyear = "NA"
            report_type = row.get("report_type")
            my_report = Report.objects.filter(finyear=finyear,
                                              location=my_location,
                                              report_type=report_type).first()
            if my_report is None:
                my_report = Report.objects.create(finyear=finyear, location=my_location,
                                      report_type=report_type)
            my_report.report_url = row.get("report_url")
            my_report.excel_url = row.get("excel_url")
            my_report.save()
            report_post_save_operation(my_report)

if __name__ == '__main__':
    main()
