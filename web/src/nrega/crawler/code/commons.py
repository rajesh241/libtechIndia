import os
import sys
import logging
fileDir = os.path.dirname(os.path.realpath(__file__))
rootDir=fileDir+"/../../../"
sys.path.insert(0, rootDir)
from logging.handlers import RotatingFileHandler
from nrega.crawler.code.defines import reportTypeDict

def loggerFetch(level=None,filename=None):
  defaultLogLevel="debug"
  logFormat = '%(asctime)s:[%(name)s|%(module)s|%(funcName)s|%(lineno)s|%(levelname)s]: %(message)s' #  %(asctime)s %(module)s:%(lineno)s %(funcName)s %(message)s"
  if filename is not None:
    logger = logging.getLogger(filename)
  else:
    logger = logging.getLogger(__name__)

  if not level:
    level = defaultLogLevel
  
  if level:
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
      raise ValueError('Invalid log level: %s' % level)
    else:
      logger.setLevel(numeric_level)
  ch = logging.StreamHandler()
  formatter = logging.Formatter(logFormat)
  ch.setFormatter(formatter)
  logger.addHandler(ch)

  if filename is not None:
    filename1="%s/%s/%s" % (crawlerLogDir,"info",filename)
    fh = RotatingFileHandler(filename1, maxBytes=5000000, encoding="utf-8",backupCount=10)
    fh.setFormatter(formatter)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)
  if filename is not None:
    filename1="%s/%s/%s" % (crawlerLogDir,"debug",filename)
    fhd = RotatingFileHandler(filename1, maxBytes=5000000, encoding="utf-8",backupCount=10)
    fhd.setFormatter(formatter)
    fhd.setLevel(logging.DEBUG)
    logger.addHandler(fhd)
  return logger

def getAvailableReports(lobj):
  locationType=lobj.locationType.title()
  if lobj.isNIC is True:
    prefix='NIC'
  else:
    prefix=lobj.stateShortCode
  key=prefix+locationType
  emptyArray=[]
  availableReports=reportTypeDict.get(key,emptyArray)
  return availableReports
