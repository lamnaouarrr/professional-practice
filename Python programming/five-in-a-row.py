import os
import re
import pygame
import sys
from pygame import gfxdraw

#ensure the working directory is the same as the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

class Game:
    WIDTH = 501
    HEIGHT = 502
    BOARD_SIZE = min(WIDTH, HEIGHT)

    SIZE = 13  #fixed board size 13x13
    sq_w = (BOARD_SIZE - 1) // SIZE
    text_size = (BOARD_SIZE - 1) // 8
    ts1 = 0.01
    ts2 = 0.005
    ts3 = 0.003
    ts4 = 0.003

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 99, 71)  # Soft red color for the background
    DARK_SLATE_GREY = (45, 52, 54)  # Color #2d3436
    ORANGE = (211, 84, 0)  # Color #d35400
    BOARD = (211, 211, 211)  # Light grey color for the board

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Five In A Row by LAMNAOUAR AYOUB")

        # Load the icon
        icon_path = 'crown.png'
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)  # Set the window icon

        self.screen.fill(self.BOARD)
        pygame.display.flip()

        self.font_name = pygame.font.match_font('Comic Sans MS')
        self.board = Board(self.SIZE)
        self.prev_move = None
        self.moves = 0
        self.current_player = 'X'
        self.running = True
        self.render()  # Ensure the board is rendered upon initialization
        self.main_loop()

    def draw_text(self, surf, text, size, x, y, color=ORANGE):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (int(x), int(y))
        surf.blit(text_surface, text_rect)

    def render(self):
        self.screen.fill(self.BLACK)
        rect = pygame.Surface((self.sq_w - 1, self.sq_w - 1)).get_rect()
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                center = (int(i * self.BOARD_SIZE / self.SIZE) + self.sq_w // 2 + (self.WIDTH - self.BOARD_SIZE) // 2,
                          int(j * self.BOARD_SIZE / self.SIZE) + self.sq_w // 2 + (self.HEIGHT - self.BOARD_SIZE) // 2)
                rect.center = center
                color = self.board.rows[i][j]
                pygame.draw.rect(self.screen, self.BOARD, rect)
                if color == 'O':
                    if self.prev_move == (i, j):
                        gfxdraw.filled_circle(self.screen, center[0], center[1], int(self.sq_w * 0.4), self.BLACK)
                        gfxdraw.aacircle(self.screen, center[0], center[1], int(self.sq_w * 0.4), self.BLUE)
                    else:
                        gfxdraw.filled_circle(self.screen, center[0], center[1], int(self.sq_w * 0.4), self.BLACK)
                        gfxdraw.aacircle(self.screen, center[0], center[1], int(self.sq_w * 0.4), self.BLACK)
                if color == 'X':
                    gfxdraw.filled_circle(self.screen, center[0], center[1], int(self.sq_w * 0.4), self.WHITE)
                    gfxdraw.aacircle(self.screen, center[0], center[1], int(self.sq_w * 0.4), self.WHITE)
        pygame.display.flip()

    def game_over(self, winner, moves):
        text = ''
        if winner == 'X':
            text = 'White player won in ' + str(moves) + ' moves'
        elif winner == 'O':
            text = 'Black player won in ' + str(moves) + ' moves'
        elif winner == 'p':
            text = 'You stopped after ' + str(moves) + ' turns'
        else:
            text = 'DRAW!'
        self.screen.fill(self.DARK_SLATE_GREY)  # Set the background color to #2d3436
        self.shadowed_text('GAME OVER', 1.3 * self.text_size, min(self.WIDTH, 800) * self.ts1, -2.0 * self.text_size)
        self.shadowed_text(text, 0.6 * self.text_size, min(self.WIDTH, 800) * self.ts2, -0.8 * self.text_size)
        self.shadowed_text('Click to play again', 0.4 * self.text_size, min(self.WIDTH, 800) * self.ts3, 0.6 * self.text_size)
        pygame.display.flip()

    def shadowed_text(self, text, size, shadow, offset=0, reversed=False):
        size = int(size)
        shadow = int(shadow)
        offset = int(offset)
        self.draw_text(self.screen, text, size, self.WIDTH / 2, self.HEIGHT / 2 + offset, self.ORANGE)

    def resize(self, event):
        surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        self.WIDTH = event.w
        self.HEIGHT = event.h
        self.BOARD_SIZE = min(self.WIDTH, self.HEIGHT)
        self.sq_w = (self.BOARD_SIZE) // self.SIZE
        self.text_size = (self.BOARD_SIZE - 1) // 8
        self.render()
        self.game_over('p', self.moves)
        pygame.display.flip()

    def main_loop(self):
        while self.running:
            waiting = True
            restart_game = False
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        inp = pygame.mouse.get_pos()
                        inp = [int((inp[0] - (self.WIDTH - self.BOARD_SIZE) / 2) / self.BOARD_SIZE * self.SIZE),
                               int((inp[1] - (self.HEIGHT - self.BOARD_SIZE) / 2) / self.BOARD_SIZE * self.SIZE)]
                        try:
                            if inp[0] < 0 or inp[1] < 0 or self.board.rows[inp[0]][inp[1]] != '_': raise ValueError
                            self.board.set(inp, self.current_player)
                            self.render()
                            waiting = False
                        except:
                            pass
                    if event.type == pygame.VIDEORESIZE:
                        self.resize(event)

            if restart_game: continue

            result = self.board.check()
            self.moves += 1
            if result is not None:
                self.render()
                self.game_over(result, self.moves)
                pygame.display.flip()
                waiting = True
                render_text = True
                while waiting:
                    space_pressed = False
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                space_pressed = True
                        if event.type == pygame.QUIT:
                            self.running = False
                            waiting = False
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            waiting = False
                        if event.type == pygame.VIDEORESIZE:
                            self.resize(event)
                    if space_pressed:
                        render_text = not render_text
                        if render_text:
                            self.game_over(result, self.moves)
                            pygame.display.flip()
                        else:
                            self.render()
                self.board = Board(self.SIZE)
                self.sq_w = (self.BOARD_SIZE - 1) // self.SIZE
                self.moves = 0
                self.prev_move = None

            self.current_player = 'O' if self.current_player == 'X' else 'X'

            self.render()
        pygame.quit()

class Board:
    def __init__(self, size):
        self.size = size
        self.rows = self.empty_arr(size, size, '_')
        self.columns = self.get_columns(self.rows)
        self.diagonal_1 = self.get_diagonals(self.rows)
        self.diagonal_2 = self.get_diagonals(self.rows, True)
        self.scoreing_dic = {
            '_XX(?=(_))': -4, '_XX(?=(O))': -2, 'OXX(?=(_))': -2, 'OXX(?=(O))': -1, '__XXX(?=(_))': -100, '_XXX(?=(__))': -100,
            '_XX_X(?=(_))': -100, '_X_XX(?=(_))': -100, 'XXXX(?=(_))': -400,
            'XXX_X': -400, 'XX_XX': -400, 'X_XXX': -400, '_XXXX': -400, 'XXXXX': -1600, '_OO(?=(_))': 3, '_OO(?=(X))': 2,
            'XOO(?=(_))': 2, 'XOO(?=(X))': 1, '__OOO(?=(_))': 15, '_OOO(?=(__))': 15,
            '_OO_O(?=(_))': 12, '_O_OO(?=(_))': 12, 'OOOO(?=(_))': 155, 'OOO_O': 150, 'OO_OO': 150, 'O_OOO': 150, '_OOOO': 155,
            'OOOOO': 2000, 'OX': 1, 'XO': 1
        }

    def empty_arr(self, l, w, fill=0):
        return [[fill for _ in range(w)] for _ in range(l)]

    def get_columns(self, arr):
        return [[j[i] for j in arr] for i in range(len(arr[0]))]

    def get_diagonals(self, arr, od=False):
        if od:
            arr = [list(reversed(i)) for i in arr]
        n = len(arr) + len(arr[0]) - 1
        res = []
        for i in range(n):
            l = []
            x = i
            while x >= 0:
                try:
                    l.append(arr[x][i - x])
                except(IndexError):
                    pass
                finally:
                    x -= 1
            if od:
                l.reverse()
            res.append(l)
        return res

    def update(self):
        self.diagonal_1 = self.get_diagonals(self.rows)
        self.diagonal_2 = self.get_diagonals(self.rows, True)

    def set(self, pos, color):
        self.rows[pos[0]][pos[1]] = color
        self.columns[pos[1]][pos[0]] = color
        self.update()

    def check(self):
        draw = all('_' not in row for row in self.rows)
        if draw: return '?'
        for orientation in [self.rows, self.columns, self.diagonal_1, self.diagonal_2]:
            for line in orientation:
                if 'XXXXX' in ''.join(line):
                    return 'X'
                elif 'OOOOO' in ''.join(line):
                    return 'O'
        return None

    def score(self):
        score = 0
        for orientation in [self.rows, self.columns, self.diagonal_1, self.diagonal_2]:
            for line in orientation:
                strng = ''.join(line)
                for pattern, value in self.scoreing_dic.items():
                    score += value * len(re.findall(pattern, strng))
        return score

if __name__ == "__main__":
    Game()
