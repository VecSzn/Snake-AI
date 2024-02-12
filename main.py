import pygame
import random
import numpy as np
from dqn import Agent
from minigame_framework import MiniGameFramework


# Snake Game
class SnakeGame(MiniGameFramework):
    def __init__(self, width, height, speed, name, pixel_size):
        super().__init__(width, height, speed, name, pixel_size)
        self.reset_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def render(self):
        self.display.fill((0, 0, 0))
        self.snake.render(self.display)
        self.food.render(self.display)

        pygame.display.update()
        self.clock.tick(self.speed)

    def reset_game(self):
        self.snake = Snake(self.width, self.height)
        self.food = Food(self.width, self.height, self.pixel_size)
        self.img = np.zeros((self.height, self.width, 1))

    def get_state(self):
        head = self.snake.body[0]
        state = [
            int(self.food.position[1] < head[1]),  # Food positions
            int(self.food.position[1] > head[1]),
            int(self.food.position[0] < head[0]),
            int(self.food.position[0] > head[0]),
            int(self.snake.is_danger((head[0], head[1] - 20))),  # Dangers around
            int(self.snake.is_danger((head[0], head[1] + 20))),
            int(self.snake.is_danger((head[0] - 20, head[1]))),
            int(self.snake.is_danger((head[0] + 20, head[1]))),
        ]
        return state

    def get_distance(self):
        head = self.snake.body[0]
        distance = np.sqrt(
            np.square(head[0] - self.food.position[0])
            + np.square(head[1] - self.food.position[1])
        )
        return distance


class Snake:
    def __init__(self, width, height):
        self.body = [(width * 10, height * 10)]
        self.direction = (0, -1)
        self.color = (0, 255, 0)
        self.step_without_food = 0
        self.direction = (0, -1)

    def is_out_of_bounds(self, head):
        return (
            head[0] < 0
            or head[0] >= game.width * game.pixel_size
            or head[1] < 0
            or head[1] >= game.height * game.pixel_size
        )

    def check_collision(self, head):
        if head in self.body[1:]:
            return True
        return False

    def is_danger(self, head):
        if self.check_collision(head) or self.is_out_of_bounds(head):
            return True

        return False

    def change_direction(self, action):
        if action == 0 and self.direction != (0, 1):
            self.direction = (0, -1)
        elif action == 1 and self.direction != (0, -1):
            self.direction = (0, 1)
        elif action == 2 and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif action == 3 and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self, action):
        self.change_direction(action)
        head = self.body[0]
        reward = -0.2
        current_dis = game.get_distance()
        new_head = (
            head[0] + self.direction[0] * game.pixel_size,
            head[1] + self.direction[1] * game.pixel_size,
        )
        done = False

        if self.is_danger(new_head) or self.step_without_food > 1000:
            done = True
            reward = -1

        else:
            self.body.insert(0, new_head)
            self.step_without_food += 1

            dis = game.get_distance()
            if current_dis > dis:
                reward = 0.1

            if new_head == game.food.position:
                reward = 1
                while game.food.position in self.body:
                    game.food.generate_new_position()

                self.step_without_food = 0
            else:
                self.body.pop()

        return (game.get_state(), done, reward)

    def render(self, display):
        for segment in self.body:
            pygame.draw.rect(
                display,
                self.color,
                (segment[0], segment[1], game.pixel_size, game.pixel_size),
            )


class Food:
    def __init__(self, width, height, pixel_size):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.generate_new_position()

    def generate_new_position(self):
        x = random.randint(0, self.width - 1) * self.pixel_size
        y = random.randint(0, self.height - 1) * self.pixel_size
        self.position = (x, y)

    def render(self, display):
        pygame.draw.rect(
            display,
            self.color,
            (self.position[0], self.position[1], game.pixel_size, game.pixel_size),
        )


game = SnakeGame(40, 30, 20, "Snake Game", 20)
game.initialize()

agent = Agent()
steps = 0

average = []
for i in range(1, 10000 + 1):
    render = False
    game.reset_game()
    current_state = game.get_state()
    done = False

    if not i % 25:
        print(f"Episode: {i}")
        print(f"Average Score {np.average(average)}")
        print(f"Epsilon: {agent.epsilon}")
        print()
        render = True
        average = []

        if agent.epsilon < 0.03:
            agent.epsilon = 0

    while not done:
        game.handle_events()
        action = agent.get_action(current_state)
        state, done, reward = game.snake.update(action)
        agent.add(current_state, action, reward, state)
        current_state = state
        if render:
            game.render()
        steps += 1

    average.append(len(game.snake.body))
    batch = agent.batching(64)
    agent.train(batch)
