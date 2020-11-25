#!/bin/bash
#First we will kill the process if it is older than 3 hours
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo DIR
cd $DIR/../backend/venv
source bin/activate
#export PYTHONPATH="${PYTHONPATH}:/home/crawler/repo/libtechIndiaCrawler/"
export PYTHONPATH="${PYTHONPATH}:$HOME/repo/libtechIndia/backend/"


#python $DIR/../backend/src/nrega/crawler/scripts/create_bundle.py -$1  &> /tmp/bundle.log
cmd="python $DIR/../backend/src/nrega/crawler/scripts/create_bundle.py -$1"

myPID=$(pgrep -f "$cmd")
echo $myPID
if [ -z "$myPID" ]
then
  echo "Variable is empty"
else
  echo "Variable is not empty"
  myTime=`ps -o etimes= -p "$myPID"`
  echo $myTime
  if [ $myTime -gt 43200 ]
    then
      echo "Time is about 12 hours"
      kill -9 $myPID
  fi
fi
# 28800 corresponds to roughly 8 hours
pgrep -f "$cmd" || $cmd &> /tmp/bundle.log
