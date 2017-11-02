# Author: Tiago Baptista
# Purpose: Update gomez thread counters on Zabbix

# Imports
#########
# from datetime import datetime as dt
import subprocess
import re
import os
import sys

IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    from Queue import Queue
else:
    from queue import Queue

from threading import Thread
import time

# Static variables
##################
#logfile = "/var/log/output/gomezthread.log"
logfile = "/home/f3902293/gomezthread_tmp.log"  # change to argv[1]
CHECK = ["Queue Size", "Active Size", "Completed", "DISCONNECTING"]
gomez_hosts = ['s3-gomez-02', 's4-gomez-02']
zabbix_serv = '172.16.2.112'
rundir = "/home/f3902293/"

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Helper functions
##################


def zabbix_sender(entry):
    # Simple function to format single line to send to zabbix

    host = entry.split()[0]
    node = "node_" + str(entry.split()[1])
    desc = entry.split()[2]
    value = entry.split()[3]
    item = "/usr/bin/zabbix_sender -z " + zabbix_serv + " -s " + \
        host + " -k " + node + "_" + desc + " -o " + str(value)
    #process = subprocess.Popen(item, shell=True, stdout=subprocess.PIPE)
    #output = process.communicate()
    #print item
    time.sleep(5 / 1000.0)


def update_zabbix(list):
    # Loop through full object and thread zabbix sender

    inittime = round(time.time() * 1000)
    pool = ThreadPool(16)

    for item in list:
        pool.add_task(zabbix_sender, item)

    pool.wait_completion()
    stoptime = round(time.time() * 1000)
    print("%s || [INFO] Zabbix processing took %s ms") % (now, str(stoptime - inittime))


# Threading class
#################
class Worker(Thread):
    """ Execute tasks from given queue """

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print("%s || [ERROR] %s") % (now, e)
            finally:
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming from queue """

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def map(self, func, arg_list):
        for args in arg_list:
            self.add_task(func, args)

    def wait_completion(self):
        self.tasks.join()


class Gomez:
    """ Builds gomez object from log files """

    def __init__(self):
        inittime = round(time.time() * 1000)
        Gomez.full = []
        Gomez.disconnects = {}

        # Gotta find a cleaner way to handle multiple nodes and hosts
        # Format is {'gomez host':
        #       {
        #       node1: value, node2: value
        #       }
        #       }
        for gomez in gomez_hosts:
            Gomez.disconnects[gomez] = {'1': 0, '2': 0}
            Gomez.full.append(gomez + ' 1 DISCONNECTING 0')
            Gomez.full.append(gomez + ' 2 DISCONNECTING 0')

        self.f = open(logfile, "r")

        for line in self.f:
            gomeznode = re.search('FNB_GOMEZ_NODE(.+?)_MSG', line).group(1)
            hostname = line.split()[3]
            for counter in CHECK:
                if counter in line and counter != 'DISCONNECTING':
                    poolSize = re.search(
                        counter + '(.*?)\[(.+?)\]', line).group(2)
                    Gomez.full.append(
                        hostname + ' ' +
                        gomeznode + ' ' +
                        counter.split()[0] + ' ' +
                        poolSize)
                elif counter in line and counter == 'DISCONNECTING':
                    try:
                        currentHostDict = Gomez.disconnects[hostname]
                        currentHostDict[gomeznode] += 1
                        Gomez.full.append(
                            hostname + ' ' +
                            gomeznode + ' ' +
                            counter.split()[0] + ' ' +
                            str(currentHostDict[gomeznode]))
                    except Exception as e:
                        print("%s || [ERROR] %s") % (now, e)
        self.f.close()
        stoptime = round(time.time() * 1000)

        print("%s || [INFO] File processing took %s ms") % (now, str(stoptime - inittime))
        print("%s || [INFO] Total entries to send: %s") % (now, len(Gomez.full))
        #open(logfile, 'w').close()


# Main
#######

def main():
    print "============================================"
    print("%s || [INFO] Initializing...") % (now)
    pid = str(os.getpid())
    pidfile = rundir + "/gomezmonitor.pid"

    if os.path.isfile(pidfile):
        print("%s || [ERROR] Found an existing pid file: %s") % (now, pidfile)
        sys.exit()
    else:
        file(pidfile, 'w').write(pid)

        if os.stat(logfile).st_size == 0:
            print("%s || [ERROR] Log file is empty, exiting...") % now
            os.unlink(pidfile)
            sys.exit()
        else:
            obj1 = Gomez()
            update_zabbix(obj1.full)
            print("%s || [INFO] %s") % (now, str(obj1.disconnects['s3-gomez-02']))
            print("%s || [INFO] %s") % (now, str(obj1.disconnects['s4-gomez-02']))

            #open(logfile, 'w').close()
            os.unlink(pidfile)


if __name__ == "__main__":
    main()
