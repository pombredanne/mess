#mylist = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
import random

#times = 5

#def nchoice(alist, times):
#	final_list = []
#	tries = 0
#	while tries < times:
#		final_list.append(random.choice(alist))
#		tries += 1
#	return final_list


DUNGEON = [(0, 0), (0, 1), (0, 2),
		   (1, 0), (1, 1), (1, 2),
		   (2, 0), (2, 1), (2, 2)]


def get_location():
	# Randomize door, monster and player locations
	monster = random.choice(DUNGEON)
	player = random.choice(DUNGEON)
	door = random.choice(DUNGEON)
	if monster == door or player == monster or door == player:
		get_location()
	return player, monster, door


def move_player(player, move):
	x, y = player

	if move == 'LEFT':
		y -= 1
	elif move == 'RIGHT':
		y += 1
	elif move == 'UP':
		x -= 1
	elif move == 'DOWN':
		x += 1
	return x, y

def get_moves(player):
	moves = ['LEFT', 'RIGHT', 'DOWN', 'UP']
	if player[0] == 0:
		moves.remove('UP')
	if player[0] == 2:
		moves.remove('DOWN')
	if player[1] == 0:
		moves.remove('LEFT')
	if player[1] == 2:
		moves.remove('RIGHT')
	return moves

def draw_map(player):
	print " _ _ _ _ "
	tile = '|{}'
	for idx, cell in enumerate(DUNGEON):
		if idx in [0, 1, 3, 4, 6, 7]:
			if cell == player:
				print tile.format('X'),
			else:
				print tile.format('_'),
		else:
			if cell == player:
				print tile.format('X')
			else:
				print tile.format('_|')

def main():
	print "Welcome! Enter QUIT to leave"
	player, monster, door = get_location()
	#print "Door is {}, Player is {}, Monster is {}".format(door, player, monster)
	draw_map(player)
	while True:
		allowed = get_moves(player)
		print allowed
		move = raw_input("Where to next?> ").upper()

		if move == 'QUIT':
			break
		if move in allowed:
			player = move_player(player, move)
			draw_map(player)
		else:
			print "**OUCH**"
			continue

		if player == door:
			print "You're out!"
			break
		elif player == monster:
			print "You died!"
			break

main()

#if __name__ == __main__:
#	main()
