import pygame
import math

pygame.init()
running = True

WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT) = (1000, 600)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode(WINDOW_SIZE)

color = BLACK
shape = 'line'

clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption('Давайте рисовать!')
screen.fill(WHITE)

width = 1

prev, cur = None, None

font = pygame.font.SysFont('Verdana', 15)

while running:
    pygame.draw.rect(screen, WHITE, (0, 0, WINDOW_WIDTH, 30))
    screen.blit(font.render(f'Mode: {shape}', True, BLACK), (10, 10))
    screen.blit(font.render(f'Width: {width}', True, BLACK), (310, 10))
    screen.blit(font.render(f'Color: {color}', True, BLACK), (610, 10))
    
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        ctrl_pressed = pressed[pygame.K_RCTRL] or pressed[pygame.K_LCTRL]
        alt_pressed = pressed[pygame.K_RALT] or pressed[pygame.K_LALT]

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if pressed[pygame.K_DOWN] and width > 1:
                width -= 1
            if pressed[pygame.K_UP]:
                width += 1
            if alt_pressed and pressed[pygame.K_b]:
                color = BLUE
            if alt_pressed and pressed[pygame.K_r]:
                color = RED
            if alt_pressed and pressed[pygame.K_g]:
                color = GREEN
            if alt_pressed and pressed[pygame.K_q]:
                color = BLACK

            if ctrl_pressed and pressed[pygame.K_c]:
                shape = 'circle'
            if ctrl_pressed and pressed[pygame.K_r]:
                shape = 'rectangle'
            if ctrl_pressed and pressed[pygame.K_l]:
                shape = 'line'
            if ctrl_pressed and pressed[pygame.K_e]:
                shape = 'eraser'
                
            if ctrl_pressed and pressed[pygame.K_t]:
                shape = 'right_triangle'
            if ctrl_pressed and pressed[pygame.K_q]:
                shape = 'equilateral_triangle'
            if ctrl_pressed and pressed[pygame.K_h]:
                shape = 'rhombus'

        if shape == 'line' or shape == 'eraser':
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                cur = pygame.mouse.get_pos()
                if prev:
                    if shape == 'line':
                        pygame.draw.line(screen, color, prev, cur, width)
                    if shape == 'eraser':
                        pygame.draw.line(screen, WHITE, prev, cur, width)
                    prev = cur
            if event.type == pygame.MOUSEBUTTONUP:
                prev = None
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                prev = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                cur = pygame.mouse.get_pos()
                if shape == 'circle':
                    x = (prev[0] + cur[0]) / 2
                    y = (prev[1] + cur[1]) / 2
                    r = math.sqrt((cur[0] - prev[0])**2 + (cur[1] - prev[1])**2) / 2
                    pygame.draw.circle(screen, color, (int(x), int(y)), int(r), width)
                elif shape == 'rectangle':
                    x = min(prev[0], cur[0])
                    y = min(prev[1], cur[1])
                    w = abs(cur[0] - prev[0])
                    h = abs(cur[1] - prev[1])
                    pygame.draw.rect(screen, color, (x, y, w, h), width)
                elif shape == 'right_triangle':
                    pygame.draw.polygon(screen, color, [prev, (prev[0], cur[1]), cur], width)
                elif shape == 'equilateral_triangle':
                    side_length = math.sqrt((cur[0] - prev[0])**2 + (cur[1] - prev[1])**2)
                    height = side_length * math.sqrt(3) / 2
                    pygame.draw.polygon(screen, color, [
                        prev,
                        (prev[0] + side_length, prev[1]),
                        (prev[0] + side_length / 2, prev[1] - height)
                    ], width)
                elif shape == 'rhombus':
                    pygame.draw.polygon(screen, color, [
                        prev,
                        (2 * cur[0] - prev[0], cur[1]),
                        cur,
                        (2 * prev[0] - cur[0], prev[1])
                    ], width)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
