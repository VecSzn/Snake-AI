import pygame


# 我的第一个PyGame游戏框架
class MiniGameFramework:
    def __init__(self, width, height, speed, name):
        self.width = width
        self.height = height
        self.is_running = False
        self.display = None
        self.speed = speed
        self.name = name
        self.clock = pygame.time.Clock()

    def initialize(self):
        pygame.init()
        pygame.display.set_caption(self.name)
        self.display = pygame.display.set_mode((self.width, self.height))
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        pass

    def render(self):
        pass

    def run(self):
        self.initialize()

        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.speed)

        pygame.quit()
