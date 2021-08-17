import pygame
import os
import copy
import math

pygame.init()
pod_template = {'player': '',
                'prongs': {'NW': False, 'N': False, 'NE': False, 'E': False,
                           'SE': False, 'S': False, 'SW': False, 'W': False},
                'pos': ['', '']}  # empty pod
board = {'A': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'B': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'C': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'D': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'E': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'F': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}}}  # empty board

MAX_PRONGS = 12  # number of prongs each player starts with
LWIDTH = 4  # width of line on board
DIM_SQUARE = 90  # dimension of square
DIM_POD = 60  # dimension of pod
POD_OFFSET = (DIM_SQUARE - DIM_POD) // 2  # used for placing pod
COLUMNS = 6
LINES = 7
# width and height of board
WIDTH, HEIGHT = (COLUMNS + 1) * LWIDTH + COLUMNS * DIM_SQUARE, (LINES + 1) * LWIDTH + LINES * DIM_SQUARE
PRONG_DIAG_SIZE = 30
PRONG_LENGTH = 30
PRONG_WIDTH = 10

# colors used
BEIGE = (245, 245, 220)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
LIGHT_GREEN = (50, 205, 50)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption("Octi")

# load images
# TODO: transparent images on selection / hover
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


GREEN_POD_IMAGE = pygame.image.load(os.path.join('Assets', 'green_pod.png'))
GREEN_POD = pygame.transform.rotate(pygame.transform.scale(GREEN_POD_IMAGE, (DIM_POD, DIM_POD)), 90)
RED_POD_IMAGE = pygame.image.load(os.path.join('Assets', 'red_pod.png'))
RED_POD = pygame.transform.rotate(pygame.transform.scale(RED_POD_IMAGE, (DIM_POD, DIM_POD)), -90)
PRONG_HORIZ_IMAGE = pygame.image.load(os.path.join('Assets', 'prong_horiz.png'))
PRONG_HORIZ = pygame.transform.scale(PRONG_HORIZ_IMAGE, (PRONG_LENGTH, PRONG_WIDTH))
PRONG_VERT_IMAGE = pygame.image.load(os.path.join('Assets', 'prong_vert.png'))
PRONG_VERT = pygame.transform.scale(PRONG_VERT_IMAGE, (PRONG_WIDTH, PRONG_LENGTH))
PRONG_DIAG1_IMAGE = pygame.image.load(os.path.join('Assets', 'prong_diag1.png'))
PRONG_DIAG1 = pygame.transform.scale(PRONG_DIAG1_IMAGE, (PRONG_DIAG_SIZE, PRONG_DIAG_SIZE))
PRONG_DIAG2_IMAGE = pygame.image.load(os.path.join('Assets', 'prong_diag2.png'))
PRONG_DIAG2 = pygame.transform.scale(PRONG_DIAG2_IMAGE, (PRONG_DIAG_SIZE, PRONG_DIAG_SIZE))
GREEN_PODS_LIST=[]
RED_PODS_LIST=[]

data = {'green_prongs': MAX_PRONGS,
        'red_prongs': MAX_PRONGS,
        'turn': 'green',
        'run': True,
        'sel_pod': ['', ''],
        'mouse_coords': [0, 0],
        'mouse_square': ['A', '1']}


def init_board():
    data['turn'] = 'green'
    data['green_prongs'] = MAX_PRONGS
    data['red_prongs'] = MAX_PRONGS
    # place pods in starting positions
    for i in range(4):
        greenpod = copy.deepcopy(pod_template)
        greenpod['player'] = 'green'
        greenpod['pos'] = [chr(ord('A') + i + 1), '6']
        col = greenpod['pos'][0]
        line = greenpod['pos'][1]
        board[col][line] = greenpod
    for i in range(4):
        redpod = copy.deepcopy(pod_template)
        redpod['player'] = 'red'
        redpod['pos'] = [chr(ord('A') + i + 1), '2']
        col = redpod['pos'][0]
        line = redpod['pos'][1]
        board[col][line] = redpod


def pos_to_coords(a, b):  # get position on board from pygame coordinates
    col = ord(a) - ord('A') + 1
    line = int(b)
    x = col * LWIDTH + (col - 1) * DIM_SQUARE
    y = line * LWIDTH + (line - 1) * DIM_SQUARE
    return x, y


