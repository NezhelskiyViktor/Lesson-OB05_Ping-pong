import pygame
import sys
from random import *

start_game = False
speed_bars = 10

class Ball:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._vx = 0
        self._vy = 0
        self.hitbox = pygame.Rect(self._x - 20, self._y - 20, 40, 40)
        self.rect = pygame.draw.circle(screen, WHITE, (self._x, self._y), 20)

    def set_speed(self, speed):
        self._vx, self._vy = speed

    def set_x_y(self):
        self._x, self._y = 300, 400

    def move(self):
        self._x += self._vx
        self._y += self._vy
        self.hitbox = pygame.Rect(self._x - 20, self._y - 20, 40, 40)
        self.rect = pygame.draw.circle(screen, WHITE, (self._x, self._y), 20)
        # Проверка на столкновение с Bar
        collision_top = self.hitbox.colliderect(top_bar.hitbox)
        if collision_top:
            collision_top = False
            self._vy = -self._vy
            self._vx = self._vx + top_bar._vx // 5
        collision_bottom = self.hitbox.colliderect(bottom_bar.hitbox)
        if collision_bottom:
            collision_bottom = False
            self._vy = -self._vy
            self._vx = self._vx + bottom_bar._vx // 5
        # Проверка на выход на границы экрана
        if self._y < 11 or self._y > 789:
            global start_game
            start_game = False
            self.set_speed((0, 0))
        if self._x < 21 or self._x > 579:
            self._vx = -self._vx
        self.hitbox = pygame.Rect(self._x - 20, self._y - 20, 40, 40)
        return self._x


class Bar:
    def __init__(self, y):
        self._x = 220
        self._y = y
        self._vx = 0
        self._width = 160
        self._height = 10
        self.hitbox = pygame.Rect(self._x, self._y, self._width, self._height)
        self.rect = pygame.draw.rect(screen, WHITE, self.hitbox)

    def move(self):
        self._x += self._vx
        if self._x < 0 or self._x > 600 - self._width:
            self._vx = 0
        self.hitbox = pygame.Rect(self._x, self._y, self._width, self._height)
        self.rect = pygame.draw.rect(screen, WHITE, self.hitbox)
        return self._x

    def set_speed(self, speed):
        self._vx = speed

    def set_x(self, x):
        self._x = x - self._width // 2


def draw_text(surface, text, y):
    _font_name = pygame.font.match_font('arial')
    _font = pygame.font.SysFont(_font_name, 24)
    _text_surface = _font.render(text, True, YELLOW)
    _text_rect = _text_surface.get_rect()
    _text_rect.midtop = (300, y)
    surface.blit(_text_surface, _text_rect)


pygame.init()
pygame.mouse.set_visible(False)
FPS = 20
clock = pygame.time.Clock()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Создание экрана
screen = pygame.display.set_mode((600, 800))

pygame.display.set_caption('Игра Пинг-понг')

ball = Ball(300, 400)
top_bar = Bar(20)
bottom_bar = Bar(770)
game_with_computer = False

# Цикл игры
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE) or \
                    (event.key == pygame.K_KP_ENTER) or \
                    (event.key == pygame.K_RETURN):
                start_game = not start_game
                if start_game:
                    game_with_computer = (event.key == pygame.K_SPACE)
                    ball.set_speed((choice([-6, -5, -4, -3, -2, -1, 0,1, 2, 3, 4, 5, 6]), choice([-13,-12, 12, 13])))
                    ball.set_x_y()
                    top_bar.set_speed(0)
                    bottom_bar.set_speed(0)
                else:  # Остановка игры
                    ball.set_speed((0, 0))
                    ball.set_x_y()
                    top_bar.set_speed(0)
                    top_bar.set_x(300)
                    bottom_bar.set_speed(0)
                    bottom_bar.set_x(300)
            # Обработка нажатия клавиш игроками
            if event.key == pygame.K_RIGHT:
                bottom_bar.set_speed(speed_bars)
            elif event.key == pygame.K_LEFT:
                bottom_bar.set_speed(-speed_bars)
            elif event.key == pygame.K_DOWN:
                bottom_bar.set_speed(0)

            if event.key == pygame.K_d:
                top_bar.set_speed(speed_bars)
            elif event.key == pygame.K_a:
                top_bar.set_speed(-speed_bars)
            elif event.key == pygame.K_s:
                top_bar.set_speed(0)
    # Обновление экрана
    screen.fill(BLACK)
    if not game_with_computer:
        draw_text(screen, "<a> <s> <d>", 0)
    draw_text(screen, "<Right> <Down> <Left>", 780)
    if not start_game:
        draw_text(screen, "Если игра с компьютером нажмите <Пробел>,", 200)
        draw_text(screen, "если игра с человеком нажмите <Enter>", 220)
    if game_with_computer:
        top_bar.set_x(ball.move())
    else:
        ball.move()
    top_bar.move()
    bottom_bar.move()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
