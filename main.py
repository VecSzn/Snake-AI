import pygame
import random
from minigame_framework import MiniGameFramework

#Snake小游戏 贪吃蛇
class SnakeGame(MiniGameFramework):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.snake = None #Snake Function 还没写
        self.food = None  #Food Function 还没写

    def handle_events(self):
        super().handle_events()

    def update(self):
        pass

    def render(self):
        self.display.fill((0, 0, 0))
        pygame.display.update()