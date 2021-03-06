import pygame
import os
import sys
import copy
import math
import time

pygame.init()
pod_template = {'player': '',
                'prongs': {'NW': False, 'N': False, 'NE': False, 'E': False,
                           'SE': False, 'S': False, 'SW': False, 'W': False}
                }  # empty pod
board = {'A': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'B': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'C': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'D': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'E': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}},
         'F': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}}}  # empty board

data = {'turn': 'green',
        'run': True,
        'sel_pod': ['', ''],
        'mouse_coords': [0, 0],
        'mouse_square': ['', ''],
        'capturing': False}

DIR_DATA = {'N': 'PRONG_VERT, (x + DIM_SQUARE // 2 - PRONG_WIDTH // 2, y)',
            'NW': 'PRONG_DIAG1, (x, y)',
            'W': 'PRONG_HORIZ, (x, y + DIM_SQUARE // 2 - PRONG_WIDTH // 2)',
            'SW': 'PRONG_DIAG2, (x, y + DIM_SQUARE - PRONG_DIAG_SIZE)',
            'S': 'PRONG_VERT, (x + DIM_SQUARE // 2 - PRONG_WIDTH // 2, y + DIM_SQUARE - PRONG_LENGTH)',
            'SE': 'PRONG_DIAG1, (x + DIM_SQUARE - PRONG_DIAG_SIZE, y + DIM_SQUARE - PRONG_DIAG_SIZE)',
            'E': 'PRONG_HORIZ, (x + DIM_SQUARE - PRONG_LENGTH, y + DIM_SQUARE // 2 - PRONG_WIDTH // 2)',
            'NE': 'PRONG_DIAG2, (x + DIM_SQUARE - PRONG_DIAG_SIZE, y)'}

DIRECTIONS = ('N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE')

LWIDTH = 4  # width of line on board
DIM_SQUARE = 90  # dimension of square
DIM_POD = 60  # dimension of pod
POD_OFFSET = (DIM_SQUARE - DIM_POD) // 2  # used for placing pod
COLUMNS = 6
LINES = 7
# width and height of board
WIDTH, HEIGHT = (COLUMNS + 1) * LWIDTH + COLUMNS * DIM_SQUARE, (LINES + 1) * LWIDTH + LINES * DIM_SQUARE
# prong image dimensions
PRONG_DIAG_SIZE = 30
PRONG_LENGTH = 30
PRONG_WIDTH = 10

# colors used
BEIGE = (245, 245, 220)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
LIGHT_GREEN = (50, 205, 50)
DARK_GREEN = (22, 101, 36)
RED = (200, 66, 13)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption("Octi")


# load images
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


GREEN_POD_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'green_pod.png')))
GREEN_POD = pygame.transform.rotate(pygame.transform.scale(GREEN_POD_IMAGE, (DIM_POD, DIM_POD)), 90)
RED_POD_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'red_pod.png')))
RED_POD = pygame.transform.rotate(pygame.transform.scale(RED_POD_IMAGE, (DIM_POD, DIM_POD)), -90)
PRONG_HORIZ_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'prong_horiz.png')))
PRONG_HORIZ = pygame.transform.scale(PRONG_HORIZ_IMAGE, (PRONG_LENGTH, PRONG_WIDTH))
PRONG_VERT_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'prong_vert.png')))
PRONG_VERT = pygame.transform.scale(PRONG_VERT_IMAGE, (PRONG_WIDTH, PRONG_LENGTH))
PRONG_DIAG1_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'prong_diag1.png')))
PRONG_DIAG1 = pygame.transform.scale(PRONG_DIAG1_IMAGE, (PRONG_DIAG_SIZE, PRONG_DIAG_SIZE))
PRONG_DIAG2_IMAGE = pygame.image.load(resource_path(os.path.join('Assets', 'prong_diag2.png')))
PRONG_DIAG2 = pygame.transform.scale(PRONG_DIAG2_IMAGE, (PRONG_DIAG_SIZE, PRONG_DIAG_SIZE))

FONT = 'freesansbold.ttf'
FONT_SIZE = 20
FONT2_SIZE = 45
OUTLINE_OFFSET = 2
# text
font = pygame.font.Font(FONT, FONT_SIZE)
turn_text = font.render('Turn: ', True, BLACK)
green_text = font.render('green', True, DARK_GREEN)
orange_text = font.render('red', True, RED)
font2 = pygame.font.Font(FONT, FONT2_SIZE)
WINNER_GREEN = font2.render('GREEN WINS!', True, DARK_GREEN)
WINNER_GREEN_OUTLINE = font2.render('GREEN WINS!', True, BLACK)
WINNER_RED = font2.render('RED WINS!', True, RED)
WINNER_RED_OUTLINE = font2.render('RED WINS!', True, BLACK)


def draw_win_text(text):  # draw outlined text upon win
    def draw1(x1, y1, drawn_text, window):
        textbox = drawn_text.get_rect()
        textbox.center = (x1, y1)
        window.blit(drawn_text, textbox)

    x = WIDTH // 2
    y = HEIGHT // 2

    # TEXT OUTLINE
    outline_text = WINNER_RED_OUTLINE
    if text == WINNER_GREEN:
        outline_text = WINNER_GREEN_OUTLINE
    # top left
    draw1(x - OUTLINE_OFFSET, y - OUTLINE_OFFSET, outline_text, WIN)
    # top right
    draw1(x + OUTLINE_OFFSET, y - OUTLINE_OFFSET, outline_text, WIN)
    # btm left
    draw1(x - OUTLINE_OFFSET, y + OUTLINE_OFFSET, outline_text, WIN)
    # btm right
    draw1(x + OUTLINE_OFFSET, y + OUTLINE_OFFSET, outline_text, WIN)

    # TEXT FILL

    draw1(x, y, text, WIN)


def blit_alpha(target, source, location, opacity):  # draw transparent images
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


# text position
TURN_TEXT_POS = (2 * LWIDTH, 2 * LWIDTH)
TURN_PLAYER_POS = (2 * LWIDTH + turn_text.get_width(), 2 * LWIDTH)

# alpha values for transparency
PRONG_HOVEROVERPOD_ALPHA = 192
PRONG_HOVEROVERPLACEMENT_ALPHA = 64
PRONG_SELECT_ALPHA = 128
POD_HOVER_ALPHA = 192
POD_SELECT_ALPHA = 128


def clear_board():  # reset board when starting new game
    for col in board.keys():
        for line in board[col].keys():
            board[col][line] = {}


def init_board():
    clear_board()
    deselect()
    data['capturing'] = False
    data['turn'] = 'green'
    # place pods in starting positions
    for i in range(4):
        greenpod = copy.deepcopy(pod_template)
        greenpod['player'] = 'green'
        board[chr(ord('A') + i + 1)]['6'] = greenpod
    for i in range(4):
        redpod = copy.deepcopy(pod_template)
        redpod['player'] = 'red'
        board[chr(ord('A') + i + 1)]['2'] = redpod


def draw_turn_text():  # turn text
    WIN.blit(turn_text, TURN_TEXT_POS)
    if data['turn'] == 'green':
        WIN.blit(green_text, TURN_PLAYER_POS)
    if data['turn'] == 'red':
        WIN.blit(orange_text, TURN_PLAYER_POS)


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


def draw_prongs(col, line):  # place prong images on board
    x, y = pos_to_coords(col, line)
    sel_col = data['sel_pod'][0]
    sel_line = data['sel_pod'][1]
    mouse_col = data['mouse_square'][0]
    mouse_line = data['mouse_square'][1]
    sel_dir = selection()
    selected = False
    if sel_col == col and sel_line == line:
        selected = True
    for pdir in DIRECTIONS:
        if valid_capture(mouse_col, mouse_line) == 'none':
            if board[col][line]['prongs'][pdir]:
                if not selected:
                    if col == mouse_col and line == mouse_line and sel_dir == 'pod':
                        exec('blit_alpha(WIN, ' + DIR_DATA[pdir] + ', PRONG_HOVEROVERPOD_ALPHA)')
                    else:
                        exec('WIN.blit(' + DIR_DATA[pdir] + ')')
                else:
                    exec('blit_alpha(WIN, ' + DIR_DATA[pdir] + ', PRONG_SELECT_ALPHA)')
            elif pdir == sel_dir:
                if col == mouse_col and line == mouse_line:
                    if not data['capturing']:
                        exec('blit_alpha(WIN, ' + DIR_DATA[pdir] + ', PRONG_HOVEROVERPLACEMENT_ALPHA)')
        else:
            if board[col][line]['prongs'][pdir]:
                if not selected:
                    if col == mouse_col and line == mouse_line:
                        exec('blit_alpha(WIN, ' + DIR_DATA[pdir] + ', PRONG_HOVEROVERPOD_ALPHA)')
                    else:
                        exec('WIN.blit(' + DIR_DATA[pdir] + ')')
                else:
                    exec('blit_alpha(WIN, ' + DIR_DATA[pdir] + ', PRONG_SELECT_ALPHA)')

    return


def draw_pods():  # place pod images on board
    sel_col = data['sel_pod'][0]
    sel_line = data['sel_pod'][1]
    mouse_col = data['mouse_square'][0]
    mouse_line = data['mouse_square'][1]
    for col in board.keys():
        for line in board[col].keys():
            if board[col][line]:
                draw_prongs(col, line)
                player = board[col][line]['player']
                x, y = pos_to_coords(col, line)
                x += POD_OFFSET
                y += POD_OFFSET
                pod = None
                if player == 'green':
                    pod = GREEN_POD
                elif player == 'red':
                    pod = RED_POD
                selected = False
                if col == sel_col and line == sel_line:
                    selected = True
                if valid_capture(mouse_col, mouse_line) == 'none':
                    if not selected:
                        if col == mouse_col and line == mouse_line and selection() == 'pod':
                            blit_alpha(WIN, pod, (x, y), POD_HOVER_ALPHA)
                        else:
                            WIN.blit(pod, (x, y))
                    else:
                        blit_alpha(WIN, pod, (x, y), POD_SELECT_ALPHA)
                else:
                    if not selected:
                        if col == mouse_col and line == mouse_line:
                            blit_alpha(WIN, pod, (x, y), POD_HOVER_ALPHA)
                        else:
                            WIN.blit(pod, (x, y))
                    else:
                        blit_alpha(WIN, pod, (x, y), POD_SELECT_ALPHA)


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
    draw_turn_text()
    pygame.display.update()


def selection():  # return portion of square where mouse is located
    x = int(data['mouse_coords'][0])
    y = int(data['mouse_coords'][1])
    sel = 'none'
    col = data['mouse_square'][0]
    line = data['mouse_square'][1]
    if col in board and line in board[col]:
        if board[col][line] and board[col][line]['player'] == data['turn']:
            coords = pos_to_coords(col, line)
            # square split into 9 equal smaller squares, each corresponding to a direction / center
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


def deselect():
    data['sel_pod'] = ['', '']


def valid_move():  # check if selected piece can move on mouse position
    last_col = data['sel_pod'][0]
    last_line = data['sel_pod'][1]
    pod_col = ord(data['sel_pod'][0])
    pod_line = ord(data['sel_pod'][1])
    square_col = ord(data['mouse_square'][0])
    square_line = ord(data['mouse_square'][1])
    if chr(square_col) in board.keys() and chr(square_line) in board[chr(square_col)].keys():
        if not board[chr(square_col)][chr(square_line)]:
            if board[last_col][last_line]['prongs'][
              'N'] is True and square_line - pod_line == -1 and pod_col == square_col:
                return 1
            elif board[last_col][last_line]['prongs'][
              'NW'] is True and square_line - pod_line == -1 and pod_col - square_col == 1:
                return 1
            elif board[last_col][last_line]['prongs'][
              'W'] is True and pod_col - square_col == 1 and pod_line == square_line:
                return 1
            elif board[last_col][last_line]['prongs'][
              'NE'] is True and square_line - pod_line == -1 and pod_col - square_col == -1:
                return 1
            elif board[last_col][last_line]['prongs'][
              'E'] is True and pod_col - square_col == -1 and square_line == pod_line:
                return 1
            elif board[last_col][last_line]['prongs'][
              'S'] is True and square_line - pod_line == 1 and pod_col == square_col:
                return 1
            elif board[last_col][last_line]['prongs'][
              'SE'] is True and square_line - pod_line == 1 and pod_col - square_col == -1:
                return 1
            elif board[last_col][last_line]['prongs'][
              'SW'] is True and square_line - pod_line == 1 and pod_col - square_col == 1:
                return 1
    return 0


def capture(col, line):
    if board[col][line]['player'] != data['turn']:
        board[col][line] = {}


def move_capture(pdir):  # move piece in a given direction when capturing
    pod_col = data['sel_pod'][0]
    pod_line = data['sel_pod'][1]
    square_col = data['mouse_square'][0]
    square_line = data['mouse_square'][1]
    pod = board[pod_col][pod_line]
    capture(square_col, square_line)
    if pdir == 'N':
        data['sel_pod'][0] = pod_col
        data['sel_pod'][1] = chr(ord(pod_line) - 2)
        board[pod_col][chr(ord(pod_line) - 2)] = pod
        board[pod_col][pod_line] = {}
    elif pdir == 'NW':
        data['sel_pod'][0] = chr(ord(pod_col) - 2)
        data['sel_pod'][1] = chr(ord(pod_line) - 2)
        board[chr(ord(pod_col) - 2)][chr(ord(pod_line) - 2)] = pod
    elif pdir == 'W':
        data['sel_pod'][0] = chr(ord(pod_col) - 2)
        data['sel_pod'][1] = pod_line
        board[chr(ord(pod_col) - 2)][pod_line] = pod
    elif pdir == 'SW':
        data['sel_pod'][0] = chr(ord(pod_col) - 2)
        data['sel_pod'][1] = chr(ord(pod_line) + 2)
        board[chr(ord(pod_col) - 2)][chr(ord(pod_line) + 2)] = pod
    elif pdir == 'S':
        data['sel_pod'][0] = pod_col
        data['sel_pod'][1] = chr(ord(pod_line) + 2)
        board[pod_col][chr(ord(pod_line) + 2)] = pod
    elif pdir == 'SE':
        data['sel_pod'][0] = chr(ord(pod_col) + 2)
        data['sel_pod'][1] = chr(ord(pod_line) + 2)
        board[chr(ord(pod_col) + 2)][chr(ord(pod_line) + 2)] = pod
    elif pdir == 'E':
        data['sel_pod'][0] = chr(ord(pod_col) + 2)
        data['sel_pod'][1] = pod_line
        board[chr(ord(pod_col) + 2)][pod_line] = pod
    elif pdir == 'NE':
        data['sel_pod'][0] = chr(ord(pod_col) + 2)
        data['sel_pod'][1] = chr(ord(pod_line) - 2)
        board[chr(ord(pod_col) + 2)][chr(ord(pod_line) - 2)] = pod
    board[pod_col][pod_line] = {}


def valid_capture(col, line):  # check in which direction selected piece can capture on given square, if any
    last_col = data['sel_pod'][0]
    last_line = data['sel_pod'][1]
    if last_col not in 'ABCDEF' or last_line not in '1234567' or last_col == '' or last_line == '':
        return 'none'
    pod_col = ord(data['sel_pod'][0])
    pod_line = ord(data['sel_pod'][1])
    square_col = ord(col)
    square_line = ord(line)
    if chr(square_col) in board.keys() and chr(square_line) in board[chr(square_col)].keys():
        if last_col in board.keys() and last_line in board[last_col].keys():
            if board[chr(square_col)][chr(square_line)]:
                if board[last_col][last_line]['prongs'][
                  'N'] is True and square_line - pod_line == -1 and pod_col == square_col:
                    if chr(pod_line - 2) in board[chr(pod_col)].keys():
                        if not board[chr(pod_col)][chr(pod_line - 2)]:
                            return 'N'
                elif board[last_col][last_line]['prongs'][
                  'NW'] is True and square_line - pod_line == -1 and pod_col - square_col == 1:
                    if chr(pod_col - 2) in board.keys() and chr(pod_line - 2) in board[chr(pod_col - 2)].keys():
                        if not board[chr(pod_col - 2)][chr(pod_line - 2)]:
                            return 'NW'
                elif board[last_col][last_line]['prongs'][
                  'W'] is True and pod_col - square_col == 1 and pod_line == square_line:
                    if chr(pod_col - 2) in board.keys():
                        if not board[chr(pod_col - 2)][chr(pod_line)]:
                            return 'W'
                elif board[last_col][last_line]['prongs'][
                  'NE'] is True and square_line - pod_line == -1 and pod_col - square_col == -1:
                    if chr(pod_col + 2) in board.keys() and chr(pod_line - 2) in board[chr(pod_col + 2)].keys():
                        if not board[chr(pod_col + 2)][chr(pod_line - 2)]:
                            return 'NE'
                elif board[last_col][last_line]['prongs'][
                  'E'] is True and pod_col - square_col == -1 and square_line == pod_line:
                    if chr(pod_col + 2) in board.keys():
                        if not board[chr(pod_col + 2)][chr(pod_line)]:
                            return 'E'
                elif board[last_col][last_line]['prongs'][
                  'S'] is True and square_line - pod_line == 1 and pod_col == square_col:
                    if chr(pod_line + 2) in board[chr(pod_col)].keys():
                        if not board[chr(pod_col)][chr(pod_line + 2)]:
                            return 'S'
                elif board[last_col][last_line]['prongs'][
                  'SE'] is True and square_line - pod_line == 1 and pod_col - square_col == -1:
                    if chr(pod_col + 2) in board.keys() and chr(pod_line + 2) in board[chr(pod_col + 2)].keys():
                        if not board[chr(pod_col + 2)][chr(pod_line + 2)]:
                            return 'SE'
                elif board[last_col][last_line]['prongs'][
                  'SW'] is True and square_line - pod_line == 1 and pod_col - square_col == 1:
                    if chr(pod_col - 2) in board.keys() and chr(pod_line + 2) in board[chr(pod_col - 2)].keys():
                        if not board[chr(pod_col - 2)][chr(pod_line + 2)]:
                            return 'SW'
    return 'none'


