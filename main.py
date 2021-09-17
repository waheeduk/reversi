import pygame
import sys

tile_size = 64 #size of individual grid piece
turn = 1 #if turn is odd, black plays, else, white plays, black starts

#values for checking up down left right
up = (0, -1 * tile_size)
down = (0, tile_size) 
left = (-1*tile_size, 0)
right = (tile_size, 0)


black = (0,0,0)
white = (255, 255, 255)
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
    for n in range(0, len(black_occupied)): #draws black pieces
        pygame.draw.circle(screen, black, ((black_occupied[n][0] + 32), black_occupied[n][1] + 32), 25 )
    for n in range(0, len(white_occupied)): #draws white pieces
        pygame.draw.circle(screen, white, ((white_occupied[n][0] + 32), white_occupied[n][1] + 32), 25 )
    pygame.display.update() #UPDATE DRAW FUNCTION