'''
Author: Tiago Baptista (F3902293)
Purpose: To assist in Zabbix auto discovery for various BA functions
'''
#/usr/bin/env python

import json
import os
import functions

# Variables
logfile = '/var/log/'
functionsList = []


class Functions:

    def __init__(self):
        Functions.mJsonDataList = []
        print "Main class"


def main():
    pid = str(os.getpid())
    pidfile = "/var/run/testers/functions-monitor.pid"

    if os.path.isfile(pidfile):
        print("Found an existing pid file: %s") % pidfile
        sys.exit()
    else:
        file(pidfile, 'w').write(pid)

        if os.stat(logfile).st_size == 0:
            print "Log file is empty, exiting..."
            os.unlink(pidfile)
            sys.exit()
        else:
            obj1 = Functions()
            print "{\"data\":\n"
            # for results in obj1.full:
            #	obj1.create_vars(results)
            #	version = obj1.versionlist[obj1.counter - 1]
            #	update_json(obj1.dict, version)

        # print json.dumps(obj1.mJsonDataList)
        print "}"
        # open(logfile, 'w').close()
        os.unlink(pidfile)


if __name__ == "__main__":
    main()
