string = "HELP!!! Please... right now"

def capitalize(string):
	tmp_list = string.split()
	i = 0
	for item in tmp_list:
		tmp_list[i] = item.capitalize()
		i += 1
	return " ".join(tmp_list)

def rev_this(string):
	return string[::-1]

def stringcases(string):
	upper = string.upper()
	lower = string.lower()

	title = capitalize(string)
	rev = rev_this(string)

	tuple_v4 = (upper, lower, title, rev)
	return tuple_v4



print stringcases(string)