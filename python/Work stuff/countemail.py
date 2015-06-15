'''
Purpose: Count email logs, send to zabbix every second
'''

import subprocess
import time


class EmailLogs:
	
    def bashing(self, cmd):
        self.cmd = cmd
        self.process = subprocess.Popen(
            self.cmd, shell=True, stdout=subprocess.PIPE)
        self.output = self.process.communicate()[0]
        return self.output

    def updatezabbix(self):
        print self.item
        self.bashing(self.item)

    def __init__(self):
        self.count = self.bashing("grep -c Sending /var/log/output/email.log")
        self.item = "/usr/sbin/zabbix_sender -z 172.18.210.5 -s lt1-incontactgrandmama-01 -k customcat[/tmp/email] -o " + str(
            self.count)

    def finishup(self):
        f = open("/var/log/output/email.log", "w")
        f.close()


def main():
    obj1 = EmailLogs()
    obj1.updatezabbix()
    obj1.finishup()

if __name__ == "__main__":
    while True:
        try:
            main()
            time.sleep(1)
        except:
            break
