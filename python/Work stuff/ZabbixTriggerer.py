'''
Author:	Tiago Baptista (F3902293)
Purpose: Grab host groups from zabbix and send all triggers from all hosts to Online's SOI'
'''
import re
import mysql.connector as sql
import os
import sys
import subprocess

class Triggers:

    def __init__(self):

    	Triggers.traps = []

        Triggers.db = sql.connect(host='mob-sa-zabbix-db-L-1',
                                  user='zabbix',
                                  passwd='9apalm3x',
                                  db='zabbix',
                                  port=3311)

        Triggers.cursor = Triggers.db.cursor()

    @classmethod
    def fetch(self, query):
        self.query = query
        self.cursor.execute(self.query)
        self.rows = self.cursor.fetchall()

        for value, key in enumerate(self.rows):
            print "%s: %s" % (value, key[0])

        try:
        	requestedGroup = input(
        		"\nWhich host group would you like to send traps for?\n\t>> ")
            int(requestedGroup)
            self.hostGroup = self.rows[requestedGroup][0]
        except:
            print "You have not entered a valid option, please try again..."
            self.fetch(self.query)

    @classmethod
    def build(self, tempQuery, triggersQuery):
    	# Build temp table with all hosts belonging to host group
    	self.tempQuery = tempQuery + "'" + self.hostGroup + "'"
    	self.triggersQuery = triggersQuery
    	self.cursor.execute(self.tempQuery)
    	self.db.commit()

    	# Build list of triggers from temp table
    	self.cursor.execute(self.triggersQuery)
    	self.rows = self.cursor.fetchall()

    @classmethod
    def trapper(self):
    	# Build outputs
    	for entry in self.rows:
    		self.hostname = entry[0]
    		self.trigger = entry[1]
    		self.comment = entry[2]
    		if re.search('\{\#(.*?)\}',self.trigger) is not None or 'Template_' in self.hostname:
    			pass
			else:
				line = re.sub('\{HOST.NAME\}',self.hostname,self.trigger)
                self.traps.append(line + " OK " + self.comment + " 0")
        # Send traps

def sender(traps):
	#/usr/bin/snmptrap -v 1 -c RBGU 172.20.116.46 1.3.6.1.4.1.692.5.1 mob-sa-zabbix-app-L-1.fnb.co.za 6 3 - 1.3.6.1.4.1 s "DIGITAL_BANKING OPS s3-banking-syslog-01 OCEP Ebucks avg latency OK EBUCKS - High avg latency (INFO ONLY) 577"
	for trap in traps:
		item = '/usr/bin/snmptrap -v 1 -c RBGU 172.20.116.46 1.3.6.1.4.1.692.5.1 mob-sa-zabbix-app-L-1.fnb.co.za 6 3 - 1.3.6.1.4.1 s \"' + trap + '\"'
		print item
		process = subprocess.Popen(item, shell=True, stdout=subprocess.PIPE)
		output = process.communicate()
		print output

def main():
    getGroupsQuery = "SELECT DISTINCT(name) from groups;"
    tempTableQuery = "CREATE TEMPORARY TABLE poop AS\
						SELECT DISTINCT h.hostid,h.name AS hostname, hg.groupid, g.name\
						FROM hosts h\
						LEFT JOIN hosts_groups hg ON hg.hostid = h.hostid\
						LEFT JOIN groups g ON hg.groupid=g.groupid\
						WHERE g.name = "
    getTriggersQuery = "SELECT h.name AS hostname, t.description, t.comment\
						FROM hosts h, items i\
							LEFT JOIN functions f ON f.itemid=i.itemid\
							LEFT JOIN triggers t ON t.triggerid=f.triggerid AND t.status='TRIGGER_STATUS_ENABLED'\
						WHERE h.hostid=i.hostid AND h.name IN\
							(SELECT DISTINCT(hostname) FROM poop)\
						AND t.triggerid is not NULL AND t.description not like 'DIGITAL_BANKING CDM_SYS%';"

    obj1 = Triggers()
    obj1.fetch(getGroupsQuery)
    obj1.build(tempTableQuery, getTriggersQuery)
    obj1.trapper()
    sender(obj1.traps)
    obj1.db.close()

if __name__ == '__main__':
    main()
