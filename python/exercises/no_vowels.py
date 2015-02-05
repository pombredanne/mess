my_list = ['word', 'hello', 'another', 'interesting']
no_vowel_list = []

vowels = ['a', 'e', 'i', 'o', 'u']

def removal(word):
	letter_list = []
	print "Converting ",word
	#Create list from word
	for letter in word:
		letter_list.append(letter)
	print "I've got this list now {} {}".format(len(letter_list), letter_list)

	new_word = vowel(letter_list)
	return new_word

def vowel(word_list):
	for vowel in vowels:
		while True:
			try:
				word_list.remove(vowel)
			except:
				break	
	return word_list



for word in my_list:
	re_done = removal(word)
	no_vowel_word = ""
	for letter in re_done:
		no_vowel_word += letter
	no_vowel_list.append(no_vowel_word.capitalize())

print no_vowel_list

