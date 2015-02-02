import random

def gen_number():
	#Generate random number
	number = random.randrange(0,10)
	return number

def main():
	guess = input("Pick a number 'tween 1 and 10: ")
	number = gen_number()
	print "Using random # ",number
	guesses = 3
	while guesses > 1:
		if guess < number:
			guesses -= 1
			print "You have {:d} guesses left. It's too low, guess again: ".format(guesses),
			guess = input("")
			continue
		elif guess > number:
			guesses -= 1
			print "You have {:d} guesses left. It's too high, guess again: ".format(guesses),
			guess = input("")
			continue
		else:
			print "You are the winrar!"
		break
	print "Out of guesses"




if __name__ == '__main__':
	main()