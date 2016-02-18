'''
Author: Tiago Baptista
Purpose: Extract email addresses from mail logs for faster reporting
'''

import os
import re
import sys
import MySQLdb
import argparse
from datetime import datetime

now = datetime.now().strftime('%Y-%h-%d %H:%M:%S')

class Mail:
	
        def __init__(self, date):
        	self.tables = ['logs', 'logs_status']
        	
        	if date == 'today':
        		self.startDB(self.tables)
    		else:
    			self.tables[0] = self.tables[0] + date
    			self.tables[1] = self.tables[1] + '_' + date
    			self.startDB(self.tables)

        def startDB(self, tbl):
		self.tbl = tbl
		db = MySQLdb.connect(host='localhost', user='admin', passwd='shark', db='mail_logs', port=3311)

		# First query is for message table, second is for status table
		query = "SELECT seq, msg FROM %s WHERE processed='0';" % self.tbl[0]
		queryStatus = "SELECT pkey, log FROM %s WHERE email_address is NULL;" % self.tbl[1]

		# Store both queries in memory (might be a better way of doing this...)
		c = db.cursor()
		c.execute(query)
		rowsLogs = c.fetchall()
		c.execute(queryStatus)
		rowsStatus = c.fetchall()

		# Update both tables
		self.processRows(rowsLogs, c, self.tbl[0])
		self.processRows(rowsStatus, c, self.tbl[1])

		# Check for duplicates and delete
		duplicate_query = "SELECT seq FROM %s GROUP BY msg HAVING count(msg) > 1" % self.tbl[0]
		c.execute(duplicate_query)
		rowsDuplicates = c.fetchall()
		for item in rowsDuplicates:
			seq = item[0]
			delete_query = "DELETE FROM %s WHERE seq = %s" % (self.tbl[0], seq)
			c.execute(delete_query)

		db.commit()
		db.close()

        def processRows(self, rows, c, tbl):

        	self.rows = rows

        	for line in self.rows:
        		msgID = re.sub(":", "", line[1].split()[0])
        		key = line[0]

        		if 'status' not in tbl:
        			email = re.search(r'to\=\<(.*)\> proto', line[1]).group(1)
        			update_query = "UPDATE %s SET email_address = \"%s\", processed = 1, msg_id = \"%s\" WHERE seq = %s" % (tbl, email, msgID, key)
        		else:
        			email = re.search(r'to\=\<(.*)\>, [ro]', line[1]).group(1).split('>')[0]
        			status = re.search(r'status\=(.*)\ \(', line[1]).group(1).split()[0]
    				update_query = "UPDATE %s SET email_address = \"%s\", msg_id = \"%s\", status = \"%s\" WHERE pkey = %s" % (tbl, email, msgID, status, key)

			try:
				c.execute(update_query)
			except Exception as e:
				print("%s || ERROR: Exception in query update: \n%s") % (now, e)
				continue

		print("%s || Successfully Updated %s rows in %s.") % (now, len(self.rows), tbl)

        def matchUpTables(self, rows, c):
        	self.query = "SELECT pkey, "


def main():
        pid = str(os.getpid())
        pidfile = "/tmp/mailprocessor_tmp.pid"
        if os.path.isfile(pidfile):
                print("Found an existing pid file: %s") % pidfile
                sys.exit()
        else:
                file(pidfile, 'w').write(pid)

                try:
            	    a = argparse.ArgumentParser()
                    a.add_argument('--date', required=True)
                    date = vars(a.parse_args()).values()[0]
                    obj1 = Mail(date)
                    os.unlink(pidfile)
                    sys.exit()
                except Exception as e:
                        print("ERROR: Exception in main(): %s") % e
                        os.unlink(pidfile)
                        sys.exit()

if __name__ == "__main__":
        main()

