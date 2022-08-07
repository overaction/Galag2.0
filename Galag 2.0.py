import pygame
import random
import math

WIDTH = 1000
HEIGHT = 700
FPS = 60
SCORE = 0
GAMEOVER = False
PAUSE = False
BOSS = 0

pygame.init()
pygame.mixer.init()

snd_back = pygame.mixer.Sound('sound/back.ogg')
snd_stage1 = pygame.mixer.Sound('sound/bgm.ogg')
snd_stage3 = pygame.mixer.Sound('sound/bgm2.ogg')
snd_item = pygame.mixer.Sound('sound/item.ogg')
snd_shot = pygame.mixer.Sound('sound/shot.ogg')
snd_explo = pygame.mixer.Sound('sound/explosion.ogg')
snd_boss = pygame.mixer.Sound('sound/bgmboss.ogg')

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial",25)

class Background(pygame.sprite.Sprite):
    def __init__(self,dy,dspeedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/back.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = dy
        self.speedy = dspeedy
        
    def update(self):
        self.rect.y -= self.speedy
        if self.rect.y == -HEIGHT:
            self.rect.y = HEIGHT

class Starship(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/starship1.png')
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 50

        self.shotspeed = 1
        self.speedx = 0
        self.speedy = 0

        self.damage = 1
        self.life = 3
        self.shieldtime = 2000
        self.shottime = 850
        self.doubleshot = 0

    def update(self):
        for i in range(myship.life):
            heart = Heart(i*50)
            sprites.add(heart)
            hearts.add(heart)
        self.speedx = 0
        self.speedy = 0
        global PAUSE
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.speedx = -7
        if pressed[pygame.K_RIGHT]:
            self.speedx = 7
        if pressed[pygame.K_UP]:
            self.speedy = -7
        if pressed[pygame.K_DOWN]:
            self.speedy = 7
            
        if (PAUSE == True):
            if pressed[pygame.K_SPACE]:
                self.shot()
            
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.x >= WIDTH - 50:
            self.rect.x = WIDTH - 50
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= HEIGHT - 50:
            self.rect.y = HEIGHT - 50
        if self.rect.y < 0:
            self.rect.y = 0

    def shot(self):
        if (myship.doubleshot == 0):
            if (Stimer.isFinished()):
                snd_shot.play()
                Stimer.start()
                shoot = Energy(self.rect.x+25,self.rect.y)
                sprites.add(shoot)
                shots.add(shoot)
                
        elif (myship.doubleshot == 1):
            if (Stimer.isFinished()):
                snd_shot.play()
                Stimer.start()
                shoot = Energy(self.rect.x+38,self.rect.y)
                sprites.add(shoot)
                shots.add(shoot)
                shoot2 = Energy(self.rect.x+8,self.rect.y)
                sprites.add(shoot2)
                shots.add(shoot2)
                
        elif (myship.doubleshot >= 2):
            if (Stimer.isFinished()):
                snd_shot.play()
                Stimer.start()
                shoot = Energy(self.rect.x+38,self.rect.y)
                sprites.add(shoot)
                shots.add(shoot)
                shoot2 = Energy(self.rect.x+4,self.rect.y)
                sprites.add(shoot2)
                shots.add(shoot2)
                shoot3 = Energy(self.rect.x+20,self.rect.y-5)
                sprites.add(shoot3)
                shots.add(shoot3)
        
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self,dx,dy,dlife):
        pygame.sprite.Sprite.__init__(self)
        self.dimage = random.choice(enemy_list)
        self.image = pygame.image.load(self.dimage)
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.life = dlife
        self.speedx = 1.2      
        
    def update(self):
        self.rect.x += self.speedx
        if (self.rect.x > WIDTH-30) or (self.rect.x < 0):
            self.speedx *= -1
        if (random.random() > 0.996):
            self.shot()
            
    def shot(self):
        Eshoot = Energy_E(self.rect.x+20,self.rect.y+10)
        sprites.add(Eshoot)
        Eshots.add(Eshoot)

    def damage(self):
        self.life -= myship.damage
        if self.life <= 0:
            self.kill()
            
                
class BossShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/bossship.png')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 50
        self.life = 700

    def update(self):
        if (random.random() > 0.970):
            self.shot()
        if (random.random() > 0.990):
            self.rect.x = random.randrange(100,800)
            
    def shot(self):
        for x in range(3):
            for y in range(5):
                Bshoot = Energy_B(self.rect.x+200+x*30,self.rect.y+300+y*30)
                sprites.add(Bshoot)
                Eshots.add(Bshoot)

    def damage(self):
        self.life -= myship.damage
        if self.life <= 0:
            self.kill()
            EndScreen()

    def shieldbar(self):
        pygame.draw.rect(screen,(255,255,255),[50,18,WIDTH-100,20])
        pygame.draw.rect(screen,(255,0,0),[50,18,(boss.life/800)*(WIDTH-100),20])
        

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dimage = random.choice(meteor_list)
        self.image = pygame.image.load(self.dimage)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH)
        self.rect.y = random.randrange(-150,-50)
        self.speedx = random.randrange(1,10)
        self.speedy = random.randrange(-3,3)
    
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.x > WIDTH) or (self.rect.x < -40) or (self.rect.y > WIDTH): 
              self.rect.x = random.randrange(WIDTH) 
              self.rect.y = random.randrange(-150, -50)
              self.speedx = random.randrange(-3,3)
              self.speedy = random.randrange(1, 10)
        
class Energy(pygame.sprite.Sprite):
    def __init__(self,dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/fireball.png')
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.speedy = 5
        
    def update(self):
        self.rect.y -= self.speedy
        if self.rect.y < 0:
            self.kill()

class Energy_E(pygame.sprite.Sprite):
    def __init__(self,dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/Efireball.png')
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.speedy = 6
        
    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT:
            self.kill()

class Energy_B(pygame.sprite.Sprite):
    def __init__(self,dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/energyball_boss.png')
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.targetx = random.randrange(50,800)
        self.targety = 800
    
    def calcVect(self):
        self.vectX = self.targetx - self.rect.x
        self.vectY = self.targety - self.rect.y
        self.length = math.sqrt((self.vectX*self.vectX)+(self.vectY*self.vectY)) 
        if self.length != 0:
            self.normX = self.vectX/self.length
            self.normY = self.vectY/self.length

    def calcVel(self):
        self.rect.x += (self.normX)*8
        self.rect.y += (self.normY)*8

    def delete(self):
        if self.rect.y > HEIGHT or self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()
                
    def update(self):
        self.calcVect()
        self.calcVel()
        self.delete()

class Heart(pygame.sprite.Sprite):
    def __init__(self,dx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/Heart.png')
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = 50

    def update(self):
        self.kill()
        
class Item(pygame.sprite.Sprite):
    def __init__(self,dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.dimage = random.choice(item_list)
        self.image = pygame.image.load(self.dimage)
        self.rect = self.image.get_rect()
        self.rect.x = dx
        self.rect.y = dy
        self.speedx = 5
        self.speedy = 5

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT - 30 or self.rect.y < 0:
            self.speedy *= -1
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speedx *= -1
        

class Stage(pygame.sprite.Sprite):
    def __init__(self):
        global SCORE
        self.score = SCORE
        self.level = 1
        self.cooltime = 3000
        self.fix = True

    def update(self):
        self.score = SCORE
        self.new_stage()
        
    def new_stage(self):
        global PAUSE
        global BOSS
        if(self.level == 1):
            if self.fix:
                timer.start()
                self.fix = False
            Text(100,self.level)
            pygame.display.flip()
            if (timer.isFinished()):
                PAUSE = True
                spawn_E(6,2,2)
                self.level = 1.5
                self.fix = True
  
        if(self.score >= 10000 and self.level == 1.5):
            sprites.remove(meteors)
            meteors.remove(meteors)
            sprites.remove(enemys)
            enemys.remove(enemys)
            sprites.remove(shots)
            shots.remove(shots)
            sprites.remove(Eshots)
            Eshots.remove(Eshots)
            item = Item(WIDTH/2,0)
            sprites.add(item)
            items.add(item)
            self.level = 2
            
        if(self.level == 2):
            if self.fix:
                timer.start()
                PAUSE = False
                self.fix = False
            Text(100,self.level)
            pygame.display.flip()
            if(timer.isFinished()):
                PAUSE = True
                spawn_E(8,3,5)
                spawn_M(5)
                self.level = 2.5
                self.fix = True

        if(self.score >= 50000 and self.level == 2.5):
            sprites.remove(meteors)
            meteors.remove(meteors)
            sprites.remove(enemys)
            enemys.remove(enemys)
            sprites.remove(shots)
            shots.remove(shots)
            sprites.remove(Eshots)
            Eshots.remove(Eshots)
            item = Item(WIDTH/2,0)
            sprites.add(item)
            items.add(item)
            self.level = 3
            
        if(self.level == 3):
            if self.fix:
                timer.start()
                snd_stage1.stop()
                snd_stage3.set_volume(0.1)
                snd_stage3.play(-1)
                PAUSE = False
                self.fix = False
            Text(100,self.level)
            pygame.display.flip()
            if(timer.isFinished()):
                PAUSE = True
                spawn_E(10,3,10)
                spawn_M(10)
                self.level = 3.5
                self.fix = True

        if(self.score >= 150000 and self.level == 3.5):
            sprites.remove(meteors)
            meteors.remove(meteors)
            sprites.remove(enemys)
            enemys.remove(enemys)
            sprites.remove(shots)
            shots.remove(shots)
            sprites.remove(Eshots)
            Eshots.remove(Eshots)
            item = Item(WIDTH/2,0)
            sprites.add(item)
            items.add(item)
            self.level = 4
            
        if(self.level == 4):
            if self.fix:
                timer.start()
                PAUSE = False
                self.fix = False
            Text(100,self.level)
            pygame.display.flip()
            if(timer.isFinished()):
                spawn_E(10,3,30)
                spawn_M(15)
                self.level = 4.5
                PAUSE = True
                self.fix = True
                
        if(self.score >= 400000 and self.level == 4.5):
            sprites.remove(meteors)
            meteors.remove(meteors)
            sprites.remove(enemys)
            enemys.remove(enemys)
            sprites.remove(shots)
            shots.remove(shots)
            sprites.remove(Eshots)
            Eshots.remove(Eshots)
            item = Item(WIDTH/2,0)
            sprites.add(item)
            items.add(item)
            self.level = 5
            
        if(self.level == 5):
            if self.fix:
                timer.start()
                snd_stage3.stop()
                snd_boss.set_volume(0.2)
                snd_boss.play()
                PAUSE = False
                self.fix = False
            Text(100,self.level)
            pygame.display.flip()
            if(timer.isFinished()):
                sprites.add(boss)
                bosses.add(boss)
                boss.shieldbar()
                BOSS = 1
                self.level = 5.5
                PAUSE = True
                self.fix = True
            
class Timer():
    def __init__(self,cooltime):
        self.savedTime = 0
        self.passedTime = 0
        self.totalTime = cooltime
        
    def start(self):
        self.savedTime = pygame.time.get_ticks()

    def isFinished(self):
        self.passedTime = pygame.time.get_ticks() - self.savedTime
        if(self.passedTime > self.totalTime):
            return True
        else:
            return False

def StartScreen():
      image = pygame.image.load('image/background2.jpg')
      screen.fill((0,0,0))
      screen.blit(image,(0,0))
      pygame.display.flip()
      run = 1 
      while run:
          snd_back.set_volume(0.1)
          snd_back.play(-1)
          clock.tick(FPS) 
          for event in pygame.event.get():
              pressed = pygame.key.get_pressed()
              if event.type == pygame.QUIT: 
                    pygame.quit()
              if pressed[pygame.K_SPACE]:
                    snd_back.stop()
                    run = 0
def EndScreen():
      image = pygame.image.load('image/ending.jpg')
      screen.fill((0,0,0))
      screen.blit(image,(0,0))
      pygame.display.flip() 
      waiting = True 
      while waiting: 
          clock.tick(FPS) 
          for event in pygame.event.get(): 
              if event.type == pygame.QUIT: 
                  pygame.quit()
    
def spawn_E(dx,dy,dlife):
    for i in range(dx):
        for j in range(dy):
            enemy = Enemy(i*100,j*80,dlife)
            sprites.add(enemy)
            enemys.add(enemy)

def spawn_M(dx):
    for i in range(dx):
        mto = Meteor()
        sprites.add(mto)
        meteors.add(mto)

def Text(size,stage):
    font_stage = pygame.font.SysFont("Viga",size)
    if stage <= 4:
        text = font_stage.render("STAGE " + str(stage),True,(255,0,0))
        screen.blit(text,(WIDTH/2 - 110, HEIGHT/2 - text.get_height()))
    elif stage == 5:
        text = font_stage.render("BOSS STAGE",True,(255,0,0))
        screen.blit(text,(WIDTH/2 - 200, HEIGHT/2 - text.get_height()))  

sprites = pygame.sprite.Group()
enemys = pygame.sprite.Group()
shots = pygame.sprite.Group()
Eshots = pygame.sprite.Group()
meteors = pygame.sprite.Group()
hearts = pygame.sprite.Group()
items = pygame.sprite.Group()
bosses = pygame.sprite.Group()

background1 = Background(0,1)
background2 = Background(HEIGHT,1)
myship = Starship()
boss = BossShip()
stages = Stage()

timer = Timer(stages.cooltime)
Etimer = Timer(1000)
Stimer = Timer(myship.shottime)
Ktimer = Timer(myship.shieldtime)
Btimer = Timer(1500)

sprites.add(background1)
sprites.add(background2)
sprites.add(myship)

enemy_list = ['image/enemy1.png','image/enemy2.png']
meteor_list = ['image/meteor1.png','image/meteor2.png','image/meteor3.gif']
item_list = ['image/doubleshot.png','image/heartup.png','image/powerup.png','image/speedup.png']

StartScreen()
snd_stage1.set_volume(0.2)
snd_stage1.play(-1)
run = 1
while run:
    if(GAMEOVER == True):
        EndScreen()
    elif (GAMEOVER == False):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0

        enemys.update()
        meteors.update()
        shots.update()
        Eshots.update()
        background1.update()
        background2.update()
        hearts.update()
        myship.update()
        stages.update()
        items.update()
        bosses.update()
    
        collision_e = pygame.sprite.groupcollide(enemys, shots, False, True)
        collision_m = pygame.sprite.groupcollide(shots, meteors, True, True)
        collision_b = pygame.sprite.groupcollide(bosses,shots,False,True)     
        collision_i = pygame.sprite.spritecollide(myship,items,True)
        collision1 = pygame.sprite.spritecollide(myship,enemys,False)
        collision2 = pygame.sprite.spritecollide(myship,meteors,True)
        collision3 = pygame.sprite.spritecollide(myship,Eshots,True)
            
        for enemyi in collision_e:
            for j in collision_e[enemyi]:
                enemyi.damage()
                SCORE += 500*myship.damage
                snd_explo.play()

        for bossi in collision_b:
            for j in collision_b[bossi]:
                bossi.damage()
                SCORE += 500*myship.damage
                snd_explo.play()
                    
        for m in collision_m:
            snd_explo.play()
            SCORE += random.randrange(10,50)
            mto = Meteor()
            sprites.add(mto)
            meteors.add(mto)
            if random.random() > 0.8:
                item = Item(m.rect.x,m.rect.y)
                sprites.add(item)
                items.add(item)
            
        for item in collision_i:
            if(item.dimage == 'image/heartup.png'):
                if myship.life == 5:
                    myship.life = 5
                else:
                    myship.life += 1
                snd_item.set_volume(0.3)
                snd_item.play()
            elif(item.dimage == 'image/powerup.png'):
                snd_item.set_volume(0.3)
                snd_item.play()
            
                if(myship.damage == 10):
                    myship.damage = 10
                else:
                    myship.damage += 1
            elif(item.dimage == 'image/speedup.png'):
                snd_item.set_volume(0.3)
                snd_item.play()
                myship.shotspeed += 1
                if(myship.shotspeed == 2):
                    Stimer = Timer(600)
                elif(myship.shotspeed == 3):
                    Stimer = Timer(400)
                elif(myship.shotspeed == 4):
                    Stimer = Timer(300)
            elif(item.dimage == 'image/doubleshot.png'):
                snd_item.set_volume(0.3)
                snd_item.play()
                myship.doubleshot += 1
            
        if collision2:
            mto = Meteor()
            sprites.add(mto)
            meteors.add(mto)
            
        if collision1 or collision2 or collision3:
            if (Ktimer.isFinished()):
                myship.life -= 1
                snd_explo.play()
                Ktimer.start()
            if(myship.life <= 0):
                GAMEOVER = True
    
        sprites.draw(screen)
        
        text1 = font.render("SCORE : " + str(SCORE),True,(255,255,255))
        screen.blit(text1,(WIDTH/2-40,70))
        
        if(myship.damage <= 9):
            text2 = font.render("POWER : Lv" + str(myship.damage),True,(0,0,255))
        else:
            text2 = font.render("POWER : Lv MAX",True,(255,0,0))
        screen.blit(text2,(820,650))
        
        if(myship.shotspeed <= 3):
            text3 = font.render("SPEED : Lv" + str(myship.shotspeed),True,(0,0,255))
        else:
            text3 = font.render("SPEED : Lv MAX",True,(255,0,0))
        screen.blit(text3,(820,600))
        
        if(BOSS == 1):
            boss.shieldbar()
        pygame.display.flip()
pygame.quit()
