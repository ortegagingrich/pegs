"""
Contains code for handling an undo record.
"""
import numpy

from board import EnglishBoard
from game import _wait_for_input


class UndoRecord(object):
	
	def __init__(self, length, board):
		assert length > 0
		
		self.length = length
		self.board = board
		
		dimensions = [length, board.v_size, board.h_size]
		self._record_array = numpy.zeros(dimensions)
		self._version_pointer = 0
		self._invalid_pointer = 1
		self._history_pointer = 0
		self._record_array[0, :, :] = numpy.copy(board._peg_array)
	
	def replay(self):
		"""
		Replays through the undo history.
		"""
		print("Replay")
		_wait_for_input()
		
		pointer = self._history_pointer
		self.board._peg_array = numpy.copy(self._record_array[pointer, :, :])
		self.board.display()
		_wait_for_input()
		pointer = (pointer + 1) % self.length
		
		while(pointer != self._invalid_pointer):
			self.board._peg_array = numpy.copy(self._record_array[pointer, :, :])
			self.board.display()
			_wait_for_input()
			pointer = (pointer + 1) % self.length
		
		#restore to final condition
		self.board._peg_array = numpy.copy(self._record_array[self._version_pointer, :, :])
	
	def commit(self):
		"""
		Commits the current state of the board to the undo record
		"""
		#make sure there was actually a change
		if self._identical_states(self.board._peg_array, self._version_pointer):
			return
		
		#do the commit
		self._version_pointer = (self._version_pointer + 1) % self.length
		if self._invalid_pointer == self._history_pointer:
			self._history_pointer = (self._history_pointer + 1) % self.length
		self._invalid_pointer = (self._version_pointer + 1) % self.length
		self._record_array[self._version_pointer, :, :] = numpy.copy(self.board._peg_array)
	
	def undo(self):
		"""
		Attempts an undo.  If there are no further undos in the history, returns
		False; otherwise, returns True.
		"""
		#if board state is identical to the most recent record, go back
		if self._identical_states(self.board._peg_array, self._version_pointer):
			if self._version_pointer != self._history_pointer:
				self._version_pointer = (self._version_pointer - 1) % self.length
				return self.undo()
			else:
				#Cannot undo any farther
				#i.e. identical to last commit and no further history
				return False
		
		#restore board to current version pointer
		self.board._peg_array = numpy.copy(self._record_array[self._version_pointer, :, :])
		return True
	
	def redo(self):
		"""
		Attempts a redo.  If the limit of the history has been reached, returns
		False, otherwise True.
		"""
		#must be identical to undo state
		if not self._identical_states(self.board._peg_array, self._version_pointer):
			return False
		
		#check if there are redos left
		tentative = (self._version_pointer + 1) % self.length
		if tentative == self._invalid_pointer:
			return False
		
		#since there are, restore
		self._version_pointer = tentative
		self.board._peg_array = numpy.copy(self._record_array[self._version_pointer, :, :])
		return True
	
	def _identical_states(self, board_array, pointer):
		array1 = board_array
		array2 = self._record_array[pointer, :, :]
		return (array1 == array2).all()
	
	def _debug_print(self):
		print("version={}".format(self._version_pointer))
		print("invalid={}".format(self._invalid_pointer))
		print("history={}".format(self._history_pointer))
		print(self._record_array)


def __test():
	board = EnglishBoard()
	record = UndoRecord(3, board)
	print record._record_array
	
	_wait_for_input()
	
	_try_command('5 d', board)
	print record._record_array
	board.display()
	
	_wait_for_input()
	
	record.commit()
	print record._record_array
	board.display()
	
	_wait_for_input()
	

if __name__ == '__main__':
	__test()
