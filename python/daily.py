'''
TO DO:
Pass arguments: 1) Fix up menu function
				2) Run over web service
'''

#Imports
import subprocess
from sys import argv

#Variables
args = len(argv)
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

def _full():
	print "Running for yesterday/today...\n"
	print "########################\n"
	print "Order will be",userDict.keys()
	for name in userDict:
		print "Report for",name
		print "========================================================\n"
		_report(userDict[name],day="2")
		_report(userDict[name],day="1")
		print "========================================================\n"
	
def _main():
	print("Arg options: 1) <Single Name>, 2) menu\n")
	if args == 1:
		_full()
	elif args == 2:
		if argv[1] == "menu":
			print "Select from these guys"
			for name in enumerate(userDict.keys()):
				print name
		elif argv[1] in userDict.keys():
			print "Running for {} only...".format(argv[1])
			print "########################\n"
			print "========================================================\n"
			_report(userDict[argv[1]],day="2")
			_report(userDict[argv[1]],day="1")
			print "========================================================\n"
		else:
			print "You haven't provided a valid option"

#Main
if __name__ == "__main__":
	_main()