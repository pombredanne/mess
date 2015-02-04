pattern = """\
 _     _  _     _  _  _  _  _ 
| |  | _| _||_||_ |_   ||_||_|
|_|  ||_  _|  | _||_|  ||_| _|""".splitlines()

query = """\
    _  _  _  _  _  _     _ 
|_||_|| || ||_   |  |  ||_ 
  | _||_||_||_|  |  |  | _|""".splitlines()

split_to_digits = lambda lines: [[line[i:i+3] for line in lines] for i in range(0, len(lines[0]), 3)]
digits, pattern_digits = split_to_digits(query), split_to_digits(pattern)
output = "".join(str(pattern_digits.index(digit)) for digit in digits)
print(output)