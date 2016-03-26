"""
Class of standard (English) game boards for Peg Solitaire
"""
import numpy


class EnglishBoard(object):
	
	def __init__(self):
		self._peg_array = numpy.ones([7, 7])
		
		#specifics of the English board
		self._peg_array[0:2, 0:2] = -1
		self._peg_array[0:2, 5:7] = -1
		self._peg_array[5:7, 0:2] = -1
		self._peg_array[5:7, 5:7] = -1
		self._peg_array[3, 3] = 0
		
		self._populate_pegs()
	
	def _populate_pegs(self):
		"""Fills in all positive entries with peg numbers"""
		peg_counter = 0
		for i in range(0, self.v_size):
			for j in range(0, self.h_size):
				if self._peg_array[i, j] > 0:
					peg_counter += 1
					self._peg_array[i, j] = peg_counter
	
	
	@property
	def h_size(self):
		return self._peg_array.shape[1]
	
	@property
	def v_size(self):
		return self._peg_array.shape[0]
	
	@property
	def score(self):
		score = 0
		for i in range(0, self.v_size):
			for j in range(0, self.h_size):
				if self._peg_array[i, j] > 0:
					score += 1
		return score
	
	def find_peg_coordinates(self, peg_number):
		"""
		If there is a peg with the given identifier, returns a tuple with the
		coordinates.  Otherwise, returns a tuple with two negatives
		"""
		if peg_number > 0:
			for i in range(0, self.v_size):
				for j in range(0, self.h_size):
					if self._peg_array[i, j] == peg_number:
						return (i, j)
		
		return (-1, -1)
	
	def is_valid_move(self, i_dest, j_dest, i_orig=None, j_orig=None, peg_number=None):
		"""
		Checks to see if the specified move is valid.  A move is specified using
		the destination coordinates and either the origin coordinates or a peg
		identifier.
		"""
		if peg_number == None and (i_orig == None or j_orig == None):
			return False
		
		if not (i_dest in range(0, self.v_size) and j_dest in range(0, self.h_size)):
			return False
		
		if peg_number != None:
			(i_orig, j_orig) = self.find_peg_coordinates(peg_number)
		
		if self._peg_array[i_dest, j_dest] != 0:
			return False
		
		if i_dest == i_orig:
			#horizontal move
			distance = abs(j_dest - j_orig)
			middle = (int(i_dest), int(j_dest + j_orig)/2)
		elif j_dest == j_orig:
			#vertical move
			distance = abs(i_dest - i_orig)
			middle = (int(i_dest + i_orig)/2, int(j_dest))
		else:
			#must be invalid
			return False
		
		if distance != 2:
			return False
		
		if self._peg_array[middle] <= 0:
			return False
		
		return True
	
	def try_move(self, i_dest, j_dest, i_orig=None, j_orig=None, peg_number=None):
		"""
		Executes the specified move if and only if it is valid.  Returns a
		boolean indicating the success of the operation.
		"""
		if not self.is_valid_move(i_dest, j_dest, i_orig, j_orig, peg_number):
			return False
		
		if peg_number == None:
			peg_number = self._peg_array[i_orig, j_orig]
		else:
			(i_orig, j_orig) = self.find_peg_coordinates(peg_number)
		
		if i_dest == i_orig:
			#horizontal move
			middle = (i_dest, min(j_dest, j_orig) + 1)
		elif j_dest == j_orig:
			#vertical move
			middle = (min(i_dest, i_orig) + 1, j_dest)
		else:
			#should never happen; is_valid_move() should catch this case first
			message = "Board.is_valid_move() failed to catch an invalid move."
			raise ValueError(message)
		
		#finally make board changes
		self._peg_array[i_orig, j_orig] = 0
		self._peg_array[middle] = 0
		self._peg_array[i_dest, j_dest] = peg_number
		
		return True
	
	
	def display(self):
		"""
		Prints the board to the command line.
		"""
		#First the header and filler rows
		header = "i\\j||"
		filler = "---++"
		thick_filler = "===++"
		for j in range(0, self.h_size):
			header += "{0: >2d}|".format(j)
			filler += "--+"
			thick_filler += "==+"
		print(header)
		print(thick_filler)
		
		#now fill in the board
		for i in range(0, self.v_size):
			#row number
			row_string = "{0: >3d}||".format(i)
			
			for j in range(0, self.h_size):
				value = int(self._peg_array[i, j])
				if value > 0:
					row_string += "{0: >2d}|".format(value)
				elif value < 0:
					row_string += "XX|"
				else:
					row_string += "  |"
			
			print(row_string)
			print(filler)


def __test():
	test_board = EnglishBoard()
	test_board.display()
	if(test_board.try_move(3, 3, i_orig=1, j_orig=3)):
		print("valid")
	else:
		print("invalid")
	test_board.display()

if __name__ == '__main__':
	__test()
