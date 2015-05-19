'''
Author: Tiago Baptista
Purpose: Update zabbix with counters from log file.
'''

import subprocess
import re
import os
import sys
import socket

logfile = "/var/log/output/buffer.log"
CHECK = ["size", "max", "avg", "tasks"]
host = re.sub('.fnbconnect.co.za', '', socket.gethostname())
zabbix_serv = '192.168.35.151'


class Counter:

    def __init__(self):

        Counter.versionlist = []
        Counter.full = []
        Counter.counter = 0

        self.f = open(logfile, "r")
        for line in self.f:
            Counter.versionlist.append(line.split("_")[1])
            Counter.full.append(self.create_list(line.split()))

        self.f.close()

    def create_list(self, iterable):
        while len(iterable) != 4:
            for word in iterable:
                if word.split("[")[0] in CHECK:
                    continue
                else:
                    iterable.remove(word)
        return iterable

    @classmethod
    def create_vars(self, single):
        self.counter += 1

        self.dict = {}
        for field in single:
            name = field.split("[")[0]
            value = re.sub('[^0-9]', '', field)
            self.dict[name] = value


def update_zabbix(dict, version):
    for key in dict:
        value = dict[key]
        item = "/usr/sbin/zabbix_sender -z " + zabbix_serv + " -s " + host + " -k " + version + ".auditbuffer." + key + " -o " + str(value)
        print item
        process = subprocess.Popen(item, shell=True, stdout=subprocess.PIPE)
        output = process.communicate()
        print output


def main():
    pid = str(os.getpid())
    pidfile = "/var/run/audit_queue_monitor.pid"

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
            obj1 = Counter()
            obj1.processed = []

            for results in obj1.full:
                obj1.create_vars(results)
                version = obj1.versionlist[obj1.counter - 1]

                if version in obj1.processed:
                    print "Found so not processing"
                elif reduce(lambda x, y: int(x) + int(y), obj1.dict.values()) == 0:
                    print "Tasks = 0 so skipping..."
                else:
                    print "Processing..."
                    print version, obj1.dict
                    obj1.processed.append(version)
                    update_zabbix(obj1.dict, version)

            open(logfile, 'w').close()
            os.unlink(pidfile)

if __name__ == "__main__":
    main()
