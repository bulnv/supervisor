#!/usr/bin/env python3
import subprocess
import logging
import argparse
import shlex
import os
import time

try:
    from threading import _Timer
except ImportError:
    from threading import Timer as _Timer  # Python 3.3+


parser = argparse.ArgumentParser(description='Supervisor demo python implementation')
parser.add_argument('-c','--cooldown', default=5, type=int, help='Seconds to cooldown between atempts to restart')
parser.add_argument('-n', '--number_attempts', default=3, type=int, help='Number of attempts before giving up')
parser.add_argument('-p', '--process', type=str, help='Name of the process to supervise', required=True)
parser.add_argument('-i', '--inetrval_check', default=10, type=int, help='Check interval in seconds')
parser.add_argument('-l', '--logs_toggle', default=True, type=bool, help='Generate logs in case of events')
parser.add_argument('-d', '--debug', action='store_true', help='Debugging mode')
args = parser.parse_args()

LOGGING = args.logs_toggle
DEBUG = args.debug
COOLDOWN = args.cooldown
NATTEMPTS = args.number_attempts
PROCESS = args.process
INTCHECK = args.inetrval_check
FAILCOUNT = 0
RUNNUMBER = 0
TOO_FAST_PROT = 1.5 #protection from too fast start



handlers = [] 
if DEBUG:
    handlers.append(logging.StreamHandler())
if LOGGING:
    handlers.append(logging.FileHandler("supervisor.log"))
    
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s][%(threadName)s] %(message)s",
    handlers=handlers
)

def named_timer(name, interval, function, *args, **kwargs):
    timer = _Timer(interval, function, *args, **kwargs)
    timer._name = name
    return timer

def start_subprocess():
    global FAILCOUNT, NATTEMPTS, RUNNUMBER
    RUNNUMBER+=1
    subprocess_args = shlex.split(PROCESS)
    reschedule = False
    try:
        proc = subprocess.Popen(subprocess_args)
        logging.info('Trying to start {}'.format(PROCESS))
    except OSError as e:
        logging.info('Something went wrong while process starting with error message: ```{}```'.format(e))
        reschedule = True
    else:
        time.sleep(TOO_FAST_PROT)
        if proc.poll() is not None:
            reschedule = True
        else:
            logging.info('Process has been started')
            monitor_process(proc)
    if reschedule:
        logging.info('COOLDOWN. Process started and ended')
        FAILCOUNT+=1
        if FAILCOUNT < NATTEMPTS:
            logging.info('Lets try to reschedule the process in {} seconds. {} tries left'.format(COOLDOWN,NATTEMPTS-FAILCOUNT))
            named_timer('start-sproc-{}'.format(RUNNUMBER), COOLDOWN, start_subprocess).start()
        else:
            logging.info('No more tries left. Exiting...')
            os._exit(1)


def monitor_process(proc):
    global FAILCOUNT, RUNNUMBER
    check_result = proc.poll()
    logging.info('Start process check')
    
    if check_result is not None:
        FAILCOUNT+=1
        logging.info('Process has exited with {} code'.format(check_result))
        if FAILCOUNT < NATTEMPTS:
            logging.info('Int check failed. Lets try to reschedule the process in {} seconds. {} tries left'.format(COOLDOWN,NATTEMPTS-FAILCOUNT))
            named_timer('mon-process-{}'.format(RUNNUMBER), COOLDOWN, start_subprocess).start()
        else:
            logging.info('No more tries left. Exiting...')
            os._exit(1)
    else:
        logging.info('Running. See ya in {} sec'.format(INTCHECK))
        named_timer('mon-process-{}'.format(RUNNUMBER),INTCHECK, monitor_process, [proc]).start()


def do_supervise(args):
    logging.info('Starting to supervise ```{}``` process'.format(args.process))
    start_subprocess()


if __name__ == "__main__":
    do_supervise(args)
