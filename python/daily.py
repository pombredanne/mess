'''
TO DO:
Pass arguments: 1) Check if single name
				2) Check if "menu", give option to select
				3) Check if "report", run report
				4) Print out usage options on "help"
				5) Run over web service
'''

#Imports
import subprocess
import sys

#Variables
args = len(sys.argv)
userDict = {}
headBashCommand = "ssh mats-sa-incontact-L-1-a ./test.sh"
numFile = '/home/f3902293/numbers'

#Create dictionary
with open(numFile, 'r') as f:
        for line in f:
            (name, num) = line.split()
            userDict[name] = num

#Functions
def _bashing(cmd):
	process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print output
	print "--------------------------------------------------------\n"

def _report(number, day):
	appendBashCommand = headBashCommand + " " + day + " " + number
	_bashing(appendBashCommand)

def _main():
	print "Running for yesterday/today...\n"
	print "########################\n"
	print "Order will be",userDict.keys()
	for name in userDict:
		print "Report for",name
		print "========================================================\n"
		_report(userDict[name],day="2")
		_report(userDict[name],day="1")
		print "========================================================\n"
	
#Main
if __name__ == "__main__":
	_main()