import pygame


pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ball_x = SCREEN_WIDTH / 2
ball_y = SCREEN_HEIGHT / 2

is_running = True
while is_running:
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (ball_x, ball_y), 10)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    clock.tick(60)

