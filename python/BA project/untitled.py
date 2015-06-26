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
TEMP = '/tmp/test'

# SSH Keys
##################################
key = paramiko.RSAKey.from_private_key_file("/home/f3902293/.ssh/id_rsa")
thread = paramiko.SSHClient()
thread.load_system_host_keys()

class Server:

	def tellsingle(self):
		return self.running

	def get_conns(self, server, instance):
		# print "Getting currently active connections for {}: {}".format(server, instance)
		# ssh to server, get netstat -napd | grep 36400 | grep -c EST
		#process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		connections = 12
		return connections

	def __init__(self, server):

		self.running = {}

		cmd = "ssh " + server + " cat /etc/fester.conf"

		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		output = process.communicate()[0]

		f = open('/tmp/test', 'w')
		f.write(output)
		f.close()


		with open(TEMP, 'r') as f:
			for line in f:
				try:
					version = line.split()[0]
					instance = re.sub(',', '', line.split()[2])
					active_connections = self.get_conns(server, instance)
					self.running[instance] = (version, active_connections)
				except IndexError as e:
					print "ERROR: {}".format(e)



class Snapshot(Server):

	def tell(self):
		return "<> I'm a DC running these servers"
		# print dictionary

	def __init__(self, server):
		print "Initializing {}...".format(server)
		obj = Server.__init__(self, server)


def main():

	RED1 = {}
	RED3 = {}

	for server in RED1_servers:
		RED1[server] = Snapshot(server)

	print RED1

	print RED1['int1-fester-01'].running
	print RED1['int1-fester-02'].tellsingle()
	#print RED1.dict
	#RED3 = Snapshot(RED3_servers)
	#print RED3.dict

if __name__ == "__main__":
	main()
