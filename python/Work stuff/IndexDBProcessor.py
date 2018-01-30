'''
Author: Tiago Baptista
Purpose: Parse raw index logs and split them out into relevant tables

TODO: Check that tomorrows tables have been created, create if not
'''

import os
import re
import sys
import MySQLdb
import argparse
from datetime import datetime

now = datetime.now().strftime('%Y-%h-%d %H:%M:%S')


class Index:
        def __init__(self, date):
            self.date = date
            self.tables = ['index_raw_logs_']
            if date == 'today':
                self.date = datetime.now().strftime('%Y%m%d')

            self.tables[0] = self.tables[0] + self.date
            self.startDB(self.tables)

        def startDB(self, tbl):
            self.tbl = tbl
            db = MySQLdb.connect(host='localhost',
                                 user='root',
                                 passwd='shark',
                                 db='index_logs',
                                 port=3311)
            query = "SELECT pkey,rawlog FROM %s WHERE processed = '0';" % self.tbl[0]
            c = db.cursor()
            c.execute(query)
            rows = c.fetchall()
            self.processRows(rows, c, self.date)
            delete_query = "DELETE FROM %s WHERE processed = '1';" % self.tbl[0]
            c.execute(delete_query)
            db.commit()
            db.close()

        def convertDate(self, timestamp):
            try:
                self.timestamp = int(timestamp)
                converted = datetime.fromtimestamp(
                    self.timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                #print("ERROR: Exception in convertDate(): %s") % e
                converted = 0
            return converted

        def processRows(self, rows, c, tbldate):
            self.rows = rows
            for entry in self.rows:
                self.dict = {}
                line = entry[1]
                try
:                    # These 3 are always the same
                    self.dict['datetime'] = line.split()[1] + " " + line.split()[2].split(',')[0]
                    self.dict['host'] = line.split()[0].split('_')[1]
                    self.dict['thread'] = re.search('Receiver\[(.+?)\]', line).group(1)
                    if ('PAIRED' in line) or ('MOBI SESSION' in line):
                        self.dict['ip'] = re.search('Receiver\[(.+?)\]', line).group(1).split(':')[0]
                        self.dict['username'] = re.search('Username\[(.+?)\]', line).group(1)
                        self.dict['ucn'] = re.search('Ucn\[(.+?)\]', line).group(1)
                        self.dict['deviceid'] = re.search('DeviceID\[(.+?)\]', line).group(1)
                        self.dict['device_nick'] = re.search('DeviceNickname\[(.+?)\]', line).group(1)
                        self.dict['country'] = re.search('Country\[(.+?)\]', line).group(1)
                        self.dict['platform'] = re.search('Platform\[(.+?)\]', line).group(1)
                        self.dict['model'] = re.search('Model\[(.+?)\]', line).group(1)
                        self.dict['version'] = re.search('Version\[(.+?)\]', line).group(1)
                        connectNum = re.search('Connect\[(.+?)\]', line).group(1)
                        self.dict['connect'] = connectNum if connectNum.isdigit() else 0
                        # These need unixtimestamp converted to timestamp
                        self.dict['firsttrustedfin'] = self.convertDate(re.search('FirstTrustedFinancial\[(.+?)\]', line).group(1))
                        self.dict['initiated'] = self.convertDate(re.search('Initiated\[(.+?)\]', line).group(1))
                        self.dict['linked'] = self.convertDate(re.search('Linked\[(.+?)\]', line).group(1))
                        self.dict['lastlogon'] = self.convertDate(re.search('LastLogon\[(.+?)\]', line).group(1))
                        table = 'index_paired_logs_' + tbldate
                    elif 'Attempted' in line:
                        self.dict['deviceid'] = re.search('Device\[(.+?)\]', line).group(1)
                        self.dict['username'] = re.search('username\[(.+?)\]', line).group(1)
                        table = 'index_linking_logs_' + tbldate
                    elif 'ENTRY' in line:
                        self.dict['gps_enable'] = 1 if 'true' in re.search('enabled\=\"(.+?)\"', line).group(1) else 0
                        self.dict['device'] = re.search('device\=\"(.+?)\"', line).group(1)
                        self.dict['os'] = re.search('os\=\"(.+?)\"', line).group(1)
                        self.dict['platform'] = re.search('platform\=\"(.+?)\"', line).group(1)
                        self.dict['latitude'] = re.search('latitude\=\"(.+?)\"', line).group(1)
                        self.dict['longitude'] = re.search('longitude\=\"(.+?)\"', line).group(1)
                        del self.dict['host']
                        table = 'index_gps_logs_' + tbldate
                    else:
                        print 'Something went wrong'
                        continue
                try:
                    columns = ', '.join(self.dict.keys())
                    placeholders = '%(' + ')s, %('.join(self.dict.keys()) + ')s'
                    insert_query = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, placeholders)
                    update_query = "UPDATE %s set processed = 1 where pkey = %s" % (self.tbl[0], entry[0])
                    c.execute(insert_query, self.dict)
                    c.execute(update_query)
                except Exception as e:
                    print("%s || ERROR: Exception in query update: \n%s") % (now, e)
                    continue
            self.now = datetime.now().strftime('%Y-%h-%d %H:%M:%S')
            print("%s || Successfully Updated %s rows.") % (self.now, len(self.rows))


def main():
        pid = str(os.getpid())
        pidfile = "/tmp/indexprocessor.pid"
        if os.path.isfile(pidfile):
                print("Found an existing pid file: %s") % pidfile
                sys.exit()
        else:
                file(pidfile, 'w').write(pid)

                try:
                    a = argparse.ArgumentParser()
                    a.add_argument('--date', required=True)
                    date = vars(a.parse_args()).values()[0]
                    obj1 = Index(date)
                    os.unlink(pidfile)
                    sys.exit()
                except Exception as e:
                        print("ERROR: Exception in main(): %s") % e
                        os.unlink(pidfile)
                        sys.exit()

if __name__ == "__main__":
        main()
