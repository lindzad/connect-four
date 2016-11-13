##logic for connect 4
#with each click see which column it falls into and add a checker there of certain color


#TO WIN:

#check if you have any three in a row
#check if there is anything of the opponents with three in a row
#check if you have two in a row and try to do that
#check if opponent has two in a row
#place next to one in a row
#place


#board is array of arrays, first row then column

#In array, empty is -1, different players are 0-7

#check to see if adding it will help in future

#doesnt have any foresight

#combine checking offensive and defensive for lowering amounts into one large loop


from random import randint

def check_if_legal(board, col):
	return board[col][5]==-1

def check_spot(board, col, row, player):
	if col<0 or col>6:
		return False
	if row<0 or row>5:
		return False
	if board[col][row]!=-1 and board[col][row]!=player:
		return False
	return True


def col_right_height(board, col, row_height):
	if row_height<0:
		return False
	if row_height>0:
		return board[col][row_height]==-1 and board[col][row_height-1]!=-1
	return board[col][row_height]==-1


def diag_bottom_left_top_right_check(board, amount, col, row, player):
	goodspot=True
	for k in range(4-amount):
		if not check_spot(board, 6-col+amount+k, row+amount+k, player):
			goodspot=False
			break
	if goodspot and col_right_height(board, 6-col+amount, row+amount): 
		#line from bottom left to top right
		#print("diag1", amount)
		return 6-col+amount
	goodspot=True
	for k in range(4-amount):
		if not check_spot(board, 6-col-k-1, row-k, player):
			goodspot=False
			break
	if goodspot and col_right_height(board, 6-col-1, row-1): 
		#from top right to bottom left
		#print(6-i-1, j-1)
		#print("diaga", amount)
		return 6-col-1
	return -1


def diag_top_left_to_bottom_right(board, amount, col, row, player):
	goodspot=True
	for k in range(4-amount): #goes from top left to bottom right
		if not check_spot(board, col+amount+k, 5-row-amount-k, player):
			goodspot=False
			break
	if goodspot and col_right_height(board, col+amount, 5-row-amount):
		#print("dddd", amount)
		return col+amount
	goodspot=True
	for k in range(4-amount):
		if not check_spot(board, col-k-1, 5-row+k, player):
			goodspot=False
			break
	if goodspot and check_spot(board, col, row, player) and col_right_height(board, col-1, 6-row): 
		#bottom right to top left
		#print("diagaaaa", amount)
		return col-1
	return -1


def check_diag(board, amount, player, completed):
	##arrays from low left to high right
	for i in range(amount, 7):
		for j in range(0, 6-amount+completed):
			if(board[6-i][j]==player):
				valid=True
				k=1
				while(k<amount):
					if(board[6-i+k][j+k]!=player):
						valid=False
					k+=1
				if valid and not completed:
					result = diag_bottom_left_top_right_check(board, amount, i, j, player)
					if result!=-1:
						return result
				if valid and completed:
					return 0

	#arrays from high left to low right
	for i in range(0, 7-amount-completed):
		for j in range(0, 6-amount+completed):
			if board[i][5-j]==player:
				valid=True
				k=1
				while(k<amount):
					if(board[i+k][5-j-k]!=player):
						valid=False
					k+=1
				if valid and not completed:
					result = diag_top_left_to_bottom_right(board, amount, i, j, player)
					if result!=-1:
						return result
				if valid and completed:
					return 0
	return -1

def check_col(board, amount, player, completed):
	for col in range(0, 7):
		for row in range(0, 6-amount+completed):
			if board[col][row]==player:
				valid=True
				k=1
				while k<amount:
					if board[col][row+k]!=player:
						valid=False
					k+=1
				if valid and not completed:
					goodspot=True
					for i in range(4-amount): 
						#check to see if four pieces can fit there
						if not check_spot(board, col, row+amount+i, player):
							goodspot=False
							break
					if goodspot:
						#print("col", amount)
						return col
				if valid and completed:
					return 0
	return -1


