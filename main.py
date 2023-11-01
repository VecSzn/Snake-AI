import pygame
import random
from minigame_framework import MiniGameFramework

#Snake小游戏 贪吃蛇
class SnakeGame(MiniGameFramework):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.snake = Snake() 
        self.food = None  #Food Function 还没写

    def handle_events(self):
        super().handle_events()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.snake.change_direction("UP")
        elif keys[pygame.K_s]:
            self.snake.change_direction("DOWN")
        elif keys[pygame.K_a]:
            self.snake.change_direction("LEFT")
        elif keys[pygame.K_d]:
            self.snake.change_direction("RIGHT")
    def update(self):
        self.snake.update(self.food)
        self.food.update() #没写

    def render(self):
        self.display.fill((0, 0, 0))
        self.snake.render(self.display)
        self.food.render(self.display) #没写
        pygame.display.update()
#Snake
class Snake:
    def __init__(self):
        #身体大小/初始方向/颜色
        self.body = [(200, 200)]
        self.direction = (0, -1)
        self.color = (0, 255, 0)

    def change_direction(self, new_direction):
        #更换方向函数
        if new_direction == "UP" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif new_direction == "DOWN" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif new_direction == "LEFT" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif new_direction == "RIGHT" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self, food):
        #更新位置以及长度
        head = self.body[0]
        new_head = (head[0] + self.direction[0] * 20, head[1] + self.direction[1] * 20)

        if new_head[0] < 0 or new_head[0] >= 800 or new_head[1] < 0 or new_head[1] >= 600:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        self.body.insert(0, new_head)

        if new_head == food.position:
            food.generate_new_position()
        else:
            self.body.pop()

    def render(self, display):
        #渲染蛇
        for segment in self.body:
            pygame.draw.rect(display, self.color, (segment[0], segment[1], 20, 20))