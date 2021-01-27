import random
import pygame
import math

COLS = 4                    # number of cols
ROWS = 12                   # number of rows
SIZE = 180                  # virtual size
RADIUS = 20                 # radius circle
MARGIN_LR = 75              # margin left rigth
MARGIN_TB = 50              # margin top bottom

COLORS = ['Y', 'R', 'W', 'B', 'P', 'G', 'O', 'PK']

COLORS_DICT = {
    'Y': (255, 238, 0),     # yellow
    'R': (237, 68, 38),     # red
    'W': (255, 255, 255),   # white
    'B': (0, 174, 255),     # blue
    'P': (97, 0, 171),      # purple 
    'G': (33, 237, 50),     # green
    'O': (235, 144, 26),    # orange
    'PK': (237, 38, 177)    # pink
}

def init(arr):
    for _ in range(ROWS):
        arr.append(' ')

# create and init board
def create_board():
    board = []
    for i in range(12):
        board.append([])
        for j in range(COLS):
            board[i].append('.')

    return board

# draw board and colors on board
def draw_board(screen, board):
    BLACK = (37, 49, 56)
    GREY = (135, 135, 135)
    screen.fill(BLACK)
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == '.':
                pygame.draw.circle(screen, GREY, (int(j*MARGIN_LR+SIZE/COLS), (i*MARGIN_TB+60)), RADIUS)
            else:
                pygame.draw.circle(screen, COLORS_DICT.get(board[i][j]), (int(j*MARGIN_LR+SIZE/COLS), (i*MARGIN_TB+60)), RADIUS)

# draw colors on the bottom the screen
def draw_colors(screen):
    BEGIN = 44
    x = BEGIN
    y = 700
    i = 0
    for c in COLORS_DICT.values():
        pygame.draw.circle(screen, c, (x, y), RADIUS)
        x += MARGIN_LR
        i += 1
        if i == COLS:
            y += 50
            x = BEGIN

# draw colors and place to find
def draw_win_colors(screen, to_guess):
    x = 100
    for col in to_guess:
        pygame.draw.circle(screen, COLORS_DICT.get(col), (x, 350), RADIUS)
        x += 75

# put color on board
def modify_board(i, count, board, color):
    board[len(board) - 1 - count][i] = color

# compare user color and colors to guess
def compare_color(to_guess, player_colors):
    good_colors = 0
    good_place = 0
    unique_color = []

    for col in player_colors:
        if (col in to_guess and col not in unique_color):
            unique_color.append(col)
            good_colors += 1

    for i in range(0, COLS):
        if (to_guess[i] == player_colors[i]):
            good_place += 1

    return [good_colors, good_place]

# color to find
def ia_choose_colors():
    colors = COLORS.copy()
    while len(colors) != COLS:
        i = random.randint(0, len(colors) - 1)
        colors.pop(i)
    return colors

# compare user click position
def compare_xy(posx, posy):
    color = None
    if posy >= 678 and posy <= 722:
        if posx >= 24 and posx <= 64:
            color = 0
        elif posx >= 100 and posx <= 140:
            color = 1
        elif posx >= 174 and posx <= 214:
            color = 2
        elif posx >= 250 and posx <= 290:
            color = 3
    if posy >= 728 and posy <= 772:
        if posx >= 24 and posx <= 64:
            color = 4
        elif posx >= 100 and posx <= 140:
            color = 5
        elif posx >= 174 and posx <= 214:
            color = 6
        elif posx >= 250 and posx <= 290:
            color = 7
    return color

# end of game
def end(screen, to_guess):
    draw_win_colors(screen,to_guess)
    pygame.display.update()
    pygame.time.wait(3000)
    return False

def print_result(screen, result, posx):
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    font2 = pygame.font.SysFont("monospace", 40)          # font style
    for i in range(len(result)):
        s = result[i].split(',')
        if (len(s) == 2):
            gc = font2.render(s[0], 1, WHITE)
            screen.blit(gc, (325, posx))
            gp = font2.render(s[1], 1, RED)
            screen.blit(gp, (375, posx))
            posx -= MARGIN_TB

def main():
    WIDTH = 450
    HEIGHT = 800

    pygame.init()                                                    
    size = (WIDTH, HEIGHT)                               # window size

    pygame.display.set_caption("Mastermind")             # window title
    icon = pygame.image.load("img/logo.png")             # load icon         
    pygame.display.set_icon(icon)                        # put icon
    screen = pygame.display.set_mode(size)               # define screen   
    font = pygame.font.SysFont("monospace",60)           # font style

    board = create_board()
    to_guess = ia_choose_colors()
    
    run = True
    count = 0
    result = []
    on_same_line = 0

    # init result array
    init(result)

    while run:

        draw_board(screen,board)
        draw_colors(screen)

        # pos for first result (bottom)
        x = 590
        
        # print result on right 
        print_result(screen, result, x)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:  
                posx = event.pos[0]
                posy = event.pos[1]
                color = compare_xy(posx, posy)

                if color != None:
                    modify_board(on_same_line, count, board, COLORS[color])
                    on_same_line += 1

                    if on_same_line == 4:
                        resp = compare_color(to_guess, board[len(board) - 1 - count])
                        result[count] = '{},{}'.format(resp[0],resp[1])
                        count += 1
                        on_same_line = 0

                        if resp[1] == 4:
                            text = font.render('Gagné !!!',1,COLORS_DICT.get('G'))  
                            screen.fill((0,0,0))                         
                            screen.blit(text,(80,200))
                            run = end(screen,to_guess)

                if count == ROWS and run == True:
                    text = font.render('Perdu !!!', 1, COLORS_DICT.get('R')) 
                    screen.fill((0,0,0))                    
                    screen.blit(text,(90,200))
                    run = end(screen,to_guess)

if __name__ == "__main__":
    main()