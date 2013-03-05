__author__ = 'micheal'
import signal
import time


def handler(signum, frame):
    print 'Signal handler called with signal', signum
    raise IOError("Couldn't open device!")

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# This open() may hang indefinitely
# fd = os.open('/dev/ttys001', os.O_RDWR)
time.sleep(10)
signal.alarm(0)          # Disable the alarm