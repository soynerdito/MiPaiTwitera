from speedtest_cli import *
from speedtest_cli import shutdown_event
from speedtest_cli import source
import  speedtest_cli
import math
import time
import os
import sys
import threading
import re
import signal
import socket

class SpeedResults:    
    
    def __init__(self):
        self.ping = 0.0
        self.downloadSpeed = 0.0
        self.uploadSpeed = 0.0

    def __str__(self):
        respresentation = (
            'Ping: %s ms\n' 
            'Download: %s\n'
            'Upload: %s'
            % (self.ping, self.downloadSpeed, self.uploadSpeed ) )
        return respresentation    

def speedresults():
    testResults = SpeedResults()
    speedtest_cli.shutdown_event = threading.Event()
    signal.signal(signal.SIGINT, ctrl_c)
    
    try:
        config = getConfig()
    except URLError:
        print_('Cannot retrieve speedtest configuration')
        sys.exit(1)

    servers = closestServers(config['client'])
    #Ping Results
    best = getBestServer(servers)
    testResults.ping = best['latency']
    #print_('Ping: %(latency)s ms' % best)

    sizes = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
    urls = []
    for size in sizes:
        for i in range(0, 4):
            urls.append('%s/random%sx%s.jpg' %
                        (os.path.dirname(best['url']), size, size))   
    dlspeed = downloadSpeed(urls, True )    
    #print_('Download: %0.2f Mbit/s' % ((dlspeed / 1000 / 1000) * 8))
    testResults.downloadSpeed = '%0.2f Mbit/s' % ((dlspeed / 1000 / 1000) * 8)
    
    sizesizes = [int(.25 * 1000 * 1000), int(.5 * 1000 * 1000)]
    sizes = []
    for size in sizesizes:
        for i in range(0, 25):
            sizes.append(size)

    ulspeed = uploadSpeed(best['url'], sizes, True)
    #print_('Upload: %0.2f Mbit/s' % ((ulspeed / 1000 / 1000) * 8))
    testResults.uploadSpeed = '%0.2f Mbit/s' % ((ulspeed / 1000 / 1000) * 8)
    
    return testResults

def main():
    try:
        result = speedresults()
        print result
    except KeyboardInterrupt:
        print_('\nCancelling...')

if __name__ == '__main__':
    main()
