def add_list(stuff):
  new_stuff = 0
  for i in stuff:
    new_stuff += i
  return new_stuff

def summarize(stuff):
  string = str(stuff)
  result = str(add_list(stuff))
  print "The sum of " + string + " is " + result + "."

add_list([1, 2, 3])
summarize([1, 2, 3])