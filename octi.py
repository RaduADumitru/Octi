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

# list of prongs; might not be necessary
green_pods = []
red_pods = []

data = {'green_prongs': MAX_PRONGS,
        'red_prongs': MAX_PRONGS,
        'turn': 'green',
        'run': True}


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


def pos_to_dir(col, line, x, y):  # get prong direction from square position and mouse position
    coords = pos_to_coords(col, line)
    pdir = ''
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


def prong_pos(col, line, dir):  # WIP
    return None, None


def draw_test():  # for testing
    # r_test = pygame.Rect(300, 300, 180, 300)
    # pygame.draw.rect(WIN, ORANGE, r_test)
    r_test = pygame.Surface((180, 300))
    WIN.blit(r_test, (300, 300))
    # r_test = pygame.transform.rotate(r_test, 45)
    # WIN.blit(r_test, (300, 300))


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


def draw_allprongs():  # for testing
    for green_pod in green_pods:
        draw_prongs(green_pod['pos'][0], green_pod['pos'][1])
    for red_pod in red_pods:
        draw_prongs(red_pod['pos'][0], red_pod['pos'][1])


def draw_pods():  # place pod images on board
    # for green_pod in green_pods:  # place board
    #     x, y = pos_to_coords(green_pod['pos'][0], green_pod['pos'][1])
    #     WIN.blit(GREEN_POD, (x + POD_OFFSET, y + POD_OFFSET))
    # for red_pod in red_pods:
    #     x, y = pos_to_coords(red_pod['pos'][0], red_pod['pos'][1])
    #     WIN.blit(RED_POD, (x + POD_OFFSET, y + POD_OFFSET))
    for col in board.keys():
        for line in board[col].keys():
            if board[col][line] != {}:
                draw_prongs(col, line)
                player = board[col][line]['player']
                x, y = pos_to_coords(col, line)
                x += POD_OFFSET
                y += POD_OFFSET
                if player == 'green':
                    WIN.blit(GREEN_POD, (x, y))
                elif player == 'red':
                    WIN.blit(RED_POD, (x, y))


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
    # draw_allprongs()
    draw_pods()
    # draw_test()

    pygame.display.update()


def place_prong():
    mouse_pos = pygame.mouse.get_pos()
    pod_pos = coords_to_pos(mouse_pos[0], mouse_pos[1])
    print(pygame.mouse.get_pos())
    print(pod_pos)
    if board[pod_pos[0]][pod_pos[1]] != {}:
        pdir = pos_to_dir(pod_pos[0], pod_pos[1], mouse_pos[0], mouse_pos[1])
        if not board[pod_pos[0]][pod_pos[1]]['prongs'][pdir]:
            board[pod_pos[0]][pod_pos[1]]['prongs'][pdir] = True


#  functions to move pods; WIP
def move_n(pod):
    line = chr(ord(pod['pos'][1]) - 1)
    pod['pos'][1] = chr(ord(pod['pos'][1]) - 1)


def move_nw(pod):
    pod['pos'][1] = chr(ord(pod['pos'][1]) - 1)
    pod['pos'][0] = chr(ord(pod['pos'][0]) - 1)


def move_w(pod):
    pod['pos'][0] = chr(ord(pod['pos'][0]) - 1)


def move_sw(pod):
    pass



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
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                place_prong()
        draw_board()

if __name__ == '__main__':
    while True:
        main()
