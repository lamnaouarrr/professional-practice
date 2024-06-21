import pygame
import random
import sys

#position class to store row and column coordinates
class Position:
    def __init__(self, row, column):
        self.row = row #initialize row
        self.column = column #initialize column

#colors class to store various color constants
class Colors:
    background = (41, 128, 185) #background color
    dashboard = (22, 160, 133) #dashboard color
    dashboard_blocks = (52, 152, 219) #dashboard blocks color
    dark_grey = (26, 31, 40) #dark grey color
    green = (47, 230, 23) #green color
    red = (231, 76, 60) #red color
    orange = (226, 116, 17) #orange color
    yellow = (243, 156, 18) #yellow color
    purple = (166, 0, 247) #purple color
    cyan = (21, 204, 209) #cyan color
    blue = (13, 64, 216) #blue color
    white = (255, 255, 255) #white color
    dark_blue = (44, 44, 127) #dark blue color
    light_blue = (59, 85, 162) #light blue color
    grey = (189, 195, 199) #grey color

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue] #return list of cell colors

#block class to handle block properties and actions
class Block:
    def __init__(self, id):
        self.id = id #initialize block id
        self.cells = {} #initialize cells dictionary
        self.cell_size = 30 #initialize cell size
        self.row_offset = 0 #initialize row offset
        self.column_offset = 0 #initialize column offset
        self.rotation_state = 0 #initialize rotation state
        self.colors = Colors.get_cell_colors() #get cell colors from colors class

    def move(self, rows, columns):
        self.row_offset += rows #update row offset
        self.column_offset += columns #update column offset

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state] #get tiles for current rotation state
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset) #update position with offsets
            moved_tiles.append(position) #append updated position to moved_tiles list
        return moved_tiles #return moved tiles

    def rotate(self):
        self.rotation_state += 1 #increment rotation state
        if self.rotation_state == len(self.cells): #if rotation state exceeds possible states
            self.rotation_state = 0 #reset rotation state

    def undo_rotation(self):
        self.rotation_state -= 1 #decrement rotation state
        if self.rotation_state == -1: #if rotation state is negative
            self.rotation_state = len(self.cells) - 1 #set to last rotation state

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions() #get cell positions
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size,
                                    offset_y + tile.row * self.cell_size, self.cell_size - 1, self.cell_size - 1) #create rectangle for tile
            pygame.draw.rect(screen, self.colors[self.id], tile_rect) #draw tile on screen

#grid class to handle grid properties and actions
class Grid:
    def __init__(self):
        self.num_rows = 20 #initialize number of rows
        self.num_cols = 10 #initialize number of columns
        self.cell_size = 30 #initialize cell size
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)] #initialize grid with zeros
        self.colors = Colors.get_cell_colors() #get cell colors from colors class

    def print_grid(self):
        for row in range(self.num_rows): #iterate through rows
            for column in range(self.num_cols): #iterate through columns
                print(self.grid[row][column], end=" ") #print grid value
            print() #new line after each row

    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols: #check if inside grid boundaries
            return True #return true if inside
        return False #return false if outside

    def is_empty(self, row, column):
        if self.grid[row][column] == 0: #check if cell is empty
            return True #return true if empty
        return False #return false if not empty

    def is_row_full(self, row):
        for column in range(self.num_cols): #iterate through columns
            if self.grid[row][column] == 0: #check if cell is empty
                return False #return false if any cell is empty
        return True #return true if row is full

    def clear_row(self, row):
        for column in range(self.num_cols): #iterate through columns
            self.grid[row][column] = 0 #set cell value to 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols): #iterate through columns
            self.grid[row + num_rows][column] = self.grid[row][column] #move cell value down
            self.grid[row][column] = 0 #set original cell value to 0

    def clear_full_rows(self):
        completed = 0 #initialize completed rows counter
        for row in range(self.num_rows - 1, 0, -1): #iterate through rows from bottom to top
            if self.is_row_full(row): #check if row is full
                self.clear_row(row) #clear row
                completed += 1 #increment completed rows counter
            elif completed > 0: #if there are completed rows
                self.move_row_down(row, completed) #move row down
        return completed #return number of completed rows

    def reset(self):
        for row in range(self.num_rows): #iterate through rows
            for column in range(self.num_cols): #iterate through columns
                self.grid[row][column] = 0 #set cell value to 0

    def draw(self, screen):
        for row in range(self.num_rows): #iterate through rows
            for column in range(self.num_cols): #iterate through columns
                cell_value = self.grid[row][column] #get cell value
                cell_rect = pygame.Rect(column * self.cell_size + 11, row * self.cell_size + 11,
                                        self.cell_size - 1, self.cell_size - 1) #create rectangle for cell
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect) #draw cell on screen

#different tetris blocks
class LBlock(Block):
    def __init__(self):
        super().__init__(id=1)
        self.cells = {
            0: [Position(0, 2), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(2, 1), Position(2, 2)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 0)],
            3: [Position(0, 0), Position(0, 1), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class JBlock(Block):
    def __init__(self):
        super().__init__(id=2)
        self.cells = {
            0: [Position(0, 0), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(0, 2), Position(1, 1), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 2)],
            3: [Position(0, 1), Position(1, 1), Position(2, 0), Position(2, 1)]
        }
        self.move(0, 3)

class IBlock(Block):
    def __init__(self):
        super().__init__(id=3)
        self.cells = {
            0: [Position(1, 0), Position(1, 1), Position(1, 2), Position(1, 3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        self.move(-1, 3)

class OBlock(Block):
    def __init__(self):
        super().__init__(id=4)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 0), Position(1, 1)]
        }
        self.move(0, 4)

class SBlock(Block):
    def __init__(self):
        super().__init__(id=5)
        self.cells = {
            0: [Position(0, 1), Position(0, 2), Position(1, 0), Position(1, 1)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 2)],
            2: [Position(1, 1), Position(1, 2), Position(2, 0), Position(2, 1)],
            3: [Position(0, 0), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class TBlock(Block):
    def __init__(self):
        super().__init__(id=6)
        self.cells = {
            0: [Position(0, 1), Position(1, 0), Position(1, 1), Position(1, 2)],
            1: [Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(1, 2), Position(2, 1)],
             3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 1)]
        }
        self.move(0, 3)

class ZBlock(Block):
    def __init__(self):
        super().__init__(id=7)
        self.cells = {
            0: [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 2)],
            1: [Position(0, 2), Position(1, 1), Position(1, 2), Position(2, 1)],
            2: [Position(1, 0), Position(1, 1), Position(2, 1), Position(2, 2)],
            3: [Position(0, 1), Position(1, 0), Position(1, 1), Position(2, 0)]
        }
        self.move(0, 3)

#game class to manage game state and actions
class Game:
    def __init__(self):
        self.grid = Grid() #initialize grid
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()] #initialize list of blocks
        self.current_block = self.get_random_block() #get initial random block
        self.next_block = self.get_random_block() #get next random block
        self.game_over = False #initialize game over state
        self.score = 0 #initialize score

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1: #if one line is cleared
            self.score += 100 #add 100 to score
        elif lines_cleared == 2: #if two lines are cleared
            self.score += 300 #add 300 to score
        elif lines_cleared == 3: #if three lines are cleared
            self.score += 500 #add 500 to score
        self.score += move_down_points #add move down points to score

    def get_random_block(self):
        if len(self.blocks) == 0: #if no blocks are left
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()] #reinitialize blocks list
        block = random.choice(self.blocks) #choose random block
        self.blocks.remove(block) #remove chosen block from list
        return block #return chosen block

    def move_left(self):
        self.current_block.move(0, -1) #move block left
        if self.block_inside() == False or self.block_fits() == False: #if block is outside or doesn't fit
            self.current_block.move(0, 1) #undo move

    def move_right(self):
        self.current_block.move(0, 1) #move block right
        if self.block_inside() == False or self.block_fits() == False: #if block is outside or doesn't fit
            self.current_block.move(0, -1) #undo move

    def move_down(self):
        self.current_block.move(1, 0) #move block down
        if self.block_inside() == False or self.block_fits() == False: #if block is outside or doesn't fit
            self.current_block.move(-1, 0) #undo move
            self.lock_block() #lock block

    def lock_block(self):
        tiles = self.current_block.get_cell_positions() #get cell positions
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id #lock block in grid
        self.current_block = self.next_block #set current block to next block
        self.next_block = self.get_random_block() #get new next block
        rows_cleared = self.grid.clear_full_rows() #clear full rows
        self.update_score(rows_cleared, 0) #update score
        if self.block_fits() == False: #if block doesn't fit
            self.game_over = True #set game over state

    def reset(self):
        self.grid.reset() #reset grid
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()] #reinitialize blocks list
        self.current_block = self.get_random_block() #get initial random block
        self.next_block = self.get_random_block() #get next random block
        self.score = 0 #reset score

    def block_fits(self):
        tiles = self.current_block.get_cell_positions() #get cell positions
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False: #if cell is not empty
                return False #return false
        return True #return true

    def rotate(self):
        self.current_block.rotate() #rotate block
        if self.block_inside() == False or self.block_fits() == False: #if block is outside or doesn't fit
            self.current_block.undo_rotation() #undo rotation

    def block_inside(self):
        tiles = self.current_block.get_cell_positions() #get cell positions
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False: #if cell is outside
                return False #return false
        return True #return true

    def draw(self, screen):
        self.grid.draw(screen) #draw grid
        self.current_block.draw(screen, 11, 11) #draw current block

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290) #draw next block for IBlock
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280) #draw next block for OBlock
        else:
            self.next_block.draw(screen, 270, 270) #draw next block for other blocks

pygame.init()

arcade_font = pygame.font.Font("PressStart2P.ttf", 20) #load arcade font
large_arcade_font = pygame.font.Font("PressStart2P.ttf", 40) #load large arcade font

score_surface = arcade_font.render("SCORE", True, Colors.yellow) #render score text
next_surface = arcade_font.render("NEXT", True, Colors.yellow) #render next text
game_over_surface = large_arcade_font.render("GAME OVER", True, Colors.red) #render game over text
click_to_play_surface = arcade_font.render("Click to Play Again", True, Colors.grey) #render click to play again text

score_rect = pygame.Rect(320, 55, 170, 60) #create score rectangle
next_rect = pygame.Rect(320, 215, 170, 180) #create next rectangle

screen = pygame.display.set_mode((500, 620)) #set display mode
pygame.display.set_caption("Tetris by LAMNAOUAR AYOUB") #set window caption

icon = pygame.image.load("cube-outline.png") #load window icon
pygame.display.set_icon(icon) #set window icon

clock = pygame.time.Clock() #create clock object

game = Game() #create game object

GAME_UPDATE = pygame.USEREVENT #define game update event
pygame.time.set_timer(GAME_UPDATE, 200) #set timer for game update event

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if quit event
            pygame.quit() #quit pygame
            sys.exit() #exit system
        if event.type == pygame.KEYDOWN:
            if game.game_over: #if game is over
                game.game_over = False #reset game over state
                game.reset() #reset game
            if event.key == pygame.K_LEFT and not game.game_over: #if left key pressed
                game.move_left() #move block left
            if event.key == pygame.K_RIGHT and not game.game_over: #if right key pressed
                game.move_right() #move block right
            if event.key == pygame.K_DOWN and not game.game_over: #if down key pressed
                game.move_down() #move block down
                game.update_score(0, 1) #update score
            if event.key == pygame.K_UP and not game.game_over: #if up key pressed
                game.rotate() #rotate block
        if event.type == pygame.MOUSEBUTTONDOWN and game.game_over: #if mouse button pressed
            game.game_over = False #reset game over state
            game.reset() #reset game
        if event.type == GAME_UPDATE and not game.game_over: #if game update event
            game.move_down() #move block down

    screen.fill(Colors.background) #fill screen with background color
    
    if game.game_over:
        game_over_rect = game_over_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50)) #get game over text rect
        click_to_play_rect = click_to_play_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50)) #get click to play again text rect
        final_score_surface = arcade_font.render(f"Score: {game.score}", True, Colors.yellow) #render final score text
        final_score_rect = final_score_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2)) #get final score text rect
        screen.blit(game_over_surface, game_over_rect) #blit game over text
        screen.blit(final_score_surface, final_score_rect) #blit final score text
        screen.blit(click_to_play_surface, click_to_play_rect) #blit click to play again text
    else:
        score_value_surface = arcade_font.render(str(game.score), True, Colors.yellow) #render score value text
        screen.blit(score_surface, score_surface.get_rect(centerx=score_rect.centerx, top=20)) #blit score text
        screen.blit(next_surface, next_surface.get_rect(centerx=next_rect.centerx, top=180)) #blit next text
        pygame.draw.rect(screen, Colors.dashboard_blocks, score_rect) #draw score rectangle
        pygame.draw.rect(screen, Colors.dashboard_blocks, next_rect) #draw next rectangle
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery)) #blit score value text
        game.draw(screen) #draw game

    pygame.display.update() #update display
    clock.tick(60) #tick clock
