# Python Version: 3.x
import onlinejudge
import onlinejudge.implementation.utils as utils
import onlinejudge.implementation.logging as log
import subprocess
import sys
import time
import datetime
from typing import *
if TYPE_CHECKING:
    import argparse

default_url_opener = [ 'sensible-browser', 'xdg-open', 'open' ]

def standby(args: 'argparse.Namespace') -> None:
    # open problem A
    log.info('contest starts at ' + args.contest_time)
    log.info('now waiting...')
    while True:
        if str(datetime.datetime.now().strftime('%X')) >= args.contest_time:
            subprocess.check_call([ 'explorer', args.url + '_a' ], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
            break
        time.sleep(0.5)
