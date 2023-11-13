import pygame
import random
import numpy as np
from minigame_framework import MiniGameFramework
import time


# Snake Game
class SnakeGame(MiniGameFramework):
    def __init__(self, width, height, speed):
        super().__init__(width, height, speed)
        self.snake = Snake()
        self.food = Food()
        self.is_game_started = False
        self.reward = 0
        self.step_without_food = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def render(self):
        self.display.fill((0, 0, 0))

        if not self.is_game_started:
            pass
            # self.draw_start_text()
        else:
            self.snake.render(self.display)
            self.food.render(self.display)

        pygame.display.update()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.reward -= 10
        self.is_game_started = False

    # def draw_start_text(self):
    #     font = pygame.font.Font(None, 36)
    #     text = font.render("Click To Start Game", True, (255, 255, 255))
    #     text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
    #     self.display.blit(text, text_rect)

    def get_state(self):
        head = self.snake.body[0]
        state = [
            int(self.snake.direction_n == 0),
            int(self.snake.direction_n == 1),
            int(self.snake.direction_n == 2),
            int(self.snake.direction_n == 3),
            int(self.food.position[1] < head[1]),
            int(self.food.position[1] > head[1]),
            int(self.food.position[0] < head[0]),
            int(self.food.position[0] > head[0]),
            int(game.snake.is_danger((head[0], head[1] - 20))),
            int(game.snake.is_danger((head[0], head[1] + 20))),
            int(game.snake.is_danger((head[0] - 20, head[1]))),
            int(game.snake.is_danger((head[0] + 20, head[1]))),
        ]
        return tuple(state)


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

        if self.is_danger(new_head) or game.step_without_food > 1000:
            game.step_without_food = 0
            game.reset_game()
            return (game.get_state(), game.reward, True)

        game.reward -= 0.007
        self.body.insert(0, new_head)

        game.step_without_food += 1

        if new_head == game.food.position:
            game.reward += 1
            game.food.generate_new_position()
            game.step_without_food = 0
        else:
            self.body.pop()

        return (game.get_state(), game.reward, False)

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


class QTable:
    def __init__(self):
        self.qtable = np.zeros([2] * 12 + [4])
        self.learning_rate = 0.01
        self.discount = 0.95
        self.epsilon = 1
        self.eps_discount = 0.998
        self.current_q = 0
        self.next_max_q = 0

    def choose_action(self, state):
        d = game.snake.direction_n
        nd = 0

        if d == 0:
            nd = 1
        if d == 1:
            nd = 0
        if d == 2:
            nd = 3
        if d == 3:
            nd = 2

        actions = np.zeros([4])
        for i in range(4):
            if i != nd:
                actions[i] = self.qtable[state][i]
            else:
                actions[nd] = -np.inf

        if random.random() > self.epsilon:
            return np.argmax(actions)
        else:
            l = [0, 1, 2, 3]
            l.remove(nd)
            return random.choice(l)

    def update(self, reward, state, action):
        new_q = (1 - self.learning_rate) * self.current_q + self.learning_rate * (
            reward + (self.discount * self.next_max_q)
        )
        self.qtable[state][action] = new_q

        game.is_game_started = True


game = SnakeGame(800, 600, 30)
game.initialize()
agent = QTable()
length = []

if __name__ == "__main__":
    for i in range(1, 999999):
        if not game.is_running:
            break

        render = False
        done = False

        current_state = game.get_state()
        game.reward = 0
        agent.epsilon = agent.epsilon * agent.eps_discount

        if i % 250 == 0:
            print("episodes:", i)
            print(agent.epsilon)
            print(np.average(length))
            render = True
            length = []

        while not done and game.is_running:
            game.handle_events()
            action = agent.choose_action(current_state)
            agent.current_q = np.max(agent.qtable[current_state])

            new_state, reward, done = game.snake.update(action)
            agent.next_max_q = np.max(agent.qtable[new_state])
            agent.update(reward, current_state, action)
            current_state = new_state
            length.append(len(game.snake.body))

            if render:
                game.render()
                game.clock.tick(game.speed)
