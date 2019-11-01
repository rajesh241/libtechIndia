#!/bin/bash
#First we will kill the process if it is older than 3 hours
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo DIR
cd $DIR/../../../../../venv/
pwd
source bin/activate
cmd="python $DIR/cron.py -e"
$cmd
