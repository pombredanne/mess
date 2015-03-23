'''
Author: Tiago Baptista
Purpose: Update zabbix with 3 counters from log file.

TO DO:
1) Cater for multiple instances
'''

import subprocess
import re

# logfile = "/var/log/output/buffer.log"
logfile = "test.file"
CHECK = ["size", "max", "avg", "tasks"]


class Counter:

    def __init__(self):
        with open(logfile, "r") as self.f:
            Counter.lst = self.f.readline().split()
        self.CHECK = CHECK

        while len(Counter.lst) != 4:
            for word in Counter.lst:
                if word.split("[")[0] in self.CHECK:
                    continue
                else:
                    Counter.lst.remove(word)
        self.f.close

    @classmethod
    def create_vars(self):
        self.dict = {}
        for field in self.lst:
            name = field.split("[")[0]
            value = re.sub('[^0-9]', '', field)
            self.dict[name] = value


def update_zabbix(dict):
    for key in dict:
        value = dict[key]
        item = "/usr/sbin/zabbix_sender -z 172.18.210.5 -s lt1-fester-01 -k auditbuffer." + key + " -o " + str(value)
        process = subprocess.Popen(item, shell=True, stdout=subprocess.PIPE)
        output = process.communicate()
        print output


def main():
    obj1 = Counter()
    obj1.create_vars()
    update_zabbix(obj1.dict)
    open(logfile, 'w').close()


if __name__ == "__main__":
    main()
