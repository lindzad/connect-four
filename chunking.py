#7 columns of 6 rows,
#starts in bottom left corner.

"""
chunking makes moves for any player
maybe do by dictionary with board val and number of, then length to see how many tyoes there are
if len 2 and one is -1, add the move

add way to sort moves by num_full, and then by player for specifc player

when have priority list, check for validity, and if not go on. 
check if board with new value would make the other player win
add to list of dont move there
if nothing, go random as long as not on no put list 
"""




#check by chunking
from logic import *

class Move(object):
	def __init__(self, direction, player, num_filled, start_col, start_row, end_col, end_row):
		self.direction=direction
		self.player=player
		self.num_full=num_filled
		self.start_row=start_row
		self.start_col=start_col
		self.end_row=end_row
		self.end_col=end_col


def sets_up_other(board, col, row, player, num_players):
	board[col][row]=player
	if board_won(board, num_players):
		return False
	if stop_other_three(board, player, num_players)!=-1:
		return True
	return False


def process_move(board, move, num_players):
	#see if itll go where you want
	#make sure it doesn't set up anyone else
	player=move.player
	col=move.start_col
	row=move.start_row
	if board[col][row]==-1 and col_right_height(board, col, row)and not sets_up_other(board, col, row, player, num_players):
		return col
	if move.direction=='row':
		for i in range(1,4):
			if board[col+i][row]==-1 and col_right_height(board, col+i, row) and not sets_up_other(board, col+i, row, player, num_players):
				return col+i
	if move.direction=='col':
		for i in range(1,4):
			if board[col][row+i]==-1 and col_right_height(board, col, row+i) and not sets_up_other(board, col, row+i, player, num_players):
				return col
	if move.direction=='diag1':
		for i in range(1,4):
			if board[col+i][row+i]==-1 and col_right_height(board, col+i, row+i) and not sets_up_other(board, col+i, row+i, player, num_players):
				return col+i
	if move.direction=='diag2':
		for i in range(1,4):
			if board[col+i][row-i]==-1 and col_right_height(board, col+i, row-i) and not sets_up_other(board, col+i, row-i, player, num_players):
				return col+i
	return -1  #returns if can't fill in any of the spots


def check_others(board, num_players, moves_list):
	for i in range(5):
		moves=moves_list[i]
		for move in moves:
			if process_move(board, move, num_players)!=1:
				return process_move(board,move, num_players)
	return -1


def pop_top_move(board, moves, player, num_players):
	#get col at the end from this
	player_3=other_3=player_2=other_2=player_1=other_1=[]
	for move in moves:
		if move.player==player and move.num_full==3:
			if process_move(board, move, num_players)!=1:
				return process_move(board, move, num_players)
		elif move.player==player and move.num_full==2:
			player_2.append(move)
		elif move.player==player and move.num_full==1:
			player_1.append(move)
		elif move.num_full==3:
			other_3.append(move)
		elif move.num_full==2:
			other_2.append(move)
		else:
			other_1.append(move)
	return check_others(board, num_players, [other_3, player_2, other_2, player_1, other_1])



def rows(board, moves):
	for j in range(6):
		for i in range(4):
			chunk={}
			for k in range(4):
				if board[i+k][j] not in chunk:
					chunk[board[i+k][j]]=1
				else:
					chunk[board[i+k][j]]+=1
			if len(chunk)==2 and (-1 in chunk):
				for player_key in chunk:
					if player_key!=-1:
						moves.append(Move('row', player_key, chunk[player_key], i, j, i+3, j))
	return moves

def cols(board, moves):
	for i in range(7):
		for j in range(3):
			chunk={}
			for k in range(4):
				if board[i][j+k] not in chunk:
					chunk[board[i][j+k]]=1
				else:
					chunk[board[i][j+k]]+=1
			if len(chunk)==2 and (-1 in chunk):
				for player_key in chunk:
					if player_key!=-1:
						moves.append(Move('col', player_key, chunk[player_key], i, j, i, j+3))
	return moves


def diag_up_right(board, moves):
	#diagonal going from bottom left to top right
	for col in range(4):
		for row in range(3):
			chunk={}
			for i in range(4):
				if board[col+i][row+i] not in chunk:
					chunk[board[col+i][row+i]]=1
				else:
					chunk[board[col+i][row+i]]+=1
			if len(chunk)==2 and (-1 in chunk):
				for player_key in chunk:
					if player_key!=-1:
						moves.append(Move('diag1', player_key, chunk[player_key], col, row, col+3, row+3))
	return moves


def diag_up_left(board, moves):
	#go from upper left to bottom right
	for col in range(4):
		for row in range(3): #will be 6 minus this
			chunk={}
			for i in range(4):
				if board[col+i][5-row-i] not in chunk:
					chunk[board[col+i][5-row-i]]=1
				else:
					chunk[board[col+i][5-row-i]]+=1
			if len(chunk)==2 and (-1 in chunk):
				for player_key in chunk:
					if player_key!=-1:
						moves.append(Move('diag2', player_key, chunk[player_key], col, 5-row, col+3, 2-row))
	return moves


def find_moves(board,player):
	#return a list of Move objects
	#check for every row chunk, then cols, then diag and other diag
	#when putting in, check if will set up other for winning (modify board and winning move funtion)
	#check if can be placed there(full under it)-- col right height function
	moves=[]
	moves=rows(board, moves)
	moves=cols(board, moves)
	moves=diag_up_right(board, moves)
	moves=diag_up_left(board, moves)
	return moves

def get_ai_move(board, player, num_players):
	moves=find_moves(board, player)
	move=pop_top_move(board, moves, player, num_players)
	if move!=-1:
		return move
	return get_column(board)




if __name__ == "__main__":
	board=[ \
	[-1,-1,-1,-1,-1,-1], \
	[-1,-1,-1,-1,-1,-1], \
	[-1,-1,-1,-1,-1,-1], \
	[-1,-1,-1,-1,-1,-1], \
	[-1,-1,-1,-1,-1,-1], \
	[-1,-1,-1,-1,-1,-1], \
	[-1,-1,-1,-1,-1,-1] \
	]
