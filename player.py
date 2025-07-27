import board
import random
import math

# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.
class Player:
	
	def __init__(self, name, depth = 6):
		# If name is X, then it is a maximising player, otherwise it is a minimising player
		self.name = name

		self.depth = depth

		# track the opponent's name
		self.opponent = "O" if self.name == "X" else "X"
	
		self.numExpanded = 0 # Use this to track the number of nodes you expand
		self.numPruned = 0 # Use this to track the number of times you prune 


	# This method evaluates the board and returns a value for the board.
	def evaluate(self, board):
		if board.lastPlay[2] == "X" and board.checkWin():
			return 1
		elif board.lastPlay[2] == "O" and board.checkWin():
			return -1
		else:
			return 0
		

	# this method evaluates the board and returns a value for the board, taking into account the depth of the board, this will help the minimax algorithm to 
	# choose the best move earlier on in the search when using alpha-beta pruning.
	def evaluateWithDepth(self, board, depth):
		if board.lastPlay[2] == "X" and board.checkWin():
			return depth
		elif board.lastPlay[2] == "O" and board.checkWin():
			return -depth
		else:
			return 0
		
	#this method returns an array that holds which columns to check in minimax by ordering of the middle of the board then moving outwards
	def getColumnOrder(self, board):
			middleColumn = board.numColumns // 2

			columnOrder = [middleColumn]  # Start with the middle column

			for distance in range(1, board.numColumns // 2 + 1):
				leftColumn = middleColumn - distance
				if leftColumn >= 0:
					columnOrder.append(leftColumn)

				rightColumn = middleColumn + distance
				if rightColumn < board.numColumns and rightColumn != leftColumn:
					columnOrder.append(rightColumn)

			return columnOrder
	

	# This method implements the minimax algorithm. It should return the evaluation of the board.
	def minimax(self, board, depth, maxPlayer):
		self.numExpanded += 1

		# If the game is over, or we have reached the maximum depth, or there is winner (a terminal node), return the evaluation of the board
		if depth == 0 or board.checkFull() or board.checkWin():
			return self.evaluate(board)

		# If it is the maximising player's turn, return the maximum evaluation of the possible moves
		if maxPlayer:
			maxEval = float('-inf')
			for col in range(board.numColumns):
				if board.addPiece(col, "X"):
					eval = self.minimax(board, depth - 1, not(maxPlayer))
					board.removePiece(col)
					maxEval = max(maxEval, eval)
			return maxEval
		# If it is the minimising player's turn, return the minimum evaluation of the possible moves
		else:
			minEval = float('inf')
			for col in range(board.numColumns):
				if board.addPiece(col, "O"):
					eval = self.minimax(board, depth - 1, not(maxPlayer))
					board.removePiece(col)
					minEval = min(minEval, eval)
			return minEval
		

	# This method implements the minimax algorithm with alpha-beta pruning. It should return the evaluation of the board.
	def minimaxAlphaBeta(self, board, depth, alpha, beta, maxPlayer):
		self.numExpanded += 1

		# If the game is over, or we have reached the maximum depth, or there is winner (a terminal node), return the evaluation of the board
		if depth == 0 or board.checkFull() or board.checkWin():
			return self.evaluateWithDepth(board, depth)

		#start considering moves from the middle of the board outwards
		columnOrder = self.getColumnOrder(board)
		# If it is the maximising player's turn, return the maximum evaluation of the possible moves
		if maxPlayer:
			maxEval = float('-inf')
			for col in columnOrder:
				if board.addPiece(col, "X"):
					eval = self.minimaxAlphaBeta(board, depth - 1, alpha, beta, not(maxPlayer))
					board.removePiece(col)
					maxEval = max(maxEval, eval)
					alpha = max(alpha, eval)
					if beta <= alpha:
						self.numPruned += 1
						break
			return maxEval
		# If it is the minimising player's turn, return the minimum evaluation of the possible moves
		else:
			minEval = float('inf')
			for col in columnOrder:
				if board.addPiece(col, "O"):
					eval = self.minimaxAlphaBeta(board, depth - 1, alpha, beta, not(maxPlayer))
					board.removePiece(col)
					minEval = min(minEval, eval)
					beta = min(beta, eval)
					if beta <= alpha:
						self.numPruned += 1
						break
			return minEval


	# This method gets the best move utilising minimax without alpha-beta pruning. It should return the column that your next piece should be placed in.
	def getMove(self, gameBoard):
		maxPlayer = (self.name == 'X') # True if this player is the maximising player (X)
		bestMove = None
		bestEval = float('-inf')

		# For each possible move, get the evaluation of the board and return the best move (maximum value move)
		for col in range(gameBoard.numColumns):
			if gameBoard.addPiece(col, self.name):
				eval = self.minimax(gameBoard, self.depth, not(maxPlayer))  # 6 is the depth
				gameBoard.removePiece(col)
				if eval > bestEval:
					bestEval = eval
					bestMove = col
		return bestMove


	# This method gets the best move utilising minimax with alpha-beta pruning. It should return the column that your next piece should be placed in.
	def getMoveAlphaBeta(self, gameBoard):
		maxPlayer = (self.name == 'X')
		bestMove = None

		#start considering moves from the middle of the board outwards
		columnOrder = self.getColumnOrder(gameBoard)
		# For each possible move, get the evaluation of the board and return the best move (maximum value move)
		if maxPlayer:
			bestEval = float('-inf')
			for col in columnOrder:
				if gameBoard.addPiece(col, self.name):
					eval = self.minimaxAlphaBeta(gameBoard, self.depth, float('-inf'), float('inf'), not(maxPlayer))
					gameBoard.removePiece(col)
					if eval > bestEval:
						bestEval = eval
						bestMove = col
		#if player is an oppenent player (player used for testing) then get the lowest value move
		else:
			bestEval = float('inf')
			for col in columnOrder:
				if gameBoard.addPiece(col, self.name):
					eval = self.minimaxAlphaBeta(gameBoard, self.depth, float('-inf'), float('inf'), not(maxPlayer))
					gameBoard.removePiece(col)
					if eval < bestEval:
						bestEval = eval
						bestMove = col
		return bestMove
	
	
	