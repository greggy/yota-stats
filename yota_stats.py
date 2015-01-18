#!/usr/bin/env python

import urllib2
import time
import csv


URL = 'http://10.0.0.1/status'
DELAY = 1 # seconds
PERIOD = 100 # seconds


def run(datawriter, start):
    now = time.time()
    while start + PERIOD > now:
        res = urllib2.urlopen(URL)
        data = res.read().split()
        SINR = data[19].split('=')[-1]
        RSRP = data[21].split('=')[-1]
        ts = str(time.time()).split('.')[0]
        print('SINR:', SINR, 'RSRP:', RSRP, 'TS', ts)
        datawriter.writerow([SINR, RSRP, ts])
        time.sleep(DELAY)
        now = time.time()


def main():
    start = time.time()
    with open('./stats.csv', 'wb') as csvfile:
        datawriter = csv.writer(csvfile)
        run(datawriter, start)


if __name__ == '__main__':
    main()
