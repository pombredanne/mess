# Imports
##################################
import re
import subprocess
import paramiko
import socket
socket.setdefaulttimeout(5)

# Configs
##################################
CONFIG = '/etc/fester.conf'
RED1_servers = ['int1-fester-01', 'int1-fester-02', 'int1-fester-03']
RED3_servers = ['int2-fester-01', 'int2-fester-02', 'int2-fester-03']
ACTIVE_VERSIONS = ['9', '10']
TEMP = '/tmp/test'
LOG = '/tmp/conn_per_version'

# SSH Keys
##################################
key = paramiko.RSAKey.from_private_key_file("/home/f3902293/.ssh/id_rsa")
thread = paramiko.SSHClient()
thread.load_system_host_keys()

class Server:

	def tellsingle(self):
		return self.running

	def demote(self, user_uid, group_uid):
		def result():
			os.setgid(group_uid)
			os.setuid(user_uid)
		return result

	def get_conns(self, server, instance):
		#print "Getting currently active connections for {}: {}".format(server, instance)
		# ssh to server, get netstat -napd | grep 36400 | grep -c EST
		cmd0 = "ssh " + server + " ps aux | grep " + instance
		process = subprocess.Popen(cmd0, preexec_fn=self.demote(3317,3317), stdout=subprocess.PIPE, shell=True)
		pid = process.communicate()[0].split()[1]
		cmd1 = "ssh " + server + " netstat -napd | grep 36400 | grep " + pid + " | grep -c EST"
		process = subprocess.Popen(cmd1, preexec_fn=self.demote(3317,3317), stdout=subprocess.PIPE, shell=True)
		output = process.communicate()[0]
		connections = re.sub('\n', '', output)
		return connections

	def __init__(self, server):

		self.running = {}

		cmd = "ssh " + server + " cat /etc/fester.conf"

		process = subprocess.Popen(cmd, preexec_fn=self.demote(3317,3317), stdout=subprocess.PIPE, shell=True)
		output = process.communicate()[0]

		f = open(TEMP, 'w')
		f.write(output)
		f.close()


		f = open(TEMP, 'r')
		for line in f:
			try:
				version = line.split()[0]
				instance = re.sub(',', '', line.split()[2])
				active_connections = self.get_conns(server, instance)
				self.running[instance] = (version, active_connections)
			except IndexError as e:
				break
		f.close()

class Snapshot(Server):

	def tell(self):
		return "<> I'm a DC running these servers"
		# print dictionary

	def __init__(self, server):
		#print "Initializing {}...".format(server)
		obj = Server.__init__(self, server)

def main():
	f = open(LOG, 'w')
	f.write('')
	f.close()

	RED1 = {}
	RED3 = {}

	for server in RED1_servers:
		RED1[server] = Snapshot(server)

	for server in RED3_servers:
		RED3[server] = Snapshot(server)

	for fester in RED1.keys():
		instance =  RED1[fester].running.keys()
		for i in instance:
			version = RED1[fester].running[i][0]
			active_conns = RED1[fester].running[i][1]
			f = open(LOG, 'a')
			f.write("version: " + version + " " + active_conns + "\n")
	f.close()

	for fester in RED3.keys():
		instance =  RED3[fester].running.keys()
		for i in instance:
			version = RED3[fester].running[i][0]
			active_conns = RED3[fester].running[i][1]
			f = open(LOG, 'a')
			f.write("version: " + version + " " + active_conns + "\n")
	f.close()

	for version in ACTIVE_VERSIONS:
		f = open(LOG, 'r')
		total_conn = 0

		for line in f:
			if version in line.split():
				total_conn += int(line.split()[2])
		f.close()
		f = open(LOG, 'a')
		f.write(version + " = " + str(total_conn) + "\n")
		f.close()
		# print "FOUND " + version + " with " + str(total_conn)


if __name__ == "__main__":
	main()
