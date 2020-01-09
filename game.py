import pygame
import random
import time

speed = 2

pygame.init()
WHITE = (255,255,255)
BLACK = (0,0,0)
not_pasul = True
screen = pygame.display.set_mode((500, 500))
jumping = False
crouch = False
cactus_list = []
jump = 0
v_jump = 0.1 * speed
g = 1/15000 * speed ** 2
cactus_t = 0
while not_pasul:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Usually wise to be able to close your program.
            not_pasul = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not jumping:
                jumping = True
    crouch = pygame.key.get_pressed()[pygame.K_DOWN]

    if jumping:
        if crouch:
            jump += v_jump - 0.1 * speed
        else:
            jump += v_jump
        v_jump -= g
        if jump <= 0:
            jumping = False
            jump = 0
            v_jump = 0.1 * speed

    if cactus_t <= 0:
        cactus_t = 3 + random.uniform(0,2)
        cactus_list.append([550,random.choice([10,20,60]),True if random.random()>0.8 else False,random.choice([400,450])])
    else:
        cactus_t -= 0.001 * speed

    if (cactus_list[0][2] == False and cactus_list[0][0] <= 60 and cactus_list[0][0] + cactus_list[0][1] >= 50 and 450 - jump > 420) or (not crouch and cactus_list[0][2] == True and cactus_list[0][0] <= 60 and cactus_list[0][0] + 30 >= 50 and cactus_list[0][3] - 30 <= 450 - jump <= cactus_list[0][3] + 15) or (cactus_list[0][2] == True and crouch and jump != 0 and cactus_list[0][0] <= 60 and cactus_list[0][0] + 30 >= 50 and cactus_list[0][3] - 30 <= 450 - jump <= cactus_list[0][3] + 15):
        time.sleep(1)
        not_pasul = False


    screen.fill((255,255,255))
    if cactus_list[0][0] < -60:
        cactus_list.remove(cactus_list[0])
    for i in range(len(cactus_list)):
        if cactus_list[i][2]:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(cactus_list[i][0], cactus_list[i][3], 30, 12))
        else:
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(cactus_list[i][0], 450, cactus_list[i][1], 30))
        cactus_list[i][0] -= 0.05 * speed


    if crouch:
        pygame.draw.rect(screen, BLACK, pygame.Rect(50, 465 - jump, 20, 15))
    else:
        pygame.draw.rect(screen,BLACK,pygame.Rect(50,450-jump,10,30))
    pygame.display.flip()

    print(cactus_list)
