import pygame
from pygame.locals import *
import sys
import random
import time
import os
os.chdir("c:\PlatAnimJR") 
pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional
 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

start_button = pygame.image.load('start.png')
s_button_rect = start_button.get_rect(center = (WIDTH/2,150))
quit_button =  pygame.image.load('quit.png')
q_button_rect = quit_button.get_rect(center = (WIDTH/2, 300))

def menu_screen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if s_button_rect.collidepoint(event.pos):
                    plat_game()

                if q_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        displaysurface.fill((125,67,28))
        displaysurface.blit(start_button, s_button_rect)
        displaysurface.blit(quit_button, q_button_rect)
        pygame.display.update()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.image.load("standing.png")
        self.rect = self.surf.get_rect()
        self.index = 0
        self.walkRight = [pygame.image.load('R1.png'),
                            pygame.image.load('R2.png'),
                            pygame.image.load('R3.png'),
                            pygame.image.load('R4.png'),
                            pygame.image.load('R5.png'),
                            pygame.image.load('R6.png'),
                            pygame.image.load('R7.png'),
                            pygame.image.load('R8.png'),
                            pygame.image.load('R9.png')]
        self.walkLeft = [pygame.image.load('L1.png'),
                            pygame.image.load('L2.png'),
                            pygame.image.load('L3.png'),
                            pygame.image.load('L4.png'),
                            pygame.image.load('L5.png'),
                            pygame.image.load('L6.png'),
                            pygame.image.load('L7.png'),
                            pygame.image.load('L8.png'),
                            pygame.image.load('L9.png')]
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0 
 
    def move(self):
        self.acc = vec(0,0.5)
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            self.surf = self.walkLeft[self.index]
            self.index += 1
            if self.index > 8:
                self.index = 0
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            self.surf = self.walkRight[self.index]
            self.index += 1
            if self.index > 8:
                self.index = 0
                 
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:   
                        hits[0].point = False   
                        self.score += 1          
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
 
 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50,100), 12))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, HEIGHT-30)))
        self.speed = random.randint(-1, 1)
        
        self.point = True   
        self.moving = True
        
    
    def move(self):
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH
 
 
def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50,100)
        p  = platform()      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                              random.randrange(-50, 0))
             C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
#herman code
class power_up():
    def __init__(self):
        self.image = pygame.image.load("PowerUp.png")
        self.image = pygame.transform.scale(self.image(30,30))
        self.rect= self.image.get_rect()
        self.rect =random.randint(0,370)
        self.rect.y = 300

    def powerUpSpawn(self):
        displaysurface.blit(self.image, self.rect)
        pygame.draw.rect(displaysurface,'red',self.rect,4)
    
    def changePlaces(self):
        self.rect.x=random.randint(0,370)
        self.rect.y =-20
    def scoll(self):
        self.rect.y +=abs(P1.vel.y)

#herman code
PT1 = platform()
P1 = Player()
 
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
 
platforms = pygame.sprite.Group()
platforms.add(PT1)

PT1.moving = False
PT1.point = False   ##
 
for x in range(random.randint(4,5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)
 
def plat_game(): 
    while True:
        P1.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_SPACE:
                    P1.jump()
            if event.type == pygame.KEYUP:    
                if event.key == pygame.K_SPACE:
                    P1.cancel_jump()

        if P1.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaysurface.fill((255,0,0))
                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                sys.exit()
    
        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
    
        plat_gen()
        displaysurface.fill((0,0,0))
        f = pygame.font.SysFont("Verdana", 20)     
        g  = f.render(str(P1.score), True, (123,255,0))   
        displaysurface.blit(g, (WIDTH/2, 10))   
        
        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()
        print(P1.index)
        pygame.display.update()
        FramePerSec.tick(FPS)
menu_screen()