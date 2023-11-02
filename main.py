import pygame
import random
import numpy as np
from minigame_framework import MiniGameFramework

# Snake Game
class SnakeGame(MiniGameFramework):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.snake = Snake()
        self.food = Food()
        self.q_table = QTable()
        self.is_game_started = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and not self.is_game_started:
                self.is_game_started = True

    
    def get_state(self):
        print(self.snake.body)
        return ((self.snake.body, self.food.position))

    def update(self):
        if self.is_game_started:
            state = self.get_state()
            print(state)
            state_index = self.q_table.get_index(state)
            print(state_index)
            self.q_table.state.append(state)
            self.q_table.current_q.append(np.argmax(self.q_table.qtable[state_index][1]))
            move = self.q_table.choose_action(state_index)
            self.q_table.actions.append(move)

            self.snake.change_direction(move)
            self.snake.update(self.food)
            self.food.update()
            
            new_state = self.get_state()

            state_index = self.q_table.get_index(new_state)
            self.q_table.next_max_q.append(np.argmax(self.q_table.qtable[state_index][1]))
            

    def render(self):
        self.display.fill((0, 0, 0))

        if not self.is_game_started:
            self.draw_start_text()
        else:
            self.snake.render(self.display)
            self.food.render(self.display)

        pygame.display.update()

    def reset_game(self):
        self.q_table.reward = -1
        self.snake = Snake()
        self.food = Food()
        self.is_game_started = False
        self.q_table.update()

    def is_out_of_bounds(self):
        head = self.snake.body[0]
        return head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height

    def draw_start_text(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Click To Start Game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.display.blit(text, text_rect)




class Snake:
    def __init__(self):
        self.body = [(200, 200)]
        self.direction = (0, -1)
        self.color = (0, 255, 0)

    def check_collision(self):
        head = self.body[0]
        if head in self.body[1:]:
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

    def update(self, food):
        head = self.body[0]
        new_head = (head[0] + self.direction[0] * 20, head[1] + self.direction[1] * 20)

        if new_head[0] < 0 or new_head[0] >= 800 or new_head[1] < 0 or new_head[1] >= 600:
        #撞墙        
            game.reset_game()
            return
        if self.check_collision():
            game.reset_game()
            return
        
        self.body.insert(0, new_head)

        if new_head == food.position:
            food.generate_new_position()
            game.q_table.reward += 1
        else:
            self.body.pop()

    def render(self, display):
        for segment in self.body:
            pygame.draw.rect(display, self.color, (segment[0], segment[1], 20, 20))




class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.generate_new_position()

    def generate_new_position(self):
        x = random.randint(0, 39) * 20
        y = random.randint(0, 29) * 20
        self.position = (x, y)

    def update(self):
        pass

    def render(self, display):
        pygame.draw.rect(display, self.color, (self.position[0], self.position[1], 20, 20))

class QTable:
    def __init__(self):
        self.qtable = []
        self.learning_rate = 0.2
        self.discount = 0.9
        self.epsilon = 1
        self.current_q = []
        self.next_max_q = []
        self.moves = []
        self.state = []
        self.actions = []
        self.reward = 0

    def get_index(self, state):
        for i in range(len(self.qtable)):
            print(self.qtable[i][0])
            if self.qtable[i][0] == state[0]:
                return i
                
        self.qtable.append([state, [0, 0, 0, 0]])
        print('new')
        return len(self.qtable) - 1
        
    
    def choose_action(self, state_index):
        #if random.random() > self.epsilon:
        action = np.argmax(self.qtable[state_index][1])
        print(self.qtable[state_index][1])
        # else:
        #     action = random.choice([0, 1, 2, 3])
        return action


    def update(self):
        print('update')
        for i in range(len(self.actions) - 1):
        
            state_index = self.get_index(self.state[i])
        
            new_q = (1 - self.learning_rate) * self.current_q[i] + self.learning_rate * (self.reward + (self.discount * self.next_max_q[i]))
            self.qtable[state_index][1][self.actions[i]] = new_q

        self.epsilon -= 0.05
        
        state_index = self.get_index(self.state[-1])
        self.qtable[state_index][1][self.actions[-1]] = self.reward
            
        self.actions = []
        self.current_q = []
        self.next_max_q = []
        self.moves = []
        self.state = []
        self.reward = 0

if __name__ == "__main__":
    game = SnakeGame(800, 600)
    game.run()


