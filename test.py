import pygame
import random
import numpy as np
import time
from matplotlib import pyplot as plt
from minigame_framework import MiniGameFramework


# Snake Game
class SnakeGame(MiniGameFramework):
    def __init__(self, width, height, speed, name):
        super().__init__(width, height, speed, name)
        self.snake = Snake()
        self.food = Food()
        self.new_direction = 0
        self.step_without_food = 0

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
            head[0] + self.snake.direction[0] * 20,
            head[1] + self.snake.direction[1] * 20,
        )
        state = [
            self.new_direction,
            int(self.food.position[1] > head[1]),
            int(self.food.position[1] < head[1]),
            int(self.food.position[0] < head[0]),
            int(self.food.position[0] > head[0]),
            int(game.snake.is_danger((new_head[0], new_head[1] - 20))),
            int(game.snake.is_danger((new_head[0], new_head[1] + 20))),
            int(game.snake.is_danger((new_head[0] - 20, new_head[1]))),
            int(game.snake.is_danger((new_head[0] + 20, new_head[1]))),
        ]
        return tuple(state)

    def get_distance(self):
        distance = (
            abs(game.snake.body[0][0] - game.food.position[0]),
            abs(game.snake.body[0][1] - game.food.position[1]),
        )
        return distance


class Snake:
    def __init__(self):
        self.body = [(200, 200)]
        self.direction = (0, -1)
        self.color = (0, 255, 0)
        self.direction_n = 0

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

    def change_direction(self, new_direction):
        if new_direction == 0 and self.direction != (0, 1):
            self.direction = (0, -1)
        elif new_direction == 1 and self.direction != (0, -1):
            self.direction = (0, 1)
        elif new_direction == 2 and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif new_direction == 3 and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self, action):
        self.direction_n = action
        self.change_direction(action)
        head = self.body[0]
        new_head = (head[0] + self.direction[0] * 20, head[1] + self.direction[1] * 20)

        eat = False
        done = False

        if self.is_danger(new_head) or game.step_without_food > 1000:
            game.step_without_food = 0
            done = True

        if not done:
            self.body.insert(0, new_head)

            game.step_without_food += 1

            if new_head == game.food.position:
                game.step_without_food = 0
                eat = True
            else:
                self.body.pop()

        distance = game.get_distance()

        return (game.get_state(), distance, eat, done)

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

    def update(self):
        pass

    def render(self, display):
        pygame.draw.rect(
            display, self.color, (self.position[0], self.position[1], 20, 20)
        )


class QTable:
    def __init__(self):
        self.qtable = np.zeros([4] + [2] * 8 + [4])
        self.learning_rate = 0.01
        self.discount = 0.95
        self.epsilon = 1
        self.eps_discount = 0.999

    def choose_action(self, state):
        if random.random() > self.epsilon:
            return np.argmax(self.qtable[state])
        else:
            return random.choice([0, 1, 2, 3])

    def update(self, reward, state, new_state, action, done):
        # for i in range(len(states)):
        #     state, action, done = states[i]
        #     last = False
        #     if i + 1 == len(states):
        #         last = True

        if not done:
            # if not last:
            #     new_state, _, _ = states[i + 1]
            new_q = (1 - self.learning_rate) * max(
                self.qtable[state]
            ) + self.learning_rate * (
                reward + self.discount * max(self.qtable[new_state])
            )
        else:
            new_q = (1 - self.learning_rate) * max(
                self.qtable[state]
            ) + self.learning_rate * reward
        # if not last:
        self.qtable[state][action] = new_q


game = SnakeGame(800, 600, 30, "Snake Game")
game.initialize()
agent = QTable()
length = []

if __name__ == "__main__":
    for i in range(1, 100000):
        if not game.is_running:
            break

        render = False
        done = False

        current_state = game.get_state()
        current_dis = game.get_distance()
        states = []

        reward = -1
        agent.epsilon = agent.epsilon * agent.eps_discount

        if i % 500 == 0:
            render = True
            print("episodes:", i)
            print(agent.epsilon)
            print(np.average(length))
            length = []

        game.reset_game()
        while not done and game.is_running:
            game.handle_events()
            action = agent.choose_action(current_state)
            new_state, new_dis, eat, done = game.snake.update(action)

            if current_dis[0] > new_dis[0] or current_dis[1] > new_dis[1]:
                reward = 1
            else:
                reward = -1

            if eat:
                game.food.generate_new_position()
                reward = 2
            if done:
                reward = -10

            # states.append((current_state, action, done))
            agent.update(reward, current_state, new_state, action, done)

            current_state = new_state
            current_dis = new_dis
            length.append(len(game.snake.body))

            if render:
                game.render()
                game.clock.tick(game.speed)

        game.reset_game()
