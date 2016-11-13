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

#AI is always number 1 in array

#check to see if adding it will help iin future


#additional logic to add, check if 4 can fit before add one


def check_if_legal(board, i, j):
	return

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
					goodspot=True
					for k in range(3-amount):
						if (board[6-i+amount+k][j+amount+k]!=-1):
							goodspot=False
					if goodspot:
						return 6-i+amount
					if i<6 and j>0 and board[6-i-1][j-1]==-1:
						#print("diaga")
						return 6-i-1
				if valid and completed:
					return 0

	#arrays from high left to low right
	for i in range(0, 7-amount+completed):
		for j in range(0, 6-amount+completed):
			if board[i][5-j]==player:
				valid=True
				k=1
				while(k<amount):
					if(board[i+k][5-j-k]!=player):
						valid=False
					k+=1
				if valid and not completed:
					goodspot=True
					for k in range(3-amount):
						if (board[i+amount+k][5-j-amount-k]!=-1):
							goodspot=False
					if goodspot:
						return i+amount
					if i>0 and j<7 and j>0 and board[i-1][6-j]==-1:
						#print("diagaaaa")
						return i-1
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
					for i in range(3-amount): #check to see if four pieces can fit there
						if board[col][row+amount+i]!=-1:
							goodspot=False
					if goodspot:
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
					for i in range(3-amount):
						if (board[col+amount+ i][row]!=-1):
							goodspot=False
					if goodspot:
						return col+amount
					if col!=0 and board[col-1][row]==-1:
						#print("row")
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
	for col in range(7):
		if board[col][5]==-1:
			return col
	print("BOARD IS FULL SOS")
	return -1


def ai_choose_col(board, player, num_players):
	col = winning_move(board, player)
	if col!=-1:
		return col
	col = stop_other_three(board, player, num_players)
	if col!=-1:
		return col
	col = progress_two(board, player)
	if col!=-1:
		return col
	col = defend_two(board, player, num_players)
	if col!=-1:
		return col
	col = next_to_existing(board, player)
	if col!=-1:
		return col
	##to get to this point it is the first move in the game
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


'''
	print_board(board)
	print()

	finished=False
	count=0
	while(not finished) and (count<10):
		col = ai_choose_col(board, 0,2)
		board=add_piece(board, col, 0)
		print_board(board)
		print()
		col=ai_choose_col(board, 1, 2)
		board=add_piece(board, col, 1)
		print_board(board)
		print()
		finished, winner = board_won(board, 2)
		count+=1
	print_board(board)
	print(winner)'''






