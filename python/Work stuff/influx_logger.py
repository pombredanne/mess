'''
Author: Tiago Baptista (F3902293)
Purpose: Pull response time stats, send to InfluxDB API in a batch

TO DO:
1) Catch being killed so as to remove the pid.
'''
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td
from influxdb import InfluxDBClient
from Queue import Queue
from threading import Thread
from optparse import OptionParser
import os
import sys
import re
import signal
import time
import json

# Some general settings
logfile = '/home/f3902293/test.log'
influxDbHost = 's3-influx-01'
influxDbPort = 8086

# Main object
class Response:

	def __init__(self):
		#Write new logs into here...could be neater...
		Response.logs = ['CASSANDRA',' FESTER ','GEO',' MORTICIA ','SSO','THING','BehaviorEngine','VODS','DB']

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
        #open(logfile, 'w').close()


    @classmethod
    def bashing(self, cmd):
        print output[0]

    @classmethod
    def getFunction(self, line, log):
        function = re.sub(' ', '', line.split(log)[1].split("call")[0].split("(")[0])
        return function

    @classmethod
    def getDbStuff(self, line):
    	dbOps = {'insert': 'into', 'select': 'from', 'delete': 'from', 'update': 'update'}
    	for ops in dbOps.keys():
    		if ops in line:
    			operation = ops
    			table = line.split(dbOps[ops])[1].split()[0].split("(")[0].split(")")[0]
    			break
    	return operation, table

    @classmethod
    def getInfluxStr(self, **args):
        response = args['rsp']
        hostname = args['hst']
        nanodate = args['ndate']
        responsedb = self.dbDict[args['log']]

        if args['log'] == "DB":
        	operation = args['op']
        	table = args['tbl']
        	JSON = [
        		{
        			"measurement" : responsedb,
        			"tags": {
        				"host": hostname,
        				"operation" : operation,
        				"table": table
    				},
    				"time": nanodate,
    				"fields": {
    					"value": int(response)
    				}
    			}
    		]
    		return JSON
        else:
        	function = args['func']
        	JSON = [
        		{
        			"measurement" : responsedb,
        			"tags": {
        				"host": hostname,
        				"function": function
        			},
        			"time": nanodate,
        			"fields": {
        				"value": int(response)
    				}
				}
			]
		return JSON

    @classmethod
    def convertDate(self, dateStr):
    	dateFormat = "%Y-%m-%d %H:%M:%S,%f"
    	influxFormat = "%Y-%m-%dT%H:%M:%S.%fZ"

        myDate = dateStr[1:-1]
        influxDate = (dt.strptime(myDate, dateFormat) - td(hours=2)).strftime(influxFormat)

        return influxDate

    @classmethod
    def getTheLine(self, line):
    	response = re.sub('ms', '', line.rsplit(None, 1)[-1])
        hostname = line.split()[3]
        nanodate = re.sub('\n', '', self.convertDate(line.split("TIME")[1].split("DEBUG")[0]))

    	for log in self.logs:
    		if log in line:
    			if log == "DB":
    				operation, table = self.getDbStuff(line)
    				influx = self.getInfluxStr(rsp=response, hst=hostname, ndate=nanodate, op=operation, tbl=table, log=log)
    				return influx
    				break
    			else:
    				function = self.getFunction(line, log)
    				influx = self.getInfluxStr(rsp=response, hst=hostname, ndate=nanodate, func=function, log=log)
    				return influx
    				break

    @classmethod
    def processlines(self):
        self.client = InfluxDBClient(host = influxDbHost, port = influxDbPort, database = 'responsetimes')
        for line in self.full:
            try:
            	sendToInflux = self.getTheLine(line)
            	print sendToInflux
            	#self.client.write_points(sendToInflux)
            except Exception as e:
            	print "ERROR in processlines(): %s" % e
            	#raise e
            	continue

def worker(threads):
	if os.stat(logfile).st_size == 0:
		print "Log file is empty, ignoring..."
	else:
		q = Queue()
		workers = []
		
		def threadProc():
			while True:
				pool = q.get()
				#obj1 = Influx()
				#obj1.processlines()
				try:
					print "Processing: %s" % pool
					obj1 = Influx()
					obj1.processlines()
				except Exception as e:
					print "ERROR in worker(): %s" % e
				q.task_done()

		for i in range(threads):
			t = Thread(target=threadProc)
			t.setDaemon(True)
			workers.append(t)
			t.start()

		q.put(logfile)
		q.join()

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

    q = Queue()
    workers = []

    if os.path.isfile(pidfile):
        print("Found an existing pid file: %s") % pidfile
        sys.exit()
    else:
        file(pidfile, 'w').write(pid)
        while True:
	        try:
	        	worker(threads)
	    	except Exception, e:
		    	print("ERROR in main(): %s") % e
		    	#os.unlink(pidfile)
		    	raise e
	    	continue

if __name__ == "__main__":
    main()