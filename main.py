import pygame
import sys

###A SIMPLE REVERSI GAME CREATED IN PYGAME ###

tile_size = 64 #size of individual grid piece
turn = 1 #if turn is odd, BLACK plays, else, WHITE plays, BLACK starts
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

#colours for the pieces and background
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

def pos_to_tile(pos):
    """converts a mouse coordinates to the coordinates of the tile that it clicked in"""
    x = (pos[0] // tile_size) * tile_size
    y = (pos[1] // tile_size) * tile_size
    return (x, y)

def basic_coords(pos):
    """returns coordinates based on reversi board grid rather than pixel coordinates"""
    x = pos[0]//tile_size
    y = pos[1]//tile_size
    return (x, y)

def valid_moves_available():
    """checks how many valid remaining moves are possible"""
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
    
def basic_check(position):
    hits = 8
    if position in enemy_piece or position in current_piece:
        return False
    for n in range(0, len(directions)):
        if ((position[0] + directions[n][0]), (position[1] + directions[n][1])) in enemy_piece:
            return True
        else:
            hits -= 1
    if hits == 0:
        return False
    
def list_valid_moves():
    """returns a list of all the valid moves possible"""
    valid_move_list = [ ]
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
    return valid_move_list

def score_move(position, adjacent, score):
    """scores a move based on how many tiles it captures, as moves are only 
    checked if we know they're valid, score always starts at 1"""
    interval = (adjacent[0] - position[0], adjacent[1] - position[1])
    check_piece = (adjacent[0] + interval[0], adjacent[1] + interval[1])
    if adjacent[0]  < 0 or adjacent[0] > (8*tile_size):
        print('out of bounds 1')
        print(adjacent)
        return 0
    elif adjacent[1] < 0 or adjacent[1] > (8*tile_size):
        print('out of bounds 2')
        print(adjacent)
        return 0
    elif adjacent not in enemy_piece and adjacent not in current_piece:
        return 0
    elif adjacent in enemy_piece:
        return score_move(adjacent, check_piece, score + 1)
    elif adjacent in current_piece:
        return score

def highest_scoring_move():
    """finds the highest scoring move"""
    moves = list_valid_moves()
    moves_scores= {}
    for n in range(0, len(moves)):
        moves_scores[moves[n]] = move_total_score(moves[n])
    for k, l in moves_scores.items():
        if l > 0:
            print(basic_coords(k), l)
    return moves_scores

def move_total_score(position):
    score = 0
    for j in range(0, len(directions)):
        adjacent = (position[0] + directions[j][0], position[1] + directions[j][1])
        score += score_move(position, adjacent, 0)
    return score

def play_best_move(move_options):
    move_score = 0
    move_pos = (0, 0)
    for i, j in move_options.items():
        if j > move_score:
            move_score = j
            move_pos = i
        elif j == move_score:
            move_score = j
            move_pos = i
    return move_pos

def minimax(current_depth, target_depth, maximise, move, score):
    if current_depth == target_depth:
        print(f'position is {move} and score is {score}')
        print(f'{move}, {score}')
        return move, score
    if maximise == True:
        pos = (0, 0)
        maxEval = -64
        possible_moves = highest_scoring_move()
        for move, score in possible_moves.items():
            eval = minimax(current_depth+1, target_depth, False, move, score)
            if eval[1] > maxEval:
                maxEval = eval[1]
                pos = eval[0]
        return pos, maxEval
    if maximise == False:
        minEval = 64
        pos = (0, 0)
        possible_moves = highest_scoring_move()
        for move, score in possible_moves.items():
            eval = minimax(current_depth+1, target_depth, True, move, score)
            if eval[1] < minEval:
                minEval = eval[1]
                pos = eval[0]
        return pos, minEval

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
    """checks which player won"""
    if len(BLACK_occupied) > len(WHITE_occupied):
        print(f'BLACK won with {len(BLACK_occupied)} pieces to WHITE\'s {len(WHITE_occupied)} pieces')
    elif len(WHITE_occupied) > len(BLACK_occupied):
        print(f'WHITE won with {len(WHITE_occupied)} pieces to BLACK\'s {len(BLACK_occupied)} pieces')
    else:
        print('it\'s a draw')

def log_move(move):
    move_log.append(basic_coords(move))
    pass

def view_move_log():
    return move_log

#initialise pygame module
pygame.init()
screen=pygame.display.set_mode((8*tile_size,8*tile_size))
pygame.display.set_caption('Reversi')
screen.fill(GREY)
#starting position of BLACK and WHITE pieces in reversi
starting_pos = [(3 * tile_size,3*tile_size), (4*tile_size,4*tile_size),\
    (3*tile_size,4*tile_size), (4*tile_size,3*tile_size)]
#lists with all the positions occupied by either BLACK or WHITE tiles
BLACK_occupied = [ ]
WHITE_occupied = [ ]
current_piece = BLACK_occupied
enemy_piece = WHITE_occupied
move_log = [ ]
# WHITE_occupied.append((192, 128))
#starting positions
for n in range(0, 4):
    if n < 2:
        BLACK_occupied.append(starting_pos[n])
    else:
        WHITE_occupied.append(starting_pos[n])
#draws the grid onto which the game is played
for n in range(0, 8):
    pygame.draw.line(screen, BLACK, (n*tile_size, 0), (n*tile_size, tile_size*8))
    pygame.draw.line(screen, BLACK, (0, n*tile_size), (8*tile_size, n*tile_size))
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
        # else:
        #     print('valid moves')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                print('button pressed')
                highest_scoring_move()
        if turn % 2 == 1:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button == 3: # right click
                    mouse_pos = pygame.mouse.get_pos()
                    tile_pos = pos_to_tile(mouse_pos)
                    print(move_total_score(tile_pos))
                elif event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    tile_pos = pos_to_tile(mouse_pos)
                    if check_valid(tile_pos) == True:
                        log_move(tile_pos)
                        current_piece.append(tile_pos)
                        turn += 1
                        if turn % 2 == 1:
                            current_piece = BLACK_occupied
                            enemy_piece = WHITE_occupied
                        else:
                            current_piece = WHITE_occupied
                            enemy_piece = BLACK_occupied
                        no_move_turns = 0
        else:
            white_turn = minimax(0, 2, False, 0, 0)
            print(f"white_turn is {white_turn}")
            print(f'white turn pos is {white_turn[0]}')
            if check_valid(white_turn[0]) == True:
                current_piece.append(white_turn[0])
                # log_move(white_turn)
                turn += 1
                if turn % 2 == 1:
                    current_piece = BLACK_occupied
                    enemy_piece = WHITE_occupied
                else:
                    current_piece = WHITE_occupied
                    enemy_piece = BLACK_occupied
                    no_move_turns = 0

    for n in range(0, len(BLACK_occupied)): #draws BLACK pieces
        pygame.draw.circle(screen, BLACK, ((BLACK_occupied[n][0] + 32), BLACK_occupied[n][1] + 32), 25 )
    for n in range(0, len(WHITE_occupied)): #draws WHITE pieces
        pygame.draw.circle(screen, WHITE, ((WHITE_occupied[n][0] + 32), WHITE_occupied[n][1] + 32), 25 )
    pygame.display.update() #UPDATE DRAW FUNCTION