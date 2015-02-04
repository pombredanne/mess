def _total(initial=5, *numbers, **keywords):
    count = initial
    print "Dictionary is",keywords
    print "List is",numbers
    print "Initial is",initial

    for number in numbers:
        count += number
    for key in keywords:
        count += keywords[key]
    return count

print _total(10, 1, 2, 3, vegetables=50, fruits=100)