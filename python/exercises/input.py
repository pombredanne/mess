leaveout = (',',' ','!','?','.', '#')
something = "Rise,,,,,    to vote!!???#!!!, sir...."
new_something = ""

def cleanup(string,new_string):
	for letter in string:
		if letter in leaveout:
			#print "Taking out >{}<".format(letter)
			pass
		else:
			#print "Leaving {} in".format(letter)
			new_string += letter
	return new_string.lower()

correct_string = cleanup(something,new_something)
#print correct_string


def reverse(correct_string):
	return correct_string[::-1]

def is_palindrome(correct_string):
	return correct_string == reverse(correct_string)

if is_palindrome(correct_string):
   print "Yes, {} is a palindrome".format(something)
else:
    print "No, {} is not a palindrome".format(something)	


