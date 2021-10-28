import pygame
from pygame import mixer
import os
import random
pygame.font.init()
pygame.init()
mixer.init()




SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WIN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("GOING UP")

FPS = 60

#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,120,255)
GREEN = (100,255,0)

#GAME VARIABLES
flip = False
GRAVITY = 1
MAX_PADS = 10 #MAXIMUM PADS ON THE SCREEN
JUMP_THRESHOLD = 200
bg_scroll = 0
game_over = False
color = WHITE
score = 0
fade_counter = 0
#CREATE A FILE TO STORE HIGHSCORE
if os.path.exists("score.txt"):
    with open("score.txt","r") as file:
            high_score = int(file.read())
else:
    high_score = 0

#SOUND
pygame.mixer.music.load(os.path.join("Assets",'Komiku_-_02_-_Poupis_Theme.mp3'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0.0)
jump_sfx = pygame.mixer.Sound(os.path.join("Assets","88499787.mp3"))
jump_sfx.set_volume(0.3)
#FONTS
font = pygame.font.SysFont("Lucida Sans",60)
font_small = pygame.font.SysFont("comicsans",35)

#IMAGES
sky_image = pygame.image.load(os.path.join("Assets", "1-1.jpg"))
player_image = pygame.image.load(os.path.join("Assets","Satyr_02_Idle_000.png"))
pad_image = pygame.image.load(os.path.join("Assets","pad.png"))

class player():
    def __init__(self,x,y):
        self.img = pygame.transform.scale(player_image,(50,50))
        self.width = 35
        self.height = 48
        self.speed = 5
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = (x,y)
        self.flip = False
        self.vel_y = 0
        
    def draw(self):
        WIN.blit(pygame.transform.flip(self.img,self.flip,False),(self.rect.x - 5,self.rect.y - 2))
        

    def move(self):
        scroll =0
        dy = 0
        dx = 0
        
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a]:
            dx -= self.speed 
            self.flip = True
        if key_pressed[pygame.K_d]:
            dx += self.speed
            self.flip = False
        #GRAVITY
        self.vel_y += GRAVITY
        dy += self.vel_y
        #COLLISION WITH THE GROUND
        #if self.rect.bottom + dy - 5 > SCREEN_HEIGHT:
           # dy = 0
           # self.vel_y = -25
        #COLLISION WITH THE EDGES
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #COLLISION WITH PAD
        for pad in pad_group:
            if pad.rect.colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
                #check if above the pad
                if self.rect.bottom < pad.rect.centery:
                    #check if falling
                    if self.vel_y > 0:
                        self.rect.bottom = pad.rect.top
                        dy = 0
                        self.vel_y = -20
                        jump_sfx.play()

        #IF PLAYER IS AT THE TOP OF SCREEN
        if self.rect.top <= JUMP_THRESHOLD:
            #if player is jumping
            if self.vel_y < 0:
                scroll = -dy
                
         
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll
        

class Pad(pygame.sprite.Sprite):
    def __init__(self,x,y,width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pad_image,(width,20))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self,scroll):
        #UPDATE PLATFORMS VERTICAL POSITION
        self.rect.y += scroll

        #CHECK IF PAD WENT OFF THE SCREEN
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()#delete the pad
    

def draw_win(scroll):
    #scrolling bg
    WIN.blit(sky_image,(0,0 + bg_scroll))
    WIN.blit(sky_image,(0,-600 + bg_scroll))
    
    


def draw_text(message,x,y,font,color):
    message_text = font.render(message,True,color)
    WIN.blit(message_text,(x,y))
    


#INSTANCES
jumper = player(SCREEN_WIDTH//2,SCREEN_HEIGHT -150)
#CREATE SPRITE GROUP
pad_group = pygame.sprite.Group()

#CREATE 1 PLATFORM
pad = Pad(SCREEN_WIDTH//2,SCREEN_HEIGHT-50,80)
pad_group.add(pad)#ADD PAD IN SPRITE GROUP

#main loop
clock = pygame.time.Clock()
run = True
while run:
    clock.tick(FPS)
    if game_over != True:
    
        scroll = jumper.move()
        #DRAW BACKGROUND
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_win(bg_scroll)
        
        #CREATE PLATFORMS
        if len(pad_group) < MAX_PADS:#IF PAD_GROUP LENGTH IS LESS THEN 10 THEN CREATE A PAD
            pad_w = random.randint(80,100)
            pad_x = random.randint(0,SCREEN_WIDTH-pad_w)
            pad_y = pad.rect.y - random.randint(80,150)
            pad = Pad(pad_x,pad_y,pad_w)
            pad_group.add(pad)#ADD PAD IN SPRITE GROUP
        
        if scroll > 0:
            score += scroll

        #DRAW PADS
        pad_group.update(scroll)
        pad_group.draw(WIN)
        draw_text(f'SCORE: {score}ft',SCREEN_WIDTH//2-60,10,font_small,color)
        #IF SCORE IS HIGHER THEN HIGH SCORE CHANGE COLOR
        if score > high_score:
            color = GREEN
        else:
            color = WHITE

        #DRAW PLAYER
        jumper.draw()
        
        #CHECK GAME OVER
        if jumper.rect.top > SCREEN_HEIGHT:
            game_over = True
    else:
        #FADE EFFECT
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            pygame.draw.rect(WIN,BLACK,(0,0,fade_counter,SCREEN_HEIGHT//2))
            pygame.draw.rect(WIN,BLACK,(SCREEN_WIDTH - fade_counter,SCREEN_HEIGHT//2,fade_counter,SCREEN_HEIGHT//2))
        else:
            draw_text(f"GAME OVER!",SCREEN_WIDTH//2-175,SCREEN_HEIGHT//2 -60,font,WHITE)
            draw_text(f"SCORE: {score}ft",SCREEN_WIDTH//2-60,SCREEN_HEIGHT//2+ 50,font_small,WHITE)
            draw_text(f"HIGH SCORE: {high_score}ft" ,SCREEN_WIDTH//2-120,SCREEN_HEIGHT//2 + 80,font_small,WHITE)
            draw_text('PRESS SPACE TO PLAY AGAIN',SCREEN_WIDTH//2 - 180,SCREEN_HEIGHT-90,font_small,WHITE)
            #UPDATE HIGH SCORE
            if score > high_score:
                high_score = score
                with open("score.txt","w") as file:
                    file.write(str(high_score))
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_SPACE]:
                #reset varables(game)
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                #RESET PLAYER
                jumper.rect.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT -150)

                #RESET PADS
                pad_group.empty()#deletes all the ppads in the group and reset

                #CREATE 1 PLATFORM
                pad = Pad(SCREEN_WIDTH//2,SCREEN_HEIGHT-50,80)
                pad_group.add(pad)#ADD PAD IN SPRITE GROUP
                

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    pygame.display.update()

pygame.quit()

