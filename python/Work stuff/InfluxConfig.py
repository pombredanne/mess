'''
Config builder class for InfluxDB
'''
import os
import sys
import ConfigParser

class InfluxConfig(object):

	'''
	Defines the main config and sections explicitly
	'''

	def __init__(self):
		super(InfluxConfig, self).__init__()
		self.CONFIG_FILE = "config.ini"
		self.INFLUX_DB_CONFIG = "influx_db_config"
		self.LOGFILES = "logfiles"
		self.PROCESSORS = "processors"
		self.RESPONSE_LOGS = "response_logs"

	@property
	def __CONFIG_FILE(self):
		return self.CONFIG_FILE

	#@property
	#def __CONFIG_SECTIONS(self):
	#	return self.CONFIG_SECTIONS


class ConfigBuilder(InfluxConfig):

	def __init__(self):
		super(ConfigBuilder, self).__init__()
		self.buildConfig()

	def buildConfig(self):
		print("Initializing with %s") % self.CONFIG_FILE
		self.config = ConfigParser.ConfigParser()

		if not os.path.isfile(self.CONFIG_FILE):
			print("ERROR! No config.ini file found!")
			sys.exit()
		else:
			self.config.read(self.CONFIG_FILE)
			#self.CONFIG_SECTIONS = self.config.sections()

			for section in self.config.sections():
				self.configMap(section)

	def configMap(self, section):
		self.sectionDict = {}
		self.options = self.config.options(section)

		for option in self.options:
			try:
				sectionDict[option] = self.config.get(section, option)
				


