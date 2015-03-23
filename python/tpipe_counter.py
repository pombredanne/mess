'''
Author: Tiago Baptista
Function: Loops over logfile and updates zabbix
'''
# import time
import subprocess

# logfile = "/var/log/output/tpipes.log"
logfile = "test.file"


class Tpipes:

    def bashing(self, cmd):
        self.cmd = cmd
        self.process = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE)
        self.output = self.process.communicate()[0]
        return self.output.rstrip('\n')

    def updatezabbix(self):

        # Loop through dictionary and update zabbix

        for key in self.tpipedict:
            self.item = "/usr/bin/zabbix_sender -z 10.33.26.165 -s mob-sa-maillogs-L-1-r1 -k " + \
                key + " -o " + str(self.tpipedict[key])
            self.bashing(self.item)

    def logcounter(self, tpipe):
        self.tpipe = tpipe
        self.cmd = "grep -c " + "\'" + self.tpipe + \
            " 0 recieved data for\' " + logfile
        self.count = self.bashing(self.cmd)
        return self.count

    def __init__(self):

        self.tpipedict = {}

        # Generate dictionary as {Tpipe name: value} from 03 to 20

        for counter in list("%02d" % x for x in range(3, 21)):
            self.tpipe = "imsc-INCONT" + counter
            self.tpipedict[self.tpipe] = self.logcounter(self.tpipe)

        print self.tpipedict


def main():
    obj1 = Tpipes()
    obj1.updatezabbix()
    f = open(logfile, "w")
    f.close()


if __name__ == "__main__":
    main()
#    while True:
#        try:
#            main()
#            time.sleep(60)
#        except:
#            break
