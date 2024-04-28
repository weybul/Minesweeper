import random
import re
import time
class Board:
    def __init__(self,dim_size,num_bombs):
        # wer namig our arguments here, we need later on
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board
        # using a helper method
        self.board = self.create_board()
        self.empty_spots()

        # initalizing an empty set to keep track of the places wev dug
        self.dug = set()

    # definin our helper method
    def create_board(self):
        # our board is a 2d representation of list of lists
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # planting bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size
            if board[row][col] == "*": # means theres aready a bomb placed at this loc
                continue 
            board[row][col] = "*"
            bombs_planted += 1
        return board
    
    # definin a func to inform the empty spots of how many neighbouring bombs there r
    def empty_spots(self):
        # iterate again
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if self.board[row][col] == "*":
                    continue
                self.board[row][col] = self.neighbouring_spots(row,col)

    # the actual func that determines the spots that have bombs on them
    def neighbouring_spots(self,r,c):
        neig_spots = 0
        
        # iterates through the neighbouring spots based on the current spot to look for those with bombs
        for row in range(max(0, r-1), min(self.dim_size-1, r+1)+1):
            for col in range(max(0, c-1), min(self.dim_size-1, c+1)+1):
                if row == r and col == c: #meaning its looking at our current position
                    continue
                elif self.board[row][col] == "*":
                    neig_spots +=1
        return neig_spots
    
    def dig(self,row,col):
        self.dug.add((row,col)) #we call self.dugg to store the row n col wev dug at

        # if a user digs at a bomb return false else
        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0 : #if its a successful dig return true
            return True
        # else if the user digs at an empty spot
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r,c) in self.dug: #saying dont dig where ucv aready dug
                    continue
                self.dig(r,c)
        return True
    
    def __str__(self):
        # STR is a special method that is used to generate human-readable string representation of an object
        # str is a special method in python that returns the string representation of an object     
        # returns the string representation of an object

        # create a visual representation of the board to be displayed
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " " #the empty string hides the spots that r undug yet

        # this section is resposible for the str-representation of out board
        str_repr = ""
        width = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            width.append(len(max(columns, key=len)))

        # this is a row that contains the columns at the top
        indices = [i for i in range(self.dim_size)]
        indices_row = "   " #these are the spaces between the columns on the top
        cells = []
        for idx,col in enumerate(indices):
            format = "%-" + str(width[idx]+1) + "s"
            cells.append(format%(col))
        indices_row += " ".join(cells)
        indices_row += " \n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            str_repr += f"{i} |"
            cells = []
            for idx,col in enumerate(row):
                format = "%-" + str(width[idx]) + "s"
                cells.append(format%(col))
            str_repr += " |".join(cells)
            str_repr += " |\n"

        str_len = int(len(str_repr) / self.dim_size)
        str_repr = indices_row + "-"*str_len + "\n" + str_repr  + "-"*str_len
        return str_repr
    
def play(dim_size=10,num_bombs=10):
    board = Board(dim_size,num_bombs)

    # show user the board
    # take input
    # end the game if user digs at a bomb
    # if user digs at an empty spot, keep iterating untill every spot is atleast next to a bomb
    # repeat untill there r no spots left to b uncovered
    # if the user doesnt dig at a bomb and uncovers all possible spots, declare them winner
    
    safe = True
    while len(board.dug) < board.dim_size**2 - board.num_bombs:
        print(board)
        try:
            user_input = re.split(",(\\s)*", input("Enter 0,0 as row n col: "))
            row, col = int(user_input[0]), int(user_input[-1])
            if (row < 0 or row >=board.dim_size) or (col < 0 or col >=board.dim_size):
                print("!!!Invalid dig!!!")
                time.sleep(0.89)
                continue

            elif (row,col) in board.dug:
                print("spot already dug, seriously man! what u smokin")
                time.sleep(0.89)

            safe = board.dig(row,col)
            if not safe:
                break
        except ValueError:
            print("Invalid Input, try again")

    if safe:
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)
        print("Congrats! u went through all the mines without getting blown up")
    else:
        board.dug = [(r,c)for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)
        print("anddd u are fireworks :D\n")
        time.sleep(2)
        print("i mean u died, firworks..ur dog stepped on a bee")
        time.sleep(2)
        print("\nget it. get it?, nvm\n")


if __name__=="__main__":
    play()





    


        
