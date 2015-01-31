#!/usr/bin/env python

from datetime import datetime
import time, pytz
import urllib2
import csv


URL = 'http://10.0.0.1/status'
DELAY = 1 # seconds
PERIOD = 86400 # seconds


def run(datawriter, start):
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = int(time.time())
    while start + PERIOD > now:
        res = urllib2.urlopen(URL)
        data = res.read().split()
        try:
            SINR = data[19].split('=')[-1]
            RSSI = data[20].split('=')[-1]
            RSRP = data[21].split('=')[-1]
            ts = int(time.mktime(moscow_tz.localize(datetime.now()).timetuple()))
            print('SINR:', SINR, 'RSSI', RSSI, 'RSRP:', RSRP, 'TS', ts)
            datawriter.writerow([SINR, RSSI, RSRP, ts])
        except IndexError:
            pass
        time.sleep(DELAY)
        now = int(time.time())


def main():
    start = int(time.time())
    with open('./stats.csv', 'wb') as csvfile:
        datawriter = csv.writer(csvfile)
        run(datawriter, start)


if __name__ == '__main__':
    main()
