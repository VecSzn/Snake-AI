import pygame
import random
from minigame_framework import MiniGameFramework

# Snake Game
class SnakeGame(MiniGameFramework):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.snake = Snake()
        self.food = Food()
        self.is_game_started = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not self.is_game_started:
                self.is_game_started = True

            if self.is_game_started:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.snake.change_direction("UP")
                    elif event.key == pygame.K_s:
                        self.snake.change_direction("DOWN")
                    elif event.key == pygame.K_a:
                        self.snake.change_direction("LEFT")
                    elif event.key == pygame.K_d:
                        self.snake.change_direction("RIGHT")

    

    def update(self):
        if self.is_game_started:
            self.snake.update(self.food)
            self.food.update()

    def render(self):
        self.display.fill((0, 0, 0))

        if not self.is_game_started:
            self.draw_start_text()
        else:
            self.snake.render(self.display)
            self.food.render(self.display)

        pygame.display.update()

    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.is_game_started = False

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
        if new_direction == "UP" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif new_direction == "DOWN" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif new_direction == "LEFT" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif new_direction == "RIGHT" and self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self, food):
        head = self.body[0]
        new_head = (head[0] + self.direction[0] * 20, head[1] + self.direction[1] * 20)

        if new_head[0] < 0 or new_head[0] >= 800 or new_head[1] < 0 or new_head[1] >= 600:
            #pygame.event.post(pygame.event.Event(pygame.QUIT))
            game.reset_game()
            return
        if self.check_collision():
            game.reset_game()
            return
        self.body.insert(0, new_head)

        if new_head == food.position:
            food.generate_new_position()
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


if __name__ == "__main__":
    game = SnakeGame(800, 600)
    game.run()