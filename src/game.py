"""
Functions for executing a game.
"""
import sys

from board import EnglishBoard


def run():
	"""Executes an interactive game"""
	board = EnglishBoard()
	
	while(board.move_possible()):
		print("Pegs Remaining: {}".format(board.score))
		board.display()
		try:
			command = _get_command()
			_try_command(command, board)
		except Exception as exception:
			print(exception)
			_wait_for_input()
	print('\n\nNo more moves are possible.')
	print('Final Score: {}'.format(board.score))
	board.display()
	_wait_for_input()


def _quit():
	sys.exit(0)

def _wait_for_input():
	raw_input('Press Enter to continue . . .')

def _get_command():
	prompt = 'Enter a command: (Use "help" for a list of command formats) $ '
	return raw_input(prompt)

def _print_help():
	print('Move commands are of the form:')
	print('\t"[peg_number] to [new_i] [new_j]"')
	print('\t"[old_i] [old_j] to [new_i] [new_j]')
	print('\t"[peg_number] [up/down/left/right/u/d/l/r]"')
	print('\t"[old_i] [old_j] [up/down/left/right/u/d/l/r]"')
	print('"help" for help.')
	print('"quit" to quit the game.')
	_wait_for_input()

def _try_command(command, board):
	"""
	Attempts to parse and execute the specified command for the given board.
	Raises an exception if either the command parsing fails, or if the move is
	invalid.
	Commands are strings of the form:
		'[peg_number] to [new_i] [new_j]'
		'[old_i] [old_j] to [new_i] [new_j]'
		'[peg_number] [up/down/left/right]'
		'[old_i] [old_j] [up/down/left/right]'
	"""
	tokens = command.split(' ')
	n_tokens = len(tokens)
	
	if 'help' in tokens:
		_print_help()
		return
	elif 'quit' in tokens:
		_quit()
	
	parse_fail = Exception('Invalid command: "{}"'.format(command))
	move_fail = Exception('Invalid Move: "{}"'.format(command))
	
	#try parsing
	try:
		if n_tokens > 3:
			#to command
			i_dest = int(tokens[-2])
			j_dest = int(tokens[-1])
			if n_tokens == 4:
				peg_number = int(tokens[0])
				i_orig = None
				j_orig = None
			elif n_tokens == 5:
				peg_number = None
				i_orig = int(tokens[0])
				j_orig = int(tokens[1])
			else:
				raise parse_fail
		else:
			#shortcut command
			if n_tokens == 2:
				peg_number = int(tokens[0])
				(i_orig, j_orig) = board.find_peg_coordinates(peg_number)
			elif n_tokens == 3:
				peg_number = None
				i_orig = int(tokens[0])
				j_orig = int(tokens[1])
			else:
				raise parse_fail
				
			#find destination
			i_dest = i_orig
			j_dest = j_orig
			option = tokens[-1]
			if option in ['up', 'u']:
				i_dest -= 2
			elif option in ['down', 'd']:
				i_dest += 2
			elif option in ['left', 'l']:
				j_dest -= 2
			elif option in ['right', 'r']:
				j_dest += 2
			else:
				raise parse_fail
	except:
		raise parse_fail
	
	#try the move
	result = board.try_move(i_dest, j_dest, i_orig, j_orig, peg_number)
	if not result:
		raise move_fail


def __test():
	board = EnglishBoard()
	winning_commands = [
		"1 3 to 3 3",
		"8 to 2 3",
		"0 2 down",
		"3 left",
		"16 up",
		"3 down",
		"27 up",
		"20 right",
		"7 d",
		"23 l",
		"7 r",
		"25 l",
		"32 u",
		"30 r",
		"17 d",
		"30 u",
		"6 d",
		"13 l",
		"26 u",
		"8 r",
		"26 l",
		"25 l",
		"25 u",
		"25 r",
		"25 r",
		"25 d",
		"25 l",
		"5 r",
		"28 u",
		"27 r",
		"5 l"
	]
	for command in winning_commands:
		_try_command(command, board)
	assert board.score == 1, 'Winning moves failed to win.'
	board.display()

if __name__ == '__main__':
	__test()