def win_wait():  # wait for short period after win
    start_time = time.time()
    seconds = 3
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data['run'] = False
                pygame.quit()
                sys.exit()
        if elapsed_time > seconds:
            break
    main()


def count_pods():  # count pods on board for each player
    green = 0
    red = 0
    for col in board.keys():
        for line in board[col].keys():
            if board[col][line]:
                player = board[col][line]['player']
                if player == 'green':
                    green += 1
                elif player == 'red':
                    red += 1
    return green, red


def check_win():  # check for each player winning
    for col in 'BCDE':
        if board[col]['2']:
            if board[col]['2']['player'] == 'green':
                draw_win_text(WINNER_GREEN)
                pygame.display.update()
                win_wait()
        if board[col]['6']:
            if board[col]['6']['player'] == 'red':
                draw_win_text(WINNER_RED)
                pygame.display.update()
                win_wait()
    nr = count_pods()
    if nr[0] == 0:
        draw_win_text(WINNER_RED)
        pygame.display.update()
        win_wait()
    if nr[1] == 0:
        draw_win_text(WINNER_GREEN)
        pygame.display.update()
        win_wait()


def end_turn():
    deselect()
    data['capturing'] = False
    if data['turn'] == 'green':
        data['turn'] = 'red'
    elif data['turn'] == 'red':
        data['turn'] = 'green'


def can_capture():  # check if selected piece can make any more captures; if not, turn will end
    if data['sel_pod'] == ['', '']:
        return False
    col = data['sel_pod'][0]
    line = data['sel_pod'][1]
    can = False
    positions = {'N': (col, chr(ord(line) - 1)),
                 'NW': (chr(ord(col) - 1), chr(ord(line) - 1)),
                 'W': (chr(ord(col) - 1), line),
                 'SW': (chr(ord(col) - 1), chr(ord(line) + 1)),
                 'S': (col, chr(ord(line) + 1)),
                 'SE': (chr(ord(col) + 1), chr(ord(line) + 1)),
                 'E': (chr(ord(col) + 1), line),
                 'NE': (chr(ord(col) + 1), chr(ord(line) - 1))}
    for cap_dir in positions.keys():
        if valid_capture(positions[cap_dir][0], positions[cap_dir][1]) != 'none':
            can = True
    return can


def move_pod(dest_col, dest_line):
    col = data['sel_pod'][0]
    line = data['sel_pod'][1]
    pod = board[col][line]
    cap_dir = valid_capture(data['mouse_square'][0], data['mouse_square'][1])
    if cap_dir != 'none':
        data['capturing'] = True
        move_capture(cap_dir)
    elif valid_move():
        if not data['capturing']:
            board[dest_col][dest_line] = pod
            board[col][line] = {}
        end_turn()
    else:
        deselect()


def main():
    init_board()
    last_col = ''
    last_line = ''
    selected = False
    while data['run']:
        clock.tick(FPS)
        if bool(pygame.mouse.get_focused()):  # if mouse on screen, get coordinates
            data['mouse_coords'] = list(pygame.mouse.get_pos())
        x = data['mouse_coords'][0]
        y = data['mouse_coords'][1]
        data['mouse_square'] = list(coords_to_pos(x, y))
        col = data['mouse_square'][0]
        line = data['mouse_square'][1]
        sel = 'none'
        if col in board.keys() and line in board[col].keys():
            if board[col][line]:
                sel = selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data['run'] = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sel not in ('none', 'pod'):
                    if not data['capturing'] and not board[col][line]['prongs'][sel]:
                        if valid_capture(col, line) == 'none':
                            board[col][line]['prongs'][sel] = True
                            end_turn()
                elif sel == 'pod' and not data['capturing'] and valid_capture(col, line) == 'none':
                    selected = True
                    data['sel_pod'] = [col, line]
                last_col = data['sel_pod'][0]
                last_line = data['sel_pod'][1]
                if (last_col != '' and last_line != '') and selected:
                    if last_col != col or last_line != line:
                        move_pod(col, line)
        if data['capturing']:
            if not can_capture():
                end_turn()
        draw_board()
        check_win()


if __name__ == '__main__':
    main()
