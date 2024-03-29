'''
Author: Tiago Baptista (F3902293)
Purpose: Pull response time stats, send to InfluxDB API in a batch

TO DO:
1) Catch being killed so as to remove the pid.
2) Property (.ini) file for general settings and log types to search for
3) Split out json generator
4) Fix random SSO values
5) Proper logging implementation (format interpreter per log type???)
6) systemctl integration and package installer
'''
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td
from optparse import OptionParser
import os
import re
import InfluxHelper
from InfluxConfig import ConfigBuilder
from InfluxThreader import ThreadPool


# Some general settings
logfile = '/var/log/output/influx.log'
influxDbHost = '172.18.223.110'
influxDbPort = 8086


# Main object
class Response:

	def __init__(self):
		#Write new logs into here...could be neater...
		Response.logs = ['CASSANDRA',' FESTER ','GEO',' MORTICIA ','SSO','THING','BehaviorEngine','VODS','DB','INTEGRATION', 'CYCLOPS', 'Gomez', 'XAVIER']
		Response.dbDict = {}
		print "Initializing..."
		for entry in self.logs:
			Response.dbDict[entry] = re.sub(' ', '',entry.lower()) + "responses"

class Influx(Response):

    def __init__(self):
    	Response.__init__(self)
        Influx.full = []
        ignoreString = ['java.sql.PreparedStatement.executeUpdate()']
        with open(logfile) as self.f:
            for line in self.f:
                if ignoreString[0] in line.split():
                    pass
                else:
                    Influx.full.append(re.sub('\n', '', line))
        open(logfile, 'w').close()

# Main process
def main():
    pid = str(os.getpid())
    pidfile = "/tmp/influxdb.pid"
    # Build config, split out into however many main threads required
    config = ConfigBuilder

    if os.path.isfile(pidfile):
        print("Found an existing pid file: %s") % pidfile
        sys.exit()
    
    file(pidfile, 'w').write(pid)
    while True:
        try:
            if os.stat(logfile).st_size == 0:
                pass
            else:
                fileSize = InfluxHelper.file_len(logfile)
                if fileSize < 1000:
                    #print "Log file is too small: %s lines. Ignoring..." % fileSize
                    continue
                else:
                    # Spawn x threads depending on how many logfiles we're reading in
                    obj1 = Influx()
                    InfluxHelper.processlines(obj1, influxDbHost, influxDbPort)
        except Exception as e:
            print("ERROR in main(): %s") % e
            #raise e
            continue
        finally:
            os.unlink(pidfile)

if __name__ == "__main__":
    sys.exit(main())
