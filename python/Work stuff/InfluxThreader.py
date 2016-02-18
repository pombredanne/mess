'''
Threader helper
'''

from influxdb import InfluxDBClient
from datetime import datetime as dt
import threading
import time
'''
def startClient(dbHost, dbPort, data):
    client = InfluxDBClient(host=dbHost, port=dbPort, database='responsetimes')
'''
class InfluxThreader:

	def __init__(self, dbhost, dbport, data):
		self.client = InfluxDBClient(host=dbhost, port=dbport, database='responsetimes')
		self.data = data
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()

	def run(self):
		#while True:
		threadID = threading.currentThread().name
		now = str(dt.now())
		length = len(self.data)
		try:
			started = int(round(time.time() * 1000))
			print "%s || %s || Inserting %s data points..." % (now, threadID, length)
			#catch response below
			self.client.write_points(self.data)
			finished = int(round(time.time() * 1000)) - started
			print "%s || %s || InfluxDB.write_points call took %sms" % (now, threadID, str(finished))
		except Exception as e:
			print "%s || %s || ERROR in InfluxThreader(): %s" % (now, threadID, e)
			pass