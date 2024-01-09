import pygame
import math
import random

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

a = pygame.Vector2(100,200)
b = pygame.Vector2(200,100)
print(b*a)
print(pygame.Vector2.magnitude(b+a))

print(10%math.pi)

c = pygame.Vector2(0,1000).as_polar()
print(c)
print(c[0])
print(c[1])
proj = b.project(a)

run = True
while run:
    screen.fill((0,0,0))

    pygame.draw.line(screen,"white", (0,0), a)
    pygame.draw.line(screen,"red", (0,0), b)
    pygame.draw.line(screen,"grey", (0,0), proj)

    j = pygame.draw.polygon(screen, "white", [(1, 100), (20, 21), (400, 300)])
    print(j.points)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.display.flip()

    clock.tick(60) / 1000
    


pygame.quit()