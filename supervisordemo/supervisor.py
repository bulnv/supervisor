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


def named_timer(name, interval, function, *args, **kwargs):
    timer = _Timer(interval, function, *args, **kwargs)
    timer._name = name
    return timer


class SuperVisor:
    def __init__(self, args):
        self.LOGGING = args['logs_toggle']
        self.DEBUG = args['debug']
        self.COOLDOWN = args['cooldown']
        self.NATTEMPTS = args['number_attempts']
        self.PROCESS = args['process']
        self.INTCHECK = args['inetrval_check']
        self.failcount = 0
        self.runnumber = 0
        self.TOO_FAST_PROT = 1.5  # protection from too fast start
        self._result = {}
        self._result.setdefault('success', 0)
        self._result.setdefault('fail', 0)
        self.process_stack = []

    @property
    def result(self):
        return self._result

    def fail_process(self):
        self.failcount += 1
        self._result['fail'] += 1

    @property
    def progressbar(self):
        return round((self.runnumber / self.NATTEMPTS) * 100, 2)

    def succ_process(self):
        self.failcount += 1
        self._result['success'] += 1

    def times_to_retry(self):
        return self.NATTEMPTS - self.failcount

    def tick_counter(self):
        self.runnumber += 1

    def append_process_to_stack(self):
        self.process_stack.append(1)

    def pop_process_from_stack(self):
        self.process_stack.append(1)

    def processes_in_stack(self):
        return len(self.stack)

    def start_subprocess(self):
        self.tick_counter()
        subprocess_args = shlex.split(self.PROCESS)
        reschedule = False
        try:
            proc = subprocess.Popen(subprocess_args)
            logging.info('Trying to start {}'.format(self.PROCESS))
        except OSError as e:
            logging.info('Something went wrong while process starting with error message: ```{}```'.format(e))
            reschedule = True
        else:
            time.sleep(self.TOO_FAST_PROT)
            if proc.poll() is not None:
                reschedule = True
            else:
                logging.info('Process has been started')

                self.monitor_process(proc)
        if reschedule:
            logging.info('COOLDOWN. Process started and ended')
            self.fail_process()
            if self.failcount < self.NATTEMPTS:
                logging.info('Lets try to reschedule the process '
                             'in {} seconds. {}  tries left'.format(self.COOLDOWN, self.times_to_retry()))
                named_timer('start-sproc-{}'.format(self.runnumber), self.COOLDOWN, self.start_subprocess).start()
            else:
                logging.info('No more tries left. Exiting...')
                os._exit(1)

    def monitor_process(self, proc):
        check_result = proc.poll()
        logging.info('Start process check')

        if check_result is not None:
            if check_result == 0:
                self.succ_process()
            else:
                self.fail_process()
            logging.info('Process has exited with {} code'.format(check_result))
            if self.failcount < self.NATTEMPTS:
                logging.info('Int check failed. Lets try to reschedule the process in {} seconds. {} tries left'.format(
                    self.COOLDOWN, self.times_to_retry()))
                named_timer('mon-process-{}'.format(self.runnumber), self.COOLDOWN, self.start_subprocess).start()
            else:
                logging.info('No more tries left. Exiting...')
                os._exit(1)
        else:
            logging.info('Running. See ya in {} sec'.format(self.INTCHECK))
            named_timer('mon-process-{}'.format(self.runnumber), self.INTCHECK, self.monitor_process, [proc]).start()


def do_supervise(args):
    logging.info('Starting to supervise ```{}``` process'.format(args.process))
    sv = SuperVisor(args.__dict__)
    sv.start_subprocess()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Supervisor demo python implementation')
    parser.add_argument('-c', '--cooldown', default=5, type=int, help='Seconds to cooldown between atempts to restart')
    parser.add_argument('-n', '--number_attempts', default=3, type=int, help='Number of attempts before giving up')
    parser.add_argument('-p', '--process', type=str, help='Name of the process to supervise', required=True)
    parser.add_argument('-i', '--inetrval_check', default=10, type=int, help='Check interval in seconds')
    parser.add_argument('-l', '--logs_toggle', default=True, type=bool, help='Generate logs in case of events')
    parser.add_argument('-d', '--debug', action='store_true', help='Debugging mode')
    args = parser.parse_args()
    handlers = []
    if args.debug:
        handlers.append(logging.StreamHandler())
    if args.logs_toggle:
        handlers.append(logging.FileHandler("supervisor.log"))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s][%(threadName)s] %(message)s",
        handlers=handlers
    )
    do_supervise(args)
