import gevent
import signal
import sys


def run_forever():
    gevent.sleep(5)
    sys.exit(0)
    for i in range(1000):
        print i

if __name__ == '__main__':
    try:
        gevent.signal(signal.SIGQUIT, gevent.shutdown)
        thread = gevent.spawn(run_forever)
        thread.join()

    except SystemExit:
        print "exist"