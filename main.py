import pygame
import random
import numpy as np
from minigame_framework import MiniGameFramework
import time
import matplotlib.pyplot as plt


# Snake Game
class SnakeGame(MiniGameFramework):
    def __init__(self, width, height, speed, name):
        super().__init__(width, height, speed, name)
        self.snake = Snake()
        self.food = Food()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def render(self):
        self.display.fill((0, 0, 0))
        self.snake.render(self.display)
        self.food.render(self.display)

        pygame.display.update()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()

    def get_state(self):
        head = self.snake.body[0]
        new_head = (
            head[0] + self.snake.direction[0] * 40,
            head[1] + self.snake.direction[1] * 40,
        )
        new__head = (
            head[0] + self.snake.direction[0] * 60,
            head[1] + self.snake.direction[1] * 60,
        )
        new___head = (
            head[0] + self.snake.direction[0] * 80,
            head[1] + self.snake.direction[1] * 80,
        )
        new____head = (
            head[0] + self.snake.direction[0] * 100,
            head[1] + self.snake.direction[1] * 100,
        )
        state = [
            self.snake.direction_n,  # Direction
            int(self.food.position[1] < head[1]),  # Food positions
            int(self.food.position[1] > head[1]),
            int(self.food.position[0] < head[0]),
            int(self.food.position[0] > head[0]),
            int(game.snake.is_danger(new_head)),  # Dangers around
            int(game.snake.is_danger(new__head)),
            int(game.snake.is_danger(new___head)),
            int(game.snake.is_danger(new____head)),
            int(game.snake.is_danger((head[0], head[1] - 20))),  # Dangers around
            int(game.snake.is_danger((head[0], head[1] + 20))),
            int(game.snake.is_danger((head[0] - 20, head[1]))),
            int(game.snake.is_danger((head[0] + 20, head[1]))),
        ]
        return tuple(state)

    def get_distance(self):
        head = self.snake.body[0]
        distance = (
            abs(head[0] - self.food.position[0]),
            abs(head[1] - self.food.position[1]),
        )
        return distance


class Snake:
    def __init__(self):
        self.body = [(200, 200)]
        self.direction = (0, -1)
        self.color = (0, 255, 0)
        self.direction_n = 0
        self.step_without_food = 0

    def is_out_of_bounds(self, head):
        return (
            head[0] < 0
            or head[0] >= game.width
            or head[1] < 0
            or head[1] >= game.height
        )

    def check_collision(self, head):
        if head in self.body[1:]:
            return True
        return False

    def is_danger(self, head):
        if self.check_collision(head) or self.is_out_of_bounds(head):
            return True

        return False

    def change_direction(self):
        if self.direction_n == 0:
            self.direction = (0, -1)
        elif self.direction_n == 1:
            self.direction = (0, 1)
        elif self.direction_n == 2:
            self.direction = (-1, 0)
        elif self.direction_n == 3:
            self.direction = (1, 0)

    def update(self, action):
        self.direction_n = action
        self.change_direction()
        head = self.body[0]
        new_head = (head[0] + self.direction[0] * 20, head[1] + self.direction[1] * 20)
        done = False

        if self.is_danger(new_head) or self.step_without_food > 1000:
            done = True
            reward = -10

        else:
            current_dis = game.get_distance()
            self.body.insert(0, new_head)
            new_dis = game.get_distance()
            self.step_without_food += 1
            if new_dis[0] < current_dis[0] or new_dis[1] < current_dis[1]:
                reward = 0.2
            else:
                reward = -1

            if new_head == game.food.position:
                reward = 1

                while game.food.position in self.body:
                    game.food.generate_new_position()
                    self.step_without_food = 0
            else:
                self.body.pop()
        return (game.get_state(), reward, done)

    def render(self, display):
        for segment in self.body:
            pygame.draw.rect(display, self.color, (segment[0], segment[1], 20, 20))


class Food:
    def __init__(self):
        self.position = (400, 300)
        self.color = (255, 0, 0)
        self.generate_new_position()

    def generate_new_position(self):
        x = random.randint(0, 39) * 20
        y = random.randint(0, 29) * 20
        self.position = (x, y)

    def render(self, display):
        pygame.draw.rect(
            display, self.color, (self.position[0], self.position[1], 20, 20)
        )


game = SnakeGame(800, 600, 60, "Snake Game")
game.initialize()
