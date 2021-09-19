import pygame
import sys

###A SIMPLE REVERSI GAME CREATED IN PYGAME ###

tile_size = 64 #size of individual grid piece
turn = 1 #if turn is odd, black plays, else, white plays, black starts
no_move_turns = 0

#values for checking up down left right, and combinations in between
directions = [ ]
n = (0, -1 * tile_size)
s = (0, tile_size) 
w = (-1*tile_size, 0)
e = (tile_size, 0)
ne = (tile_size, -1 * tile_size)
nw = (-1 * tile_size, -1*tile_size)
se = (tile_size, tile_size)
sw = (-1 * tile_size, tile_size)
directions.append(n)
directions.append(e)
directions.append(s)
directions.append(w)
directions.append(ne)
directions.append(nw)
directions.append(se)
directions.append(sw)

all_possible = [ ]
for x in range(0, 8):
    for y in range(0, 8):
        all_possible.append(((x*tile_size), (y*tile_size)))

#colours for the pieces
black = (0,0,0)
white = (255, 255, 255)

def pos_to_tile(pos):
    """converts a mouse coordinates to the coordinates of the tile that it clicked in"""
    x = (pos[0] // tile_size) * tile_size
    y = (pos[1] // tile_size) * tile_size
    return (x, y)

def valid_moves_available():
    """vchecks how many valid remaining moves are possible"""
    valid_moves = 0
    valid_move_list = []
    for n in range(0, len(enemy_piece)):
        for x in range(0, len(directions)):
            checking_piece = ((enemy_piece[n][0] + directions[x][0]), (enemy_piece[n][1] + directions[x][1]))
            if checking_piece in enemy_piece or checking_piece in current_piece:
                continue
            if checking_piece[0] > (7*tile_size) or checking_piece[0] < 0:
                continue
            if checking_piece[1] < 0 or checking_piece[1] > (7*tile_size):
                continue
            else:
                valid_move_list.append(checking_piece)
                valid_moves += 1
    if valid_moves == 0:
        return False
    else:
        print(f'for the turn {turn}, there are {valid_moves} moves available\n')
        print(valid_move_list)
        return True

def check_valid(position):
    """checks in every direction listed above, to see if the player has selected a tile
    adjacent to an enemy piece"""
    hits = 8
    if position in enemy_piece or position in current_piece:
        return False
    for n in range(0, len(directions)):
        if ((position[0] + directions[n][0]), (position[1] + directions[n][1])) in enemy_piece:
            flip(position, ( (position[0] + directions[n][0]), (position[1]+directions[n][1]) ) )
        else:
            hits -= 1
    if hits == 0:
        return False
        print('invalid move')
    else:
        return True

def flip(position, adjacent):
    """finds the furthest position on grid up to which the player has captured enemy pieces"""
    interval = (adjacent[0] - position[0], adjacent[1] - position[1])
    if adjacent[0]  < 0 or adjacent[0] > (8*tile_size):
        return False
    elif adjacent[1] < 0 or adjacent[1] > (8*tile_size):
        return False
    check_piece = (adjacent[0] + interval[0], adjacent[1] + interval[1])
    if check_piece in current_piece:
        flip_back(adjacent, (interval[0] * -1, interval[1] * -1))
    else:
        return flip(adjacent, check_piece)

def flip_back(start, interval):
	"""takes the final piece the player has captured, and working back, captures those pieces"""
	if start in current_piece:
		return
	elif start in enemy_piece:
		enemy_piece.remove((start[0], start[1]))
		current_piece.append((start[0], start[1]))
		return flip_back((start[0] + interval[0], start[1] + interval[1]), interval)

def result():
    if len(black_occupied) > len(white_occupied):
        print(f'black won with {len(black_occupied)} pieces to white\'s {len(white_occupied)} pieces')
    elif len(white_occupied) > len(black_occupied):
        print(f'white won with {len(white_occupied)} pieces to black\'s {len(black_occupied)} pieces')
    else:
        print('it\'s a draw')

#initialise pygame module
pygame.init()
screen=pygame.display.set_mode((8*tile_size,8*tile_size))
pygame.display.set_caption('Reversi')
screen.fill((50,255,255))
#starting position of black and white pieces in reversi
starting_pos = [(3 * tile_size,3*tile_size), (4*tile_size,4*tile_size),\
    (3*tile_size,4*tile_size), (4*tile_size,3*tile_size)]
#lists with all the positions occupied by either black or white tiles
black_occupied = [ ]
white_occupied = [ ]
current_piece = black_occupied
enemy_piece = white_occupied
#starting positions
for n in range(0, 4):
    if n < 2:
        black_occupied.append(starting_pos[n])
    else:
        white_occupied.append(starting_pos[n])
#draws the grid onto which the game is played
for n in range(0, 8):
    pygame.draw.line(screen, black, (n*tile_size, 0), (n*tile_size, tile_size*8))
    pygame.draw.line(screen, black, (0, n*tile_size), (8*tile_size, n*tile_size))
### ------- MAIN GAME LOOP -------- ###
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: #exit
            pygame.quit()
            sys.exit()
        if no_move_turns == 2:
            result()
        elif valid_moves_available() == False:
            no_move_turns += 1
            turn += 1
            print('no valid moves')
        else:
            print('valid moves')
        if event.type==pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            tile_pos = pos_to_tile(mouse_pos)
            if check_valid(tile_pos) == True:
                current_piece.append(tile_pos)
                turn += 1
                if turn % 2 == 1:
                    current_piece = black_occupied
                    enemy_piece = white_occupied
                else:
                    current_piece = white_occupied
                    enemy_piece = black_occupied
                no_move_turns = 0
    for n in range(0, len(black_occupied)): #draws black pieces
        pygame.draw.circle(screen, black, ((black_occupied[n][0] + 32), black_occupied[n][1] + 32), 25 )
    for n in range(0, len(white_occupied)): #draws white pieces
        pygame.draw.circle(screen, white, ((white_occupied[n][0] + 32), white_occupied[n][1] + 32), 25 )
    pygame.display.update() #UPDATE DRAW FUNCTION