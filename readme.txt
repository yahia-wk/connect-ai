The aim of this coursework is to implement and evaluate the minimax algorithm, with and without alpha-beta pruning. Full details are given in the coursework document.

The implementation will be applied to a game called Connect, again described in the coursework document. Locations in the Connect board are indexed by the corresponding row, r, and column, c. Each coordinate (r,c) represents a space on the board, where a piece can be placed (noting that in play gravity determines in which row a piece is positoned). The goal is to have a given number of pieces arranged in a single, unbroken, line. This line can stretch across the board horizontally, vertically or diagonally. Players take it turns to select a column in which to place one of their pieces, and the piece will fall to the lowest numbered row that DOES NOT have a piece in it. For example, suppose that a player places their piece in column 4. If spaces (0,4) and (1,4) are already occupied, then the player’s piece will fall to position (2, 4).

Naturally, Connect has a large state space, and so an efficient minimax algorithm is important.

In this folder, you will find 5 Python files, which are described in the coursework document:

	player.py - This is the file which implements the solution. There is a preamble which explains what is to return from each method. 

	randomPlayer.py - This is a simple opponent to test against that always chooses a random move.

	game.py - This file creates a board, and cycles between the players, requesting their next move. This is the file that is used to actually perform the game.

	board.py - This file contains the class that represents the board, and the methods that are required to play a game of Connect. This file is also commented, as it can be used when implementing the minimax algorithm.

	runGame.py - This is a simple script that will run a game. We can edit this file to create different scenarios to evaluate the solution.

