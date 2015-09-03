'''
Author: Tiago Baptista (F3902293)
Purpose: Pull response time stats, send to InfluxDB API in a batch

TO DO:
1) Catch being killed so as to remove the pid.
'''
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td
from optparse import OptionParser
import os
import re
import time
import InfluxHelper

# Some general settings
#logfile = '/home/f3902293/test.log'
logfile = '/var/log/output/influx.log'
influxDbHost = '172.18.223.199'
influxDbPort = 8086

# Main object
class Response:

	def __init__(self):
		#Write new logs into here...could be neater...
		#Response.logs = ['CASSANDRA',' FESTER ','GEO',' MORTICIA ','SSO','THING','BehaviorEngine','VODS','DB']
		Response.logs = ['VODS']
		Response.dbDict = {}
		print "Initializing..."
		for entry in self.logs:
			Response.dbDict[entry] = re.sub(' ', '',entry.lower()) + "responses"

class Influx(Response):

    def __init__(self):
    	Response.__init__(self)
        Influx.full = []
        with open(logfile) as self.f:
            for line in self.f:
                Influx.full.append(re.sub('\n', '', line))
        open(logfile, 'w').close()

# Main process
def main():
    pid = str(os.getpid())
    pidfile = "/tmp/influxdb.pid"

    p = OptionParser("usage: influx_logger.py -t<no. of threads>")
    p.add_option('-t', '--threads', dest='threads',
                help='quantity of THREADS for processing',
                metavar='THREADS')
    (options, args) = p.parse_args()
    threads = int(options.threads) if options.threads else 10

    if os.path.isfile(pidfile):
        print("Found an existing pid file: %s") % pidfile
        sys.exit()
    else:
        file(pidfile, 'w').write(pid)
        while True:
            try:
		fileSize = InfluxHelper.file_len(logfile)
                if fileSize < 500:
                    #print "Log file is too small: %s lines. Ignoring..." % fileSize
		    continue
                else:
                    obj1 = Influx()
                    InfluxHelper.processlines(obj1, influxDbHost, influxDbPort)
            except Exception as e:
                print("ERROR in main(): %s") % e
                #raise e
            continue

if __name__ == "__main__":
    main()