def coords_to_pos(x, y):  # get pygame coordinates from position on board
    col = chr(ord('A') + x // (LWIDTH + DIM_SQUARE))
    line = str(1 + y // (LWIDTH + DIM_SQUARE))
    return col, line


def pos_to_dir(col, line):  # get prong direction from square position and mouse position
    coords = pos_to_coords(col, line)
    pdir = ''
    x = data['mouse_coords'][0]
    y = data['mouse_coords'][1]
    minisquare_x = math.floor((x - coords[0]) // (DIM_SQUARE // 3))
    minisquare_y = math.floor((y - coords[1]) // (DIM_SQUARE // 3))
    if minisquare_x == 0 and minisquare_y == 0:
        pdir = 'NW'
    elif minisquare_x == 1 and minisquare_y == 0:
        pdir = 'N'
    elif minisquare_x == 2 and minisquare_y == 0:
        pdir = 'NE'
    elif minisquare_x == 0 and minisquare_y == 1:
        pdir = 'W'
    elif minisquare_x == 2 and minisquare_y == 1:
        pdir = 'E'
    elif minisquare_x == 0 and minisquare_y == 2:
        pdir = 'SW'
    elif minisquare_x == 1 and minisquare_y == 2:
        pdir = 'S'
    elif minisquare_x == 2 and minisquare_y == 2:
        pdir = 'SE'
    return pdir


def draw_prongs(col, line):  # place prong images on board
    x, y = pos_to_coords(col, line)
    if board[col][line]['prongs']['N']:
        WIN.blit(PRONG_VERT, (x + DIM_SQUARE // 2 - PRONG_WIDTH // 2, y))
    if board[col][line]['prongs']['NW']:
        WIN.blit(PRONG_DIAG1, (x, y))
    if board[col][line]['prongs']['W']:
        WIN.blit(PRONG_HORIZ, (x, y + DIM_SQUARE // 2 - PRONG_WIDTH // 2))
    if board[col][line]['prongs']['SW']:
        WIN.blit(PRONG_DIAG2, (x, y + DIM_SQUARE - PRONG_DIAG_SIZE))
    if board[col][line]['prongs']['S']:
        WIN.blit(PRONG_VERT, (x + DIM_SQUARE // 2 - PRONG_WIDTH // 2, y + DIM_SQUARE - PRONG_LENGTH))
    if board[col][line]['prongs']['SE']:
        WIN.blit(PRONG_DIAG1, (x + DIM_SQUARE - PRONG_DIAG_SIZE, y + DIM_SQUARE - PRONG_DIAG_SIZE))
    if board[col][line]['prongs']['E']:
        WIN.blit(PRONG_HORIZ, (x + DIM_SQUARE - PRONG_LENGTH, y + DIM_SQUARE // 2 - PRONG_WIDTH // 2))
    if board[col][line]['prongs']['NE']:
        WIN.blit(PRONG_DIAG2, (x + DIM_SQUARE - PRONG_DIAG_SIZE, y))
    return


def draw_pods():  # place pod images on board
    i = 0
    j = 0
    for col in board.keys():
        for line in board[col].keys():
            if board[col][line]:
                draw_prongs(col, line)
                player = board[col][line]['player']
                x, y = pos_to_coords(col, line)
                x += POD_OFFSET
                y += POD_OFFSET
                if player == 'green':
                    GREEN_PODS_LIST.append(pygame.transform.rotate(pygame.transform.scale(GREEN_POD_IMAGE, (DIM_POD, DIM_POD)), 90))
                    WIN.blit(GREEN_PODS_LIST[i], (x, y))
                    board[col][line]['img'] = GREEN_PODS_LIST[i]
                    i += 1
                    
                elif player == 'red':
                    RED_PODS_LIST.append(pygame.transform.rotate(pygame.transform.scale(RED_POD_IMAGE, (DIM_POD, DIM_POD)), 90))
                    WIN.blit(RED_PODS_LIST[j], (x, y))
                    board[col][line]['img'] = RED_PODS_LIST[j]
                    j += 1


def draw_board():  # draw game board
    WIN.fill(BEIGE)
    red_start = pygame.Rect(DIM_SQUARE + LWIDTH, DIM_SQUARE + LWIDTH,
                            5 * LWIDTH + 4 * DIM_SQUARE, 2 * LWIDTH + DIM_SQUARE)
    pygame.draw.rect(WIN, ORANGE, red_start)
    green_start = pygame.Rect(DIM_SQUARE + LWIDTH, DIM_SQUARE * 5 + LWIDTH * 5,
                              5 * LWIDTH + 4 * DIM_SQUARE, 2 * LWIDTH + DIM_SQUARE)
    pygame.draw.rect(WIN, LIGHT_GREEN, green_start)
    for vlinex in range(0, WIDTH + DIM_SQUARE + LWIDTH, + DIM_SQUARE + LWIDTH):
        vline = pygame.Rect(vlinex, 0, LWIDTH, HEIGHT)
        pygame.draw.rect(WIN, BLACK, vline)
    for hliney in range(0, HEIGHT + DIM_SQUARE + LWIDTH, + DIM_SQUARE + LWIDTH):
        hline = pygame.Rect(0, hliney, WIDTH, LWIDTH)
        pygame.draw.rect(WIN, BLACK, hline)
    draw_pods()
    # draw_test()

    pygame.display.update()


def selection():
    x = data['mouse_coords'][0]
    y = data['mouse_coords'][1]
    sel = 'none'
    col = data['mouse_square'][0]
    line = data['mouse_square'][1]
    if col in board and line in board[col]:
        if board[col][line]:
            coords = pos_to_coords(col, line)
            minisquare_x = math.floor((x - coords[0]) // (DIM_SQUARE // 3))
            minisquare_y = math.floor((y - coords[1]) // (DIM_SQUARE // 3))
            if minisquare_x == 0 and minisquare_y == 0:
                sel = 'NW'
            elif minisquare_x == 1 and minisquare_y == 0:
                sel = 'N'
            elif minisquare_x == 2 and minisquare_y == 0:
                sel = 'NE'
            elif minisquare_x == 0 and minisquare_y == 1:
                sel = 'W'
            elif minisquare_x == 1 and minisquare_y == 1:
                data['sel_pod'] = [col, line]
                sel = 'pod'
            elif minisquare_x == 2 and minisquare_y == 1:
                sel = 'E'
            elif minisquare_x == 0 and minisquare_y == 2:
                sel = 'SW'
            elif minisquare_x == 1 and minisquare_y == 2:
                sel = 'S'
            elif minisquare_x == 2 and minisquare_y == 2:
                sel = 'SE'
    return sel

def move_pod(dest_col, dest_line):
    col = data['sel_pod'][0]
    line = data['sel_pod'][1]
    pod = board[col][line]
    if(valid_move(data['sel_pod'][0],data['sel_pod'][1])):
        board[dest_col][dest_line] = pod
        data['sel_pod'][0] = dest_col
        data['sel_pod'][1] = dest_line
        del board[col][line]

def valid_move(last_col,last_line):
    pod_col = ord(data['sel_pod'][0])
    pod_line = ord(data['sel_pod'][1])
    square_col = ord(data['mouse_square'][0])
    square_line = ord(data['mouse_square'][1])
    pod = board[last_col][last_line]
    if board[last_col][last_line]['prongs']['N'] == True and square_line - pod_line == -1:
        return 1
    elif board[last_col][last_line]['prongs']['NW'] == True and (square_line - pod_line == -1 and pod_col - square_col == 1):
        return 1
    elif board[last_col][last_line]['prongs']['W'] == True and pod_col - square_col == 1:
        return 1
    elif board[last_col][last_line]['prongs']['NE'] == True and (square_line - pod_line == -1 and pod_col - square_col == -1):
        return 1
    elif board[last_col][last_line]['prongs']['E'] == True and (pod_col - square_col == -1):
        return 1
    elif board[last_col][last_line]['prongs']['S'] == True and (square_line - pod_line == 1):
        return 1
    elif board[last_col][last_line]['prongs']['SE'] == True and (square_line - pod_line == 1 and pod_col - square_col == -1):
        return 1
    elif board[last_col][last_line]['prongs']['SW'] == True and (square_line - pod_line == 1 and pod_col - square_col == 1):
        return 1
    return 0
    
    
       
# functions to move pods; WIP
def move_n(pod):
    line = chr(ord(pod['pos'][1]) - 1)
    pod['pos'][1] = chr(ord(pod['pos'][1]) - 1)
    


def move_nw(pod):
    pod['pos'][1] = chr(ord(pod['pos'][1]) - 1)
    pod['pos'][0] = chr(ord(pod['pos'][0]) - 1)
    

def move_w(pod):
    pod['pos'][0] = chr(ord(pod['pos'][0]) - 1)


def end_turn():
    data['sel_pod'] = ['', '']
    if data['turn'] == 'green':
        data['turn'] = 'red'
    elif data['turn'] == 'red':
        data['turn'] = 'green'


def over_pod():
    mousex = data['mouse_coords'][0]
    mousey = data['mouse_coords'][1]
    col, line = coords_to_pos(mousex, mousey)
    # if board[col][line] and


# check for each player winning; WIP
def check_win_green():
    for pod in []:
        if (ord('B') <= ord(pod['pos'][0]) <= ord('E')) and pod['pos'][1] == '2':
            pass


def check_win_red():
    for pod in []:
        if (ord('B') <= ord(pod['pos'][0]) <= ord('E')) and pod['pos'][1] == '6':
            pass


def main():
    init_board()
    run = True
    last_col = -1
    last_line = -1
    selected = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            data['mouse_coords'] = pygame.mouse.get_pos()
            x = data['mouse_coords'][0]
            y = data['mouse_coords'][1]
            col = data['mouse_square'][0]
            line = data['mouse_square'][1]
            data['mouse_square'] = list(coords_to_pos(x, y))
            sel = selection()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sel not in ('none', 'pod'):
                    board[col][line]['prongs'][sel] = True
                elif sel == 'pod':
                    selected = 1
                    data['sel_pod'] = [col, line]
                    print(f'Pod {col}{line} selected')
                    x, y = pos_to_coords(col, line)
                    board[col][line]['img'].set_alpha(100)
                    #blit_alpha(WIN, board[col][line]['img'],(x,y), 100)
                    pygame.display.update()
                if (last_col != -1 and last_line != -1) and selected:
                    if last_col != col or last_line != line:
                        board[last_col][last_line]['img'].set_alpha(255)
                        pygame.display.update()
                        move_pod(col,line)
                last_col = data['sel_pod'][0]
                last_line = data['sel_pod'][1]
                print(last_col,last_line)

            #alpha_surface.fill((0,0,0,0))
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        draw_board()


if __name__ == '__main__':
    while True:
        main()
