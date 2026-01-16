import pygame
import sys

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

def update_ball(ball):
    if ball and ball["active"]:
        ball["vel"] += ball["accel"]
        ball["pos"] += ball["dir"] * ball["vel"]
        if (ball["pos"] - ball["start"]).length() >= (ball["end"] - ball["start"]).length():
            ball["active"] = False
    return  ball

def draw_ball(surface, ball, angle):
    if ball:
        pygame.draw.line(surface, YELLOW, ball["start"], ball["end"], 2)
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

clock = pygame.time.Clock()

pygame.display.set_caption("Волк ловит яйца")

basket_right_down = [500, 500]
basket_left_down = [200, 500]
basket_right_up = [500, 300]
basket_left_up = [200, 300]

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_left_up = create_ball([0, 0], basket_left_up)
                ball_left_down = create_ball([0, 200], basket_left_down)
                ball_right_up = create_ball([800, 0], [600, 300])
                ball_right_down = create_ball([800, 200], [600, 500])
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

    if ball_left_up and ball_left_down and ball_right_up and ball_right_down:
        ball_left_up = update_ball(ball_left_up)
        ball_left_down = update_ball(ball_left_down)
        ball_right_up = update_ball(ball_right_up)
        ball_right_down = update_ball(ball_right_down)

    screen.fill((0, 225, 0))

    pygame.draw.rect(screen, (255, 217, 105), (position_x, position_y, size_width, size_height))   #рисуем корзину
    draw_ball(screen, ball_left_up, True)
    draw_ball(screen, ball_left_down, True)
    draw_ball(screen, ball_right_up, False)
    draw_ball(screen, ball_right_down, False)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()