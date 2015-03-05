lines = [1, 2, 3, 4, 5]

# lambda creates a function in one line
lambda_map = lambda x: x + 1
lambda_filter = lambda x: x % 2 == 1
lambda_reduce = lambda x, y: x + y

# map applies a function to every item in an iterable
print map(lambda_map, lines)
# will return [2, 3, 4, 5, 6]

# filter returns results only if test returns True over an iterable
print filter(lambda_filter, lines)
# will return [1, 3, 5] because the remainder is the value being tested

# reduce applies a 2 variable function to an iterable sequentially until
# it returns a single value
print reduce(lambda_reduce, lines)
# will return 15

# next returns the next item in an iterable
print next(line for line in lines if line == 1)
# returns the value of line where the condition is met