def check_row(board, amount, player, completed):
	for col in range(0, 7-amount+completed):
		for row in range(0, 6):
			if board[col][row]==player:
				valid=True
				k=1
				while k<amount:
					if board[col+k][row]!=player:
						valid=False
					k+=1
				if valid and not completed:
					goodspot=True
					for i in range(4-amount):
						if not check_spot(board, col+amount+i, row, player):
							goodspot=False
					if goodspot and col_right_height(board, col+amount, row):
						#print("row to right", amount)
						return col+amount
					goodspot=True
					for i in range(4-amount):
						if not check_spot(board, col-1-i, row, player):
							goodspot=False
							break
					if goodspot and col_right_height(board, col-1, row):
						#print("row left", amount)
						return col-1
				if valid and completed:
					return 0

	return -1

def board_won(board, num_players):
	for i in range(num_players):
		verdict = check_row(board, 4, i, 1)
		if verdict!=-1:
			return i
		verdict = check_col(board, 4, i, 1)
		if verdict!=-1:
	 		return i
		verdict = check_diag(board, 4, i, 1)
		if verdict!=-1:
			return i
	return -1

def winning_move(board, player):
	col = check_row(board,3,player,0)
	if col!=-1:
		return col
	col = check_col(board, 3,player,0)
	if col!=-1:
		return col
	col = check_diag(board, 3,player,0)
	return col

def stop_other_three(board, player, num_players):
	for i in range(num_players):
		if i !=player:
			col = check_row(board,3,i,0)
			if col!=-1:
				return col
			col= check_col(board, 3,i,0)
			if col!=-1:
				return col
			col = check_diag(board, 3,i,0)
			if col!=-1:
				return col
	return -1

def progress_two(board, player):
	col = check_row(board,2,player, 0)
	if col!=-1:
		return col
	col = check_col(board, 2,player,0)
	if col!=-1:
		return col
	col = check_diag(board, 2,player,0)
	return col

def defend_two(board, player, num_players):
	for i in range(num_players):
		if i !=player:
			col = check_row(board,2,i, 0)
			if col!=-1:
				return col
			col = check_col(board, 2,i,0)
			if col!=-1:
				return col
			col = check_diag(board, 2,i, 0)
			if col!=-1:
				return col
	return -1

def next_to_existing(board, player):
	col= check_row(board,1,player, 0)
	if col!=-1:
		return col
	col= check_col(board, 1,player, 0)
	if col!=-1:
		return col
	col= check_diag(board, 1,player, 0)
	return col


def get_column(board):
	while True:
		col=randint(0,6)
		if board[col][5]==-1:
			return col
	return -1


def ai_choose_col(board, player, num_players):
	col = winning_move(board, player)
	if col!=-1 and check_if_legal(board, col):
		#print("winning move")
		return col
	col = stop_other_three(board, player, num_players)
	if col!=-1 and check_if_legal(board, col):
		#print("stop other from winning")
		return col
	col = progress_two(board, player)
	if col!=-1 and check_if_legal(board, col):
		#print("getting 3 from two")
		return col
	col = defend_two(board, player, num_players)
	if col!=-1 and check_if_legal(board, col):
		#print("stopping their two")
		return col
	col = next_to_existing(board, player)
	if col!=-1 and check_if_legal(board, col):
		#print("make two")
		return col
	##to get to this point it is the first move in the game
	#print("getting random")
	return get_column(board)


def print_board(board):
	for row in range(6):
		for col in range(7):
			print(str(board[col][5-row]).rjust(3, ' '), end='')
		print()

def add_piece(board, col, player):
	for i in range(len(board[col])):
		if board[col][i]==-1:
			board[col][i]=player
			break
	return board


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


	print_board(board)
	print()

	winner=-1
	count=0
	while(winner==-1) and (count<10):
		col = ai_choose_col(board, 0,2)
		board=add_piece(board, col, 0)
		print_board(board)
		print()
		col=ai_choose_col(board, 1, 2)
		board=add_piece(board, col, 1)
		print_board(board)
		print()
		winner= board_won(board, 2)
		count+=1
	print(winner)






