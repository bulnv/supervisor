# Supervisor demo implementation
### Features

- Automatic process start after failure or expected exit;
- Cooldown preiod between retries [default 5 sec];
- Number of retries before give-up [default 3 times];
- Name of the process to lift-up;
- Logs [default enabled];
- Debug mode [default disabled];
- Check interval [default 10 sec]
- Multithreading as timer;

### Usage

```
usage: supervisor.py [-h] [-c COOLDOWN] [-n NUMBER_ATTEMPTS] -p PROCESS
               [-i INETRVAL_CHECK] [-l LOGS_TOGGLE]

Supervisor demo python implementation

optional arguments:
  -h, --help            show this help message and exit
  -c COOLDOWN, --cooldown COOLDOWN
                        Seconds to cooldown between atempts to restart
  -n NUMBER_ATTEMPTS, --number_attempts NUMBER_ATTEMPTS
                        Number of attempts before giving up
  -i INETRVAL_CHECK, --inetrval_check INETRVAL_CHECK
                        Check interval in seconds
  -l LOGS_TOGGLE, --logs_toggle LOGS_TOGGLE
                        Generate logs in case of events

required named arguments:
  -p PROCESS, --process PROCESS
                        Name of the process to supervise
```


### Examples

- `bash -c "sleep 1 && exit 0"`

```sh
./supervisor.py -p 'bash -c "sleep 1 && exit 0"' -d
2020-10-04 20:40:55,963 [INFO][MainThread] Starting to supervise ```bash -c "sleep 1 && exit 0"``` process
2020-10-04 20:40:55,969 [INFO][MainThread] Trying to start bash -c "sleep 1 && exit 0"
2020-10-04 20:40:57,470 [INFO][MainThread] COOLDOWN. Process started and ended
2020-10-04 20:40:57,471 [INFO][MainThread] Lets try to reschedule the process in 5 seconds. 2 tries left
2020-10-04 20:41:02,477 [INFO][start-sproc-1] Trying to start bash -c "sleep 1 && exit 0"
2020-10-04 20:41:03,979 [INFO][start-sproc-1] COOLDOWN. Process started and ended
2020-10-04 20:41:03,979 [INFO][start-sproc-1] Lets try to reschedule the process in 5 seconds. 1 tries left
2020-10-04 20:41:08,986 [INFO][start-sproc-2] Trying to start bash -c "sleep 1 && exit 0"
2020-10-04 20:41:10,487 [INFO][start-sproc-2] COOLDOWN. Process started and ended
2020-10-04 20:41:10,488 [INFO][start-sproc-2] No more tries left. Exiting...
```

- `bash -c "sleep 5 && exit 0"`

```sh
./supervisor.py -p 'bash -c "sleep 5 && exit 0"' -d
2020-10-04 20:41:30,152 [INFO][MainThread] Starting to supervise ```bash -c "sleep 5 && exit 0"``` process
2020-10-04 20:41:30,158 [INFO][MainThread] Trying to start bash -c "sleep 5 && exit 0"
2020-10-04 20:41:31,660 [INFO][MainThread] Process has been started
2020-10-04 20:41:31,661 [INFO][MainThread] Start process check
2020-10-04 20:41:31,661 [INFO][MainThread] Running. See ya in 10 sec
2020-10-04 20:41:41,663 [INFO][mon-process-1] Start process check
2020-10-04 20:41:41,664 [INFO][mon-process-1] Process has exited with 0 code
2020-10-04 20:41:41,664 [INFO][mon-process-1] Int check failed. Lets try to reschedule the process in 5 seconds. 2 tries left
2020-10-04 20:41:46,671 [INFO][mon-process-1] Trying to start bash -c "sleep 5 && exit 0"
2020-10-04 20:41:48,173 [INFO][mon-process-1] Process has been started
2020-10-04 20:41:48,173 [INFO][mon-process-1] Start process check
2020-10-04 20:41:48,174 [INFO][mon-process-1] Running. See ya in 10 sec
2020-10-04 20:41:58,175 [INFO][mon-process-2] Start process check
2020-10-04 20:41:59,919 [INFO][mon-process-2] Process has exited with 0 code
2020-10-04 20:41:59,971 [INFO][mon-process-2] Int check failed. Lets try to reschedule the process in 5 seconds. 1 tries left
2020-10-04 20:42:04,979 [INFO][mon-process-2] Trying to start bash -c "sleep 5 && exit 0"
2020-10-04 20:42:06,481 [INFO][mon-process-2] Process has been started
2020-10-04 20:42:06,482 [INFO][mon-process-2] Start process check
2020-10-04 20:42:06,482 [INFO][mon-process-2] Running. See ya in 10 sec
2020-10-04 20:42:16,484 [INFO][mon-process-3] Start process check
2020-10-04 20:42:16,485 [INFO][mon-process-3] Process has exited with 0 code
2020-10-04 20:42:16,485 [INFO][mon-process-3] No more tries left. Exiting...
```

- `bash -c "sleep 1 && exit 1"`

