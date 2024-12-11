# file: runner.py

#
# your alex user code is in ~/.alex/alex
# 
user = 'put-your-alex-user-code-here'

LOOP = True
T = MIN_T = 5 * 60 # once every 5 minutes
dT = 5             # if no jobs found, sleep time T increments by dT.
                   # if a job is found, T resets to MIN_T.
MAX_T = 10 * 60    # max sleep time between runs

import time
import datetime
import urllib.request
import random; random.seed()

start = datetime.datetime.now()

while 1:
    print()
    print("talking to https://ciss450othello.pythonanywhere.com/ ...", flush=True)
    url = 'https://ciss450othello.pythonanywhere.com/s?user=%s' % user
    with urllib.request.urlopen(url) as response:
        now = datetime.datetime.now()
        dt = now - start
        html = response.read().decode().strip()
        if html == 'ERROR':
            print('ERROR')
            break
        else:
            print("now: %s\ndiff: %s\nT: %s\nhtml: %s" % (now, dt, T, html))
            if 'no incomplete matches found' in html:
                #print("no job")
                T += dT
                if T >= MAX_T:
                    T = MAX_T
            else:
                #print("job found")
                T = MIN_T

    if not LOOP:
        print("LOOP is False ... halting ...")
        break

    #==========================================================================
    # Print pause message
    #==========================================================================
    next_T = T + random.randrange(0, 60)
    dt = 1 # Print the pause message once every dt seconds.
           # Increase dt to save on local CPU cycles.
    while 1:
        print(("Ctrl-C to stop ... next run in %s sec        " % next_T) + '\b' * 100,
              flush=True, end='')
        if next_T == 0: break;
        if next_T > dt:
            time.sleep(dt)
            next_T -= dt
        else:
            time.sleep(next_T)
            next_T = 0
    print()
