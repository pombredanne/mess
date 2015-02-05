# combo(['swallow', 'snake', 'parrot'], 'abc')
# Output:
# [('swallow', 'a'), ('snake', 'b'), ('parrot', 'c')]
# If you use list.append(), you'll want to pass it a tuple of new values.
# Using enumerate() here can save you a variable or two.
one = ['swallow', 'snake', 'parrot']
two = 'abc'
three = '123'
my_dict = {'name': 'Tiago', 'surname': 'Baptista', 'work': 'FNB'}


def combo(*tup):
	final_list = []
	iterate = len(tup)

	for index, field in enumerate(tup[0]):
		#print '{}: {}'.format(*field)

		to_append = (field, tup[1][index])
		final_list.append(to_append)
		#print final_list
		

		#for value in field[1]:
			#print "Value is ",value



combo(one, two, three)

def dict_test(one):
	for step in enumerate(one):
		print '{}: {}'.format(*step)


dict_test(one)


#Items() converts dict entries into keys:
for key, value in my_dict.items():
	#print '{}: {}'.format(key.title(), value)
	#print key