```sh
./supervisor.py -p 'bash -c "sleep 1 && exit 1"' -d
2020-10-04 20:43:24,230 [INFO][MainThread] Starting to supervise ```bash -c "sleep 1 && exit 1"``` process
2020-10-04 20:43:24,235 [INFO][MainThread] Trying to start bash -c "sleep 1 && exit 1"
2020-10-04 20:43:25,736 [INFO][MainThread] COOLDOWN. Process started and ended
2020-10-04 20:43:25,736 [INFO][MainThread] Lets try to reschedule the process in 5 seconds. 2 tries left
2020-10-04 20:43:30,743 [INFO][start-sproc-1] Trying to start bash -c "sleep 1 && exit 1"
2020-10-04 20:43:32,244 [INFO][start-sproc-1] COOLDOWN. Process started and ended
2020-10-04 20:43:32,245 [INFO][start-sproc-1] Lets try to reschedule the process in 5 seconds. 1 tries left
2020-10-04 20:43:37,251 [INFO][start-sproc-2] Trying to start bash -c "sleep 1 && exit 1"
2020-10-04 20:43:38,752 [INFO][start-sproc-2] COOLDOWN. Process started and ended
2020-10-04 20:43:38,753 [INFO][start-sproc-2] No more tries left. Exiting...
```

- `sh -c "sleep 10 && exit 1"`

```sh
./supervisor.py -p 'sh -c "sleep 10 && exit 1"' -d
2020-10-04 20:44:34,065 [INFO][MainThread] Starting to supervise ```sh -c "sleep 10 && exit 1"``` process
2020-10-04 20:44:34,070 [INFO][MainThread] Trying to start sh -c "sleep 10 && exit 1"
2020-10-04 20:44:35,571 [INFO][MainThread] Process has been started
2020-10-04 20:44:35,572 [INFO][MainThread] Start process check      
2020-10-04 20:44:35,572 [INFO][MainThread] Running. See ya in 10 sec
2020-10-04 20:44:45,574 [INFO][mon-process-1] Start process check
2020-10-04 20:44:45,575 [INFO][mon-process-1] Process has exited with 1 code
2020-10-04 20:44:45,575 [INFO][mon-process-1] Int check failed. Lets try to reschedule the process in 5 seconds. 2 tries left
2020-10-04 20:44:50,584 [INFO][mon-process-1] Trying to start sh -c "sleep 10 && exit 1"
2020-10-04 20:44:52,085 [INFO][mon-process-1] Process has been started
2020-10-04 20:44:52,085 [INFO][mon-process-1] Start process check
2020-10-04 20:44:52,086 [INFO][mon-process-1] Running. See ya in 10 sec
2020-10-04 20:45:02,087 [INFO][mon-process-2] Start process check
2020-10-04 20:45:02,088 [INFO][mon-process-2] Process has exited with 1 code
2020-10-04 20:45:02,089 [INFO][mon-process-2] Int check failed. Lets try to reschedule the process in 5 seconds. 1 tries left
2020-10-04 20:45:07,095 [INFO][mon-process-2] Trying to start sh -c "sleep 10 && exit 1"
2020-10-04 20:45:08,597 [INFO][mon-process-2] Process has been started
2020-10-04 20:45:08,598 [INFO][mon-process-2] Start process check
2020-10-04 20:45:08,598 [INFO][mon-process-2] Running. See ya in 10 sec
2020-10-04 20:45:18,600 [INFO][mon-process-3] Start process check
2020-10-04 20:45:18,601 [INFO][mon-process-3] Process has exited with 1 code
2020-10-04 20:45:18,601 [INFO][mon-process-3] No more tries left. Exiting...
```

- `bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"`

```sh
./supervisor.py -p 'bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"' -d
2020-10-04 20:49:17,440 [INFO][MainThread] Starting to supervise ```bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"``` process
2020-10-04 20:49:17,446 [INFO][MainThread] Trying to start bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"
2020-10-04 20:49:18,947 [INFO][MainThread] Process has been started
2020-10-04 20:49:18,948 [INFO][MainThread] Start process check
2020-10-04 20:49:18,948 [INFO][MainThread] Running. See ya in 10 sec
2020-10-04 20:49:28,950 [INFO][mon-process-1] Start process check
2020-10-04 20:49:28,951 [INFO][mon-process-1] Process has exited with 1 code
2020-10-04 20:49:28,952 [INFO][mon-process-1] Int check failed. Lets try to reschedule the process in 5 seconds. 2 tries left
2020-10-04 20:49:33,958 [INFO][mon-process-1] Trying to start bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"
2020-10-04 20:49:35,460 [INFO][mon-process-1] COOLDOWN. Process started and ended
2020-10-04 20:49:35,461 [INFO][mon-process-1] Lets try to reschedule the process in 5 seconds. 1 tries left
2020-10-04 20:49:40,467 [INFO][start-sproc-2] Trying to start bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"
2020-10-04 20:49:41,970 [INFO][start-sproc-2] COOLDOWN. Process started and ended
2020-10-04 20:49:41,970 [INFO][start-sproc-2] No more tries left. Exiting...
```

- `bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"` one run

```sh
./supervisor.py -p 'bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"' -d -n 1
2020-10-04 20:50:47,545 [INFO][MainThread] Starting to supervise ```bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"``` process
2020-10-04 20:50:47,552 [INFO][MainThread] Trying to start bash -c "if [ -f lock ]; then exit 1; fi; sleep 10 && touch lock && exit 1"
2020-10-04 20:50:49,053 [INFO][MainThread] Process has been started
2020-10-04 20:50:49,054 [INFO][MainThread] Start process check
2020-10-04 20:50:49,054 [INFO][MainThread] Running. See ya in 10 sec
2020-10-04 20:50:59,056 [INFO][mon-process-1] Start process check
2020-10-04 20:50:59,057 [INFO][mon-process-1] Process has exited with 1 code
2020-10-04 20:50:59,058 [INFO][mon-process-1] No more tries left. Exiting...
```