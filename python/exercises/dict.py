my_dict = {'apples': 1, 'bananas': 2, 'coconuts': 3}

string = "I am that I am am am"

def word_count(string):
	return_dict = {}
	sentence = string.split()
	for word in sentence:
		count = sentence.count(word)
		return_dict[word] = count
	print return_dict

word_count(string)

