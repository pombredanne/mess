#!/usr/bin/env python2.6

import re
import os
import sys
import json


logfile = "/var/log/buffer.log"
CHECK = ["size", "max", "avg", "tasks"]


class Counter:

    def __init__(self):

        Counter.versionlist = []
        Counter.full = []
        Counter.counter = 0
        Counter.mJsonDataList = []

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


def update_json(dict, version):
    for key in dict:
        value = dict[key]

        json_dict = {"{#FESTERINSTANCE}": version, "{#AUDITCHECK}": key, "{#AUDITVALUE}": str(value)}
        Counter.mJsonDataList.append(json_dict)


def main():
    pid = str(os.getpid())
    pidfile = "/var/run/audit_queue_monitor/audit_queue_monitor_json.pid"

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
            print "{\"data\":\n"
            for results in obj1.full:
                obj1.create_vars(results)
                version = obj1.versionlist[obj1.counter - 1]
                update_json(obj1.dict, version)

            print json.dumps(obj1.mJsonDataList)
            print "}"
            # open(logfile, 'w').close()
            os.unlink(pidfile)

if __name__ == "__main__":
    main()
