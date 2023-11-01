#我的第一个py游戏框架 using pygame
import pygame

#Game Class
#Usage Game()
class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.is_running = False
        self.display = None

    def initialize(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        pass
    # Render Place
    def render(self):
        self.display.fill((0, 0, 0))
        pygame.display.update()
    #Run Game Place
    def run(self):
        self.initialize()

        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()
