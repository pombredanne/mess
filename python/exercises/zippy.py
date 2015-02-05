# combo(['swallow', 'snake', 'parrot'], 'abc')
# Output:
# [('swallow', 'a'), ('snake', 'b'), ('parrot', 'c')]
# If you use list.append(), you'll want to pass it a tuple of new values.
# Using enumerate() here can save you a variable or two.
one = ['swallow', 'snake', 'parrot']
two = 'abc'
three = '123'

def combo(*tup):
	print tup[0]
	print tup[1]

	final_list = []
	for index, field in enumerate(tup[0]):
		#print '{} {}'.format(*field)
		print field
		print tup[1][index]
		

		#for value in field[1]:
			#print "Value is ",value



combo(one, two)