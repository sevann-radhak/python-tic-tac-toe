import pygame
from pygame.locals import *

class TicTacToe:
    def __init__(self):
        self.markers = self.init_markers()
        self.player = 1
        self.game_is_over = False

    def init_markers(self):
        return [[0, 0, 0] for _ in range(3)]

    def reset_markers(self):
        for i in range(len(self.markers)):
            for j in range(len(self.markers[i])):
                self.markers[i][j] = 0

    def check_winner(self):
        for i in range(3):
            if self.markers[i][0] == self.markers[i][1] == self.markers[i][2] == self.player:
                return True
            if self.markers[0][i] == self.markers[1][i] == self.markers[2][i] == self.player:
                return True
        if self.markers[0][0] == self.markers[1][1] == self.markers[2][2] == self.player:
            return True
        if self.markers[0][2] == self.markers[1][1] == self.markers[2][0] == self.player:
            return True
        return False

class GameDisplay:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen_width = 300
        self.screen_height = 300
        self.again_rect = pygame.Rect(self.screen_width // 2 - 80, self.screen_height // 2, 160, 50)
        self.font = pygame.font.SysFont(None, 40)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Tic Tac Toe Game')

    def draw_grid(self):
        bg = (255, 255, 200)
        grid = (50, 50, 50)
        self.screen.fill(bg) 
        line_width = 6
        border = 15
        for x in range(1, 3):
            pygame.draw.line(self.screen, grid, (border, x*100), (self.screen_width - border, x*100), line_width)
            pygame.draw.line(self.screen, grid, (x*100, border), (x*100, self.screen_height - border), line_width)

    def draw_markers(self):
        red = (255, 0, 0)
        green = (0, 255, 0)
        line_width = 15
        for x_pos, x in enumerate(self.game.markers):
            for y_pos, y in enumerate(x):
                if y == 1:
                    pygame.draw.line(self.screen, red, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
                    pygame.draw.line(self.screen, red, (x_pos * 100 + 85, y_pos * 100 + 15), (x_pos * 100 + 15, y_pos * 100 + 85), line_width)
                if y == -1:
                    pygame.draw.circle(self.screen, green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)

    def draw_winner(self):
        win_text = 'Player 1 wins!' if self.game.player == 1 else 'Player 2 wins!'
        win_img = self.font.render(win_text, True, (0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.screen_width // 2 - 100, self.screen_height // 2 - 50, 200, 100))
        self.screen.blit(win_img, (self.screen_width // 2 - 100, self.screen_height // 2 - 50))
        play_again_text = 'Play again?'
        play_again_img = self.font.render(play_again_text, True, (0, 0, 0))
        pygame.draw.rect(self.screen, (0, 255, 0), self.again_rect)
        self.screen.blit(play_again_img, (self.screen_width // 2 - 80, self.screen_height // 2 + 10))

    def run(self):
        clicked = False
        while True:       
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if self.game.game_is_over:
                    if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
                        clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and clicked:
                        clicked = False
                        pos = pygame.mouse.get_pos()
                        if self.again_rect.collidepoint(pos):
                            self.game.reset_markers()
                            self.game.player = 1
                            self.game.game_is_over = False
                else:    
                    self.draw_grid()
                    self.draw_markers()
                    if event.type == pygame.MOUSEBUTTONDOWN and not clicked:
                        clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and clicked:
                        clicked = False
                        pos = pygame.mouse.get_pos()
                        cell_x, cell_y = pos[0] // 100, pos[1] // 100        
                        if self.game.markers[cell_x][cell_y] == 0:
                            self.game.markers[cell_x][cell_y] = self.game.player
                            if self.game.check_winner():
                                self.game.game_is_over = True
                                self.draw_markers()          
                                self.draw_winner()
                            self.game.player *= -1
                pygame.display.update()

game = TicTacToe()
display = GameDisplay(game)
display.run()