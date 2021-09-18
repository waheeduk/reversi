import pygame
import sys

###A SIMPLE REVERSI GAME CREATED IN PYGAME ###

tile_size = 64 #size of individual grid piece
turn = 1 #if turn is odd, black plays, else, white plays, black starts

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

#colours for the pieces
black = (0,0,0)
white = (255, 255, 255)

def pos_to_tile(pos):
    """converts a mouse coordinates to the coordinates of the tile that it clicked in"""
    x = (pos[0] // tile_size) * tile_size
    y = (pos[1] // tile_size) * tile_size
    return (x, y)

def check_valid(position):
    """checks in every direction listed above, to see if the player has selected a tile
    adjacent to an enemy piece"""
    hits = 8
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
    for n in range(0, len(black_occupied)): #draws black pieces
        pygame.draw.circle(screen, black, ((black_occupied[n][0] + 32), black_occupied[n][1] + 32), 25 )
    for n in range(0, len(white_occupied)): #draws white pieces
        pygame.draw.circle(screen, white, ((white_occupied[n][0] + 32), white_occupied[n][1] + 32), 25 )
    pygame.display.update() #UPDATE DRAW FUNCTION