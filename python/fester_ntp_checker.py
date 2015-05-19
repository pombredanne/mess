'''
Author: Tiago Baptista
Purpose: Ensures NTP offset across all festers is under 150ms, runs a manual update if unsynchronized/behind.

TO DO:
1) Switch to fabric as a replacement for subprocess
2) Use setuid/setgid instead of su -l loguser (it's cleaner)
3) Daemonize better
'''

import time
import subprocess
import re
import os

SERVERS = ['s3-fester-01', 's3-fester-02', 's3-fester-03', 's3-fester-04', 's3-fester-05', 's3-fester-06', 's3-fester-07',
           's4-fester-01', 's4-fester-02', 's4-fester-03', 's4-fester-04', 's4-fester-05', 's4-fester-06', 's4-fester-07']

class Zabbix:

    def trap_ntp(self, value):
        self.value = value
        self.alert_ntp = '/usr/sbin/zabbix_sender -z 192.168.35.151 -s s3-banking-syslog-01 -k alert.ntp ' + \
            str(self.value)

        self.process = subprocess.Popen(
        	self.alert_ntp, shell=True, stdout=subprocess.PIPE)
        self.output = self.process.communicate()[0]
        
        print self.output

    def trap_daemon(self, value):
        self.value = value
        self.alert_daemon = '/usr/sbin/zabbix_sender -z 192.168.35.151 -s s3-banking-syslog-01 -k alert.daemon ' + \
            str(self.value)

        self.process = subprocess.Popen(
        	self.alert_daemon, shell=True, stdout=subprocess.PIPE)
        self.output = self.process.communicate()[0]

        print self.output

def demote(user_uid, group_uid):
	def result():
		os.setgid(group_uid)
		os.setuid(user_uid)
	return result

def manual(host):

    cmd = 'ssh ' + host + ' sudo /usr/sbin/ntpdate -u s1-noc-01'

    process = subprocess.Popen(cmd, preexec_fn=demote(3317,3317),stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0]

def get_stats(host):

	cmd = "ssh " + host + " /usr/sbin/ntpq -p | grep '*' | awk '{print $9}'"

	process = subprocess.Popen(cmd, preexec_fn=demote(3317, 3317), stdout=subprocess.PIPE, shell=True)
	output = process.communicate()[0]

	return re.sub('\n','',output)


def main():

	results = []

	for fester in SERVERS:
		offset = re.sub('-', '', get_stats(fester))

		try:
			if float(offset) > 150:
				print "Need to manual for {}. Offset at {}".format(fester, offset)
				# Stupid older versions need different formatting
				# print "Need to manual for %s. Offset at %s" % (fester, offset)
				results.append('1')
				manual(fester)
			else:
				results.append('0')
				continue
		except ValueError:
			# Not appending to results in case ntp doesn't work at all, rather just do a manual update every time.
			results.append('0')
			print "Need to manual as it doesn't look like ntp is working for {}".format(fester)
			# Older python version formatting
			# print "Need to manual as it doesn't look like ntp is working for %s" % fester
			manual(fester)

	if reduce(lambda x, y: int(x) + int(y), results) > 1:
		print "Alerting"
		# Zabbix().trap_ntp('1')
	else:
		print "Clearing"
		# Zabbix().trap_ntp('1')



if __name__ == "__main__":
	while True:
		try:
			main()
			time.sleep(30)
		except:
			break
