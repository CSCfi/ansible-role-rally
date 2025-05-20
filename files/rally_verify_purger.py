#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Python Script to purge old rally verify runs """

from __future__ import print_function
import subprocess # to run "rally verify list"
from datetime import datetime # to compare dates
import logging # to log to syslog
import logging.handlers
import argparse
import time

import sys # to handle script exit codes

####

PARSER = argparse.ArgumentParser(description='Purge old verify tests.')

PARSER.add_argument('-p', dest='PATTERN', type=str,
                    default="cron",
                    help='grep pattern to match for')
PARSER.add_argument('-s', dest='SAVE_NEWER', type=int,
                    default=90,
                    help='Save newer runs than this amount of days, default: 90')
PARSER.add_argument('-n', dest='SAVE_BEGIN', type=int,
                    default=5,
                    help='Amount from beginning to save, default: 5')
PARSER.add_argument('-d', dest='DEBUG', action='store_true',
                    default=False,
                    help='Turn debug on, otherwise logging by default at INFO')
PARSER.add_argument('-b', dest='BATCH', type=int,
                    default=5,
                    help='For every "modulus 5" verify that we purge, sleep 5 seconds')
PARSER.add_argument('-c', dest='RALLY_CMD', type=int,
                    default='rally',
                    help='Rally command')


ARGS = PARSER.parse_args()

BATCH = ARGS.BATCH
PATTERN = ARGS.PATTERN
SAVE_NEWER = ARGS.SAVE_NEWER
SAVE_BEGIN = ARGS.SAVE_BEGIN
DEBUG = ARGS.DEBUG
RALLY_CMD = ARGS.RALLY_CMD

####

NOW = datetime.now()

# Grabs column 2(UUID) and 6(Started at)
# NOTE: There is a rally python library we could use instead. If you do that, remember to sort
P = subprocess.Popen(
        f"{RALLY_CMD} verify list|grep {PATTERN}|cut -d '|' -f2,6|tail -n +{SAVE_BEGIN}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()[0]
RALLY_VERIFY_LIST = P.split("\n")
# Get rid of empty strings (because above we split on newline)
RALLY_VERIFY_LIST2 = [x for x in RALLY_VERIFY_LIST if x]

def init_log():
    """ Initialize the logging facility"""

    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    formattr = logging.Formatter('%(module)s[%(process)d]: %(levelname)s %(funcName)s: %(message)s')
    handler.setFormatter(formattr)
    log.addHandler(handler)
    return log

def delete_verifys(rally_verify_list, save_these_many_days):
    """ Delete verify runs
	Input: list of lists: [ [ "verifyuuid", "started date" ], [], .. ]
    Output: NA """

    cnt = 0

    for verify in rally_verify_list:
        run = verify.split("|")
        uuid = run[0].strip()
        date = run[1].strip()
        # date format in rally verify list: 2019-07-31T21:00:07
        date_sameasnow = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
        age = NOW-date_sameasnow
        if age.days > save_these_many_days and uuid:
            # NOTE: There is a rally python library that this rally CLI tool uses
            subprocess.Popen(f"{RALLY_CMD} verify delete --uuid {uuid}", shell=True)
            LOG.warning("Deleted verify with UUID=%s because it was too old", uuid)
            cnt = cnt + 1
            if cnt % BATCH:
                time.sleep(BATCH)
        else:
            if DEBUG:
                LOG.info("Did not delete verify with UUID=%s because it is too new", uuid)
            else:
                LOG.debug("Did not delete verify with UUID=%s because it is too new", uuid)

def safety_check(out):
    """ Exit script on errors
	Input: list of lists: [ [ "verifyuuid", "started date" ], [], .. ]
    Output: NA """

    if not out:
        LOG.error("No verifys found in rally verify list, aborting")
        sys.exit(2)

LOG = init_log()
safety_check(RALLY_VERIFY_LIST2)
delete_verifys(RALLY_VERIFY_LIST2, SAVE_NEWER)
