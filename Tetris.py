import random
import pygame
import socket
import threading

pygame.font.init()

gesture_command = None

def receive_gesture():
    global gesture_command
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 65432))

    while True:
        data = client.recv(1024).decode()
        gesture_command = data

# global variables
col = 10
row = 20
s_width = 800
s_height = 750
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

filepath = r'c:\gesture_data\highscore.txt'
fontpath = r'c:\gesture_data\arcade.TTF'
fontpath_mario = r'c:\gesture_data\mario.ttf'

S = [['.....','.....','..00.','.00..','.....'],['.....','..0..','..00.','...0.','.....']]
Z = [['.....','.....','.00..','..00.','.....'],['.....','..0..','.00..','.0...','.....']]
I = [['..0..','..0..','..0..','..0..','.....'],['.....','0000.','.....','.....','.....']]
O = [['.....','.....','.00..','.00..','.....']]
J = [['.0...','.000.','.....','.....','.....'],['..00.','..0..','..0..','.....','.....'],
     ['.....','.000.','...0.','.....','.....'],['..0..','..0..','.00..','.....','.....']]
L = [['...0.','.000.','.....','.....','.....'],['..0..','..0..','..00.','.....','.....'],
     ['.....','.000.','.0...','.....','.....'],['.00..','..0..','..0..','.....','.....']]
T = [['..0..','.000.','.....','.....','.....'],['..0..','..00.','..0..','.....','.....'],
     ['.....','.000.','..0..','.....','.....'],['..0..','.00..','..0..','.....','.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(col)] for _ in range(row)]
    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                grid[y][x] = locked_pos[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(shape_format):
        for j, column in enumerate(list(line)):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    accepted_pos = [ (x, y) for y in range(row) for x in range(col) if grid[y][x] == (0, 0, 0)]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_pos and pos[1] >= 0:
            return False
    return True

def check_lost(positions):
    return any(y < 1 for (x, y) in positions)

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2),
                         top_left_y + play_height/2 - (label.get_height()/2)))

def draw_grid(surface):
    for i in range(row):
        pygame.draw.line(surface, (0, 0, 0), (top_left_x, top_left_y + i*block_size),
                         (top_left_x + play_width, top_left_y + i*block_size))
        for j in range(col):
            pygame.draw.line(surface, (0, 0, 0), (top_left_x + j*block_size, top_left_y),
                             (top_left_x + j*block_size, top_left_y + play_height))

def clear_rows(grid, locked):
    rows_to_clear = []
    for i in range(row-1, -1, -1):
        if (0, 0, 0) not in grid[i]:
            rows_to_clear.append(i)
    
    if rows_to_clear:
        for row_index in rows_to_clear:
            for j in range(col):
                try:
                    del locked[(j, row_index)]
                except:
                    continue

        # Aşağıya kaydırma işlemi
        for key in sorted(locked.keys(), key=lambda x: x[1])[::-1]:
            x, y = key
            shift = sum(1 for cleared_row in rows_to_clear if y < cleared_row)
            if shift > 0:
                new_key = (x, y + shift)
                locked[new_key] = locked.pop(key)

    return len(rows_to_clear)


def draw_next_shape(piece, surface):
    font = pygame.font.Font(fontpath, 30)
    label = font.render('Next shape', 1, (255, 255, 255))
    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(shape_format):
        for j, column in enumerate(list(line)):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (start_x + j*block_size, start_y + i*block_size, block_size, block_size), 0)
    surface.blit(label, (start_x, start_y - 30))

def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))
    font = pygame.font.Font(fontpath_mario, 65)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))
    font = pygame.font.Font(fontpath, 30)
    label = font.render('SCORE   ' + str(score), 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width + 50, top_left_y + 200))
    label_hi = font.render('HIGHSCORE   ' + str(last_score), 1, (255, 255, 255))
    surface.blit(label_hi, (top_left_x - 220, top_left_y + 200))
    for i in range(row):
        for j in range(col):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    draw_grid(surface)
    pygame.draw.rect(surface, (255, 255, 255), (top_left_x, top_left_y, play_width, play_height), 4)

def draw_gesture_guide(surface):
    font = pygame.font.Font(fontpath, 20)
    lines = [
        "🎮 Gesture Kontrolleri:",
        "Avuc acik      : Sol",
        "Isaret parmagi : Sag",
        "Yumruk         : Hizli Dusur (DROP)",
        "Like           : Sola Dondur",
        "Dislike        : Saga Dondur",
        "Timeout        : Duraklat Devam"
    ]
    for i, line in enumerate(lines):
        label = font.render(line, 1, (200, 200, 200))
        surface.blit(label, (top_left_x + play_width + 20, 30 + i * 25))

def update_score(new_score):
    score = get_max_score()
    with open(filepath, 'w') as file:
        file.write(str(max(score, new_score)))

def get_max_score():
    with open(filepath, 'r') as file:
        return int(file.readlines()[0].strip())

def main(window):
    threading.Thread(target=receive_gesture, daemon=True).start()
    locked_positions = {}
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 1
    level_time = 0
    score = 0
    last_score = get_max_score()

    global gesture_command
    gesture_text = ""
    gesture_text_timer = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.50:
                fall_speed -= 0.0035

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        if gesture_command:
            gesture_text = gesture_command
            gesture_text_timer = pygame.time.get_ticks()

            if gesture_command == "left":
                current_piece.x -= 1
                if not valid_space(current_piece, grid):
                    current_piece.x += 1
            elif gesture_command == "right":
                current_piece.x += 1
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1
            elif gesture_command == "down":
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
            elif gesture_command == "drop":
                while valid_space(current_piece, grid):
                    current_piece.y += 1
                current_piece.y -= 1
                change_piece = True
            elif gesture_command == "rotate_left":
                current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                if not valid_space(current_piece, grid):
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
            elif gesture_command == "rotate_right":
                current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                if not valid_space(current_piece, grid):
                    current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
            elif gesture_command == "pause":
                paused = True
                draw_text_middle("PAUSED - Show gesture to resume", 30, (255, 255, 255), window)
                pygame.display.update()
                while paused:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    if gesture_command != "pause":
                        paused = False
                    pygame.time.wait(100)
            gesture_command = None

        for x, y in convert_shape_format(current_piece):
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in convert_shape_format(current_piece):
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
            update_score(score)
            if score > last_score:
                last_score = score

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        draw_gesture_guide(window)

        if gesture_text and pygame.time.get_ticks() - gesture_text_timer < 3000:
            font = pygame.font.Font(fontpath, 24)
            label = font.render(f'Gesture: {gesture_text}', 1, (255, 255, 0))
            window.blit(label, (top_left_x + 10, top_left_y - 40))

        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle('You Lost', 40, (255, 255, 255), window)
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()

def main_menu(window):
    threading.Thread(target=receive_gesture, daemon=True).start()
    run = True
    while run:
        draw_text_middle('Press any key to begin', 50, (255, 255, 255), window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                main(window)
    pygame.quit()

if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    main_menu(win)
