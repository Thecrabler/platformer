
import sys,random,time 
import pygame
from pygame import K_LEFT,KEYUP,K_RIGHT, MOUSEBUTTONDOWN,QUIT,KEYDOWN,K_SPACE

pygame.init()
vec = pygame.math.Vector2

up_top=1
HEIGHT=450
WIDTH=400
ACC =0.5
FPS=60
FRIC= -0.12
FramePerSec =pygame.time.Clock()
displaysurface= pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('platformer')
man= pygame.image.load('man2.png').convert_alpha()
Quit_button=pygame.image.load("quit.png")
Quit_button_rect=Quit_button.get_rect(center=(WIDTH/2,300))
start_button=pygame.image.load("start.png")
start_button_rect=start_button.get_rect(center=(WIDTH/2,200))

def menu_screen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type==MOUSEBUTTONDOWN:
                if Quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if start_button_rect.collidepoint(event.pos):
                    platformerg()
        displaysurface.fill((222,58,150))
        displaysurface.blit(start_button,(start_button_rect))
        displaysurface.blit(Quit_button,(Quit_button_rect))
        pygame.display.update()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf =pygame.image.load("standing.png")
        self.rect = self.surf.get_rect (center=(10,420))
        self.pos =vec((10,385))
        self.vel=vec((0,0))
        self.acc= vec((0,0))
        self.score=0
        self.index=0
        self.walkright=[ pygame.image.load('R1.png'),pygame.image.load('R2.png'),pygame.image.load('R3.png'),pygame.image.load('R4.png'),pygame.image.load('R5.png'),pygame.image.load('R6.png'),pygame.image.load('R7.png'),pygame.image.load('R8.png'),pygame.image.load('R9.png')]
        self.walkleft=[pygame.image.load('L1.png'),pygame.image.load('L2.png'),pygame.image.load('L3.png'),pygame.image.load('L4.png'),pygame.image.load('L5.png'),pygame.image.load('L6.png'),pygame.image.load('L7.png'),pygame.image.load('L8.png'),pygame.image.load('L9.png')]
    def move(self):
        self.acc =vec(0,0.5)

        pressed_keys=pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x=-ACC
            self.surf = self.walkleft[self.index]
            self.index +=1
            if self.index > 8:
                self.index = 0

        if pressed_keys[K_RIGHT]:
            self.acc.x=+ACC
            self.surf = self.walkright[self.index]
            self.index +=1
            if self.index > 8:
                self.index = 0

        self.acc.x+=self.vel.x*FRIC
        self.vel +=self.acc
        self.pos += self.vel+0.5*self.acc

        if self.pos.x>WIDTH:
            self.pos.x =0
        if self.pos.x<0:
            self.pos.x=WIDTH
        self.rect.midbottom=self.pos

    def update(self):
        hits =pygame.sprite.spritecollide(P1,platforms,False)
        if self.vel.y>0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point==True:
                        hits[0].point=False
                        self.score+=1
                    self.pos.y=hits[0].rect.top+1
                    self.vel.y =0
                    self.jumping=False
    def jump(self):
        hits =pygame.sprite.spritecollide(self,platforms,False)
        if hits and not self.jumping:
            self.jumping =True
            self.vel.y= -15
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf =pygame.Surface((random.randint(50,100),12))
        self.surf.fill((random.randint(50,255),random.randint(50,255),random.randint(50,255)))
        self.rect = self.surf.get_rect (center=(random.randint(0,WIDTH-10),random.randint(0,HEIGHT-30)))
        self.point=True
        
        
PT1=platform()
P1 =Player()
def check(platform,groupies):
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom)<50)and(abs(platform.rect.bottom - entity.rect.top)<50):
                return True
        C=False 
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
platforms=pygame.sprite.Group()
platforms.add(PT1)
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
PT1.surf =pygame.Surface((WIDTH,20))
PT1.surf.fill((255,0,0))
PT1.rect=PT1.surf.get_rect(center=(WIDTH/2,HEIGHT-10))


game_font=pygame.font.SysFont("Arial",60)
text_surf=game_font.render(str(P1.score),True,(123,255,0))
displaysurface.blit(text_surf,(WIDTH/2,10))

for x in range(random.randint(5,6)):
    pl =platform()
    platforms.add(pl)
    all_sprites.add(pl)
def platformerg():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key==pygame.K_SPACE:
                    P1.jump()
            if event.type == KEYUP:
                if event.key ==pygame.K_SPACE:
                    P1.cancel_jump()
        displaysurface.fill((0,0,0))
        
        if P1.rect.top>HEIGHT:
            for entity in all_sprites:
                entity.kill()
                time.sleep(1)
                displaysurface.fill((255,0,0))
                pygame.display.update()
                time.sleep(1)
                pygame.quit()
                sys.exit()
        
        for entity in all_sprites:
            displaysurface.blit(entity.surf,entity.rect)
        P1.move()
        P1.update()
        plat_gen()
        if P1.rect.top<=HEIGHT/3:
            P1.pos.y+=abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y+=abs(P1.vel.y)
                if plat.rect.top>=HEIGHT:
                    plat.kill()
        displaysurface.blit(text_surf,(WIDTH/2,10))
        pygame.display.update()
        FramePerSec.tick(FPS)
        print(P1.index)
menu_screen()