def sillycase(string):
	print string
	half = len(string)/2
	first = int(round(len(string)/2))
	print "First half is ",string[:first].lower()
  	print "Second half if ",string[half:].upper()

  	final = string[:first].lower() + string[half:].upper()
  	print final




sillycase("aaaaabbbbb")