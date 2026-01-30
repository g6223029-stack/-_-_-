from random import choice

import pygame
import sys
import  random

def create_ball(start_pos, end_pos, radius=15, accel=0.15):
    start = pygame.Vector2(start_pos)
    end = pygame.Vector2(end_pos)
    direction = (end - start).normalize()
    return {
        "pos": pygame.Vector2(start_pos),
        "start": start,
        "end": end,
        "dir": direction,
        "vel": 0.0,
        "accel": accel,
        "radius": radius,
        "active": True
    }

def update_ball(ball, basket_pos, basket_width, basket_height):
    if ball and ball["active"]:
        ball["vel"] += ball["accel"]
        ball["pos"] += ball["dir"] * ball["vel"]
        if (ball["pos"] - ball["start"]).length() >= (ball["end"] - ball["start"]).length():
            ball["active"] = False

            basket_rect = pygame.Rect(basket_pos[0], basket_pos[1], basket_width, basket_height)

            if basket_rect.collidepoint(ball["end"]):
                return "hit"
            return  "miss"
    return  "moving"

def draw_ball(surface, ball, angle):
    if ball and ball["active"]:
        if angle:
            normal = pygame.Vector2(ball["dir"].y, -ball["dir"].x)
        else:
            normal = pygame.Vector2(-ball["dir"].y, ball["dir"].x)
        draw_pos = ball["pos"] + normal * ball["radius"]
        pygame.draw.circle(surface, WHITE, (int(draw_pos.x), int(draw_pos.y)), ball["radius"])

pygame.init()

WIDTH = 800
HEIGHT = 600
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.SysFont("Arial", 36, bold=True)

clock = pygame.time.Clock()

pygame.display.set_caption("Волк ловит яйца")

basket_right_down = [500, 500]
basket_left_down = [200, 500]
basket_right_up = [500, 300]
basket_left_up = [200, 300]

last_spawn_time = 0
spawn_delay = 1500
score = 0
misses = 0

position_x = 500
position_y = 500
size_width = 100
size_height = 50

active_ball = None
ball_left_up = None
ball_right_up = None
ball_right_down = None
ball_left_down = None

running = True

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if [position_x, position_y] == basket_right_down:
                    position_x, position_y =basket_right_up[0], basket_right_up[1]
                elif [position_x, position_y] == basket_left_down:
                    position_x, position_y = basket_left_up[0], basket_left_up[1]

            elif event.key == pygame.K_DOWN:
                if [position_x, position_y] == basket_right_up:
                    position_x, position_y =basket_right_down[0], basket_right_down[1]
                elif [position_x, position_y] == basket_left_up:
                    position_x, position_y = basket_left_down[0], basket_left_down[1]
            elif event.key == pygame.K_LEFT:
                if [position_x, position_y] == basket_right_up:
                    position_x, position_y = basket_left_up[0], basket_left_up[1]
                elif [position_x, position_y] == basket_right_down:
                    position_x, position_y = basket_left_down[0], basket_left_down[1]
            elif event.key == pygame.K_RIGHT:
                if [position_x, position_y] == basket_left_up:
                    position_x, position_y = basket_right_up[0], basket_right_up[1]
                elif [position_x, position_y] == basket_left_down:
                    position_x, position_y = basket_right_down[0], basket_right_down[1]

    if current_time - last_spawn_time > spawn_delay:
        choice = random.randint(1, 4)
        if choice == 1 and not (ball_left_up and ball_left_up["active"]):
            ball_left_up = create_ball([0, 0], [250, 300])
        elif choice == 2 and not (ball_left_down and ball_left_down["active"]):
            ball_left_down = create_ball([0, 200], [250, 500])
        elif choice == 3 and not (ball_right_up and ball_right_up["active"]):
            ball_right_up = create_ball([800, 0], [550, 300])
        elif choice == 4 and not (ball_right_down and ball_right_down["active"]):
            ball_right_down = create_ball([800, 200], [550, 500])
        last_spawn_time = current_time

    current_basket = [position_x, position_y]

    for ball_var in ['ball_left_up', 'ball_left_down', 'ball_right_up', 'ball_right_down']:
        ball_data = globals()[ball_var]
        if ball_data and ball_data["active"]:
            res = update_ball(ball_data, current_basket, size_width, size_height)
            if res == "hit":
                score += 1
            elif res == "miss":
                misses += 1

    if misses > 3:
        running = False

    screen.fill((0, 225, 0))

    pygame.draw.rect(screen, (255, 217, 105), (position_x, position_y, size_width, size_height))   #рисуем корзину
    pygame.draw.line(screen, YELLOW, [0, 0], [250, 300], 2)
    pygame.draw.line(screen, YELLOW, [0, 200], [250, 500], 2)
    pygame.draw.line(screen, YELLOW, [800, 0], [550, 300], 2)
    pygame.draw.line(screen, YELLOW, [800, 200], [550, 500], 2)

    draw_ball(screen, ball_left_up, True)
    draw_ball(screen, ball_left_down, True)
    draw_ball(screen, ball_right_up, False)
    draw_ball(screen, ball_right_down, False)

    screen.blit(font.render(f"Счёт: {score}", True, (0, 0, 0)), (WIDTH //2- 50,20))
    screen.blit(font.render(f"Промахи: {misses}", True, (200, 0, 0)), (WIDTH //2- 70,60))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()