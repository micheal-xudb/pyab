__author__ = 'micheal'
import sys
import getopt
import urllib2
import gevent
import time
import signal
import ast


# input param
request_num = 1
concurrency = 1
dest_url = 'http://localhost'
post_data = None
time_limit = 360000
# output data
request_success = 0
request_fail = 0
total_size = 0
single_request_time = []
time_taken = 0
port = 80
server_info = None
host_info = []


def main(argv):
    global time_taken, time_limit
    time_start = time.time()
    get_para_result = get_para(argv)
    if not get_para_result:
        help_msg()
    # signal for the timelimit param
    # signal.signal(signal.SIGALRM, timeout_handler)
    # signal.alarm(time_limit)

    test_round = request_num / concurrency
    gevent.signal(signal.SIGQUIT, gevent.shutdown)

    for i in range(test_round):
        time_out = time_limit
        time_gevent_start = time.time()
        jobs = []
        for con in range(int(concurrency)):
            jobs.append(gevent.spawn(make_request, dest_url))
        if time_out > 0:
            try:
                gevent.Timeout(1).start()
                gevent.joinall(jobs, timeout=1, raise_error=True)
            except gevent.Timeout:
                print 'gevent timeout'
            time_gevent_finish = time.time()
            time_per_gevent = time_gevent_finish - time_gevent_start
            time_limit -= time_per_gevent
        else:
            print '\n Can not finish the test in time limit'
            help_msg()

    time_finish = time.time()
    time_taken = time_finish - time_start
    output_msg()
    # signal.alarm(0)


def timeout_handler(signum, frame):
    print 'Signal handler called with signal', signum
    print "can not finish the test in time limit"
    sys.exit(0)


def get_para(argv):
    global dest_url, request_num, concurrency, time_limit, server_info, port, host_info
    try:
        opts, args = getopt.getopt(argv, "n:c:p:t:h", ["requests=", "concur=", "post=", "timelimit=", "help"])
        # print opts, args  [('-n', '100'), ('-c', '2')] ['localhost/']
        try:
            dest_url = args[0]  # hostname of the server
        except IndexError:
            pass
        for option, arg in opts:
            if option in ('-n', '--requests'):
                try:
                    request_num = int(arg)
                except ValueError:
                    print '\n request_num must be integer'
                    return None
                if request_num < 1:
                    print '\n request_num must larger than 0 !'
                    return None

            elif option in ('-c', '--concurrency'):
                try:
                    concurrency = int(arg)
                except ValueError:
                    print '\n concurrency must be integer'
                    return None
                if concurrency < 1:
                    print '\n concurrency must larger than 0'
                    return None

            elif option in ('-p', '--post'):
                try:
                    post_file = arg
                    with open(post_file) as file:
                        post_str = file.read()
                        post_data = ast.literal_eval(post_str)
                except IOError:
                    print '\n can not open post file!'
                except SyntaxError:
                    print '\n post file format error!'
                if sys.getsizeof(post_data) < 1:
                    print '\n empty post file!'

            elif option in ('-t', '--timelimit'):
                try:
                    time_limit = int(arg)
                except ValueError:
                    print '\n time_limit must be integer'
                    return None
                if concurrency < 1:
                    print '\n time_limit must larger than 0'
                    return None
            elif option in ('-h', '--help'):
                return None
        # get host_info and server_info , a test of the server
        host_info = dest_url.split(':')
        try:
            server_info = urllib2.urlopen(dest_url).info()
            port = host_info[2]
        except IndexError:
            port = 80
        except urllib2.URLError, e:
            print e.reason
            help_msg()
    except getopt.GetoptError:
        print "\n getopt error !"
        help_msg()
    return 1


def make_request(url):
    global request_success, request_fail, total_size, single_request_time
    request = urllib2.Request(url, data=post_data)
    try:
        req_time_start = time.time()
        response = urllib2.urlopen(request)
        req_time_finish = time.time()
        single_request_time.append((req_time_finish - req_time_start) * 1000)  # transfer sec to ms
        if response.getcode() == 200:
            request_success += 1
            data = response.read()
            size = sys.getsizeof(data)
            total_size += size
        else:
            request_fail += 1
    except urllib2.URLError, e:
        print e.reason
        print 'URLError error!!!'
        help_msg()
    except SystemExit:
        raise Exception


def output_msg():

    # print server_info.values()
    # print server_info.keys()
    print 'Server Softeware:     %s' % server_info['server']
    print 'Server hostname:      %s' % host_info[1][2:]
    print 'Server port:          %s' % port
    try:
        content_location = server_info['content-location']
    except KeyError:
        content_location = 'Unkonwn'
    print 'Document path:        %s' % content_location
    try:
        content_length = server_info['content-length']
    except KeyError:
        content_length = 'Unkonwn'
    print 'Document length:      %s bytes' % content_length
    print 'Time taken for tests: %s sec' % time_taken
    print 'Concurrency Level:    %s' % concurrency
    print 'Complete requests:    %s' % request_success
    print 'Failed requests:      %s' % request_fail
    print 'HTML transferred:     %s bytes' % total_size
    print 'Requests per second:  %s [#/sec] (mean)' % (request_success / time_taken)
    print 'Time per request:     %s [ms] (mean)' % (time_taken / request_success * 1000)
    print 'Transfer rate:        %s [Kbytes/sec] received' % (total_size / 1000 / time_taken)
    print 'Percentage of the requests served within a certain time (ms)'
    single_request_time.sort()
    # print single_request_time

    print '50%%    %s ' % single_request_time[request_success / 2 - 1]
    print '100%%   %s (longest request)' % single_request_time[-1]


def help_msg():
    print '''
    Usage: python pyab.py [options] [http://hostname[:port]/path]
    Options are:
        -n --requests     Number of requests to perform
        -c --concurrency  Number of multiple requests to make
        -t --timelimit    Seconds to max. wait for responses
        -p --post         File containing data to POST
        -h --help         Print this usage
    Default value:
        python pyab.py -n 1 -c 1 -t 360000 http://localhost
    '''
    sys.exit(0)


if __name__ == '__main__':
    result = main(sys.argv[1:])
    if result:
        output_msg()