from __future__ import division
import pygame
import random
from os import path

resim_dosyasi = path.join(path.dirname(__file__), 'gorseller')
ses_dosyasi = path.join(path.dirname(__file__), 'sesler')


WIDTH = 480
HEIGHT = 600
FPS = 60
GUCLENDIRME_ZAMANI = 5000
BAR_UZUNLUGU = 100
BAR_YUKSEKLİGİ = 10


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Uzay Yolcusu")
saat = pygame.time.Clock()    
font_name = pygame.font.match_font('arial')

def ana_menu():
    global screen

    menu_sesi = pygame.mixer.music.load(path.join(ses_dosyasi, "menu.ogg"))
    pygame.mixer.music.play(-1)

    baslik = pygame.image.load(path.join(resim_dosyasi, "main.png")).convert()
    baslik = pygame.transform.scale(baslik, (WIDTH, HEIGHT), screen)

    screen.blit(baslik, (0,0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            ciz(screen, "Başlamak için [ENTER] tuşuna basınız.", 30, WIDTH/2, HEIGHT/2)
            ciz(screen, "Çıkmak için [Q] tuşuna basınız.", 30, WIDTH/2, (HEIGHT/2)+40)
            pygame.display.update()

 
    hazir = pygame.mixer.Sound(path.join(ses_dosyasi,'getready.ogg'))
    hazir.play()
    screen.fill(BLACK)
    ciz(screen, "HAZIRLAN!", 40, WIDTH/2, HEIGHT/2)
    pygame.display.update()
    

def ciz(surf, text, boyut, x, y):
    font = pygame.font.Font(font_name, boyut)
    text_surface = font.render(text, True, WHITE)      
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def kalkan(surf, x, y, pct):
    pct = max(pct, 0) 
    fill = (pct / 100) * BAR_UZUNLUGU
    outline_rect = pygame.Rect(x, y, BAR_UZUNLUGU, BAR_YUKSEKLİGİ)
    fill_rect = pygame.Rect(x, y, fill, BAR_YUKSEKLİGİ)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def ciz_can(surf, x, y, can, img):
    for i in range(can):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

class Patlama(pygame.sprite.Sprite):
    def __init__(self, center, boyut):
        pygame.sprite.Sprite.__init__(self)
        self.boyut = boyut
        self.image = patlama_anim[self.boyut][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.son_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        anlik = pygame.time.get_ticks()
        if anlik - self.son_update > self.frame_rate:
            self.son_update = anlik
            self.frame += 1
            if self.frame == len(patlama_anim[self.boyut]):
                self.kill()
            else:
                center = self.rect.center
                self.image = patlama_anim[self.boyut][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Oyuncu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(oyuncu_resmi, (50, 38))
        self.image.set_colorkey(BLACK)     
        self.rect = self.image.get_rect()
        self.cap = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.hizx = 0 
        self.kalkan = 100
        self.vurus_gecikme = 250
        self.son_vurus = pygame.time.get_ticks()
        self.can = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.guc = 1
        self.guc_zamani = pygame.time.get_ticks()

    def update(self):
        if self.guc >=2 and pygame.time.get_ticks() - self.guc_zamani > GUCLENDIRME_ZAMANI:
            self.guc -= 1
            self.guc_zamani = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.hizx = 0   
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.hizx = -5
        elif keystate[pygame.K_RIGHT]:
            self.hizx = 5

        if keystate[pygame.K_SPACE]:
            self.vurus()

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.hizx

    def vurus(self):
        anlik = pygame.time.get_ticks()
        if anlik - self.son_vurus > self.vurus_gecikme:
            self.son_vurus = anlik
            if self.guc == 1:
                mermi = Mermi(self.rect.centerx, self.rect.top)
                all_sprites.add(mermi)
                mermiler.add(mermi)
                vurus_sesi.play()
            if self.guc == 2:
                mermi1 = Mermi(self.rect.left, self.rect.centery)
                mermi2 = Mermi(self.rect.right, self.rect.centery)
                all_sprites.add(mermi1)
                all_sprites.add(mermi2)
                mermiler.add(mermi1)
                mermiler.add(mermi2)
                vurus_sesi.play()

            if self.guc >= 3:
                mermi1 = Mermi(self.rect.left, self.rect.centery)
                mermi2 = Mermi(self.rect.right, self.rect.centery)
                fuze1 = Fuze(self.rect.centerx, self.rect.top) 
                all_sprites.add(mermi1)
                all_sprites.add(mermi2)
                all_sprites.add(fuze1)
                mermiler.add(mermi1)
                mermiler.add(mermi2)
                mermiler.add(fuze1)
                vurus_sesi.play()
                fuze_sesi.play()

    def guclendirme(self):
        self.guc += 1
        self.guc_zamani = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_resmi)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.cap = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.hizy = random.randrange(5, 20)        
        self.hizx = random.randrange(-3, 3)

        self.rotation = 0
        self.rotation_hiz = random.randrange(-8, 8)
        self.son_update = pygame.time.get_ticks()  
        
    def rotate(self):
        anlik_zaman = pygame.time.get_ticks()
        if anlik_zaman - self.son_update > 50:
            self.son_update = anlik_zaman
            self.rotation = (self.rotation + self.rotation_hiz) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.hizx
        self.rect.y += self.hizy
        

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.hizy = random.randrange(1, 8)       
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['kalkan', 'silah'])
        self.image = guclendirme_resim[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.hizy = 2

    def update(self):
        self.rect.y += self.hizy
        if self.rect.top > HEIGHT:
            self.kill()

            

class Mermi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = mermi_resmi
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y 
        self.rect.centerx = x
        self.hizy = -10

    def update(self):
        self.rect.y += self.hizy
        if self.rect.bottom < 0:
            self.kill()

class Fuze(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = fuze_resmi
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.hizy = -10

    def update(self):
        self.rect.y += self.hizy
        if self.rect.bottom < 0:
            self.kill()



arkaplan = pygame.image.load(path.join(resim_dosyasi, 'starfield.png')).convert()
arkaplan_rect = arkaplan.get_rect()

oyuncu_resmi = pygame.image.load(path.join(resim_dosyasi, 'playerShip1_orange.png')).convert()
oyuncu_mini_resim = pygame.transform.scale(oyuncu_resmi, (25, 19))
oyuncu_mini_resim.set_colorkey(BLACK)
mermi_resmi = pygame.image.load(path.join(resim_dosyasi, 'laserRed16.png')).convert()
fuze_resmi = pygame.image.load(path.join(resim_dosyasi, 'missile.png')).convert_alpha()
meteor_resmi = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_resmi.append(pygame.image.load(path.join(resim_dosyasi, image)).convert())

patlama_anim = {}
patlama_anim['lg'] = []
patlama_anim['sm'] = []
patlama_anim['oyuncu'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(resim_dosyasi, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    patlama_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    patlama_anim['sm'].append(img_sm)

    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(resim_dosyasi, filename)).convert()
    img.set_colorkey(BLACK)
    patlama_anim['oyuncu'].append(img)

guclendirme_resim = {}
guclendirme_resim['kalkan'] = pygame.image.load(path.join(resim_dosyasi, 'shield_gold.png')).convert()
guclendirme_resim['silah'] = pygame.image.load(path.join(resim_dosyasi, 'bolt_gold.png')).convert()


vurus_sesi = pygame.mixer.Sound(path.join(ses_dosyasi, 'pew.wav'))
fuze_sesi = pygame.mixer.Sound(path.join(ses_dosyasi, 'rocket.ogg'))
expl_sesler = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sesler.append(pygame.mixer.Sound(path.join(ses_dosyasi, sound)))
pygame.mixer.music.set_volume(0.2)     

oyuncu_olum_sesi = pygame.mixer.Sound(path.join(ses_dosyasi, 'rumble1.ogg'))


baslangic = True
menu_gorunum = True
while baslangic:
    if menu_gorunum:
        ana_menu()
        pygame.time.wait(3000)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(path.join(ses_dosyasi, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.play(-1)     
        
        menu_gorunum = False
        
        all_sprites = pygame.sprite.Group()
        oyuncu = Oyuncu()
        all_sprites.add(oyuncu)

        mobs = pygame.sprite.Group()
        for i in range(8):      
            newmob()

        mermiler = pygame.sprite.Group()
        guclendirmeler = pygame.sprite.Group()

        score = 0
        
    saat.tick(FPS)     
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            baslangic = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                baslangic = False
  
    all_sprites.update()


    isabetler = pygame.sprite.groupcollide(mobs, mermiler, True, True)
    for isabet in isabetler:
        score += 50 - isabet.cap         
        random.choice(expl_sesler).play()
        expl = Patlama(isabet.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(isabet.rect.center)
            all_sprites.add(pow)
            guclendirmeler.add(pow)
        newmob()       
    isabetler = pygame.sprite.spritecollide(oyuncu, mobs, True, pygame.sprite.collide_circle)        
    for isabet in isabetler:
        oyuncu.kalkan -= isabet.cap * 2
        expl = Patlama(isabet.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if oyuncu.kalkan <= 0: 
            oyuncu_olum_sesi.play()
            olum_patlama = Patlama(oyuncu.rect.center, 'oyuncu')
            all_sprites.add(olum_patlama)
            oyuncu.hide()
            oyuncu.can -= 1
            oyuncu.kalkan = 100

    isabetler = pygame.sprite.spritecollide(oyuncu, guclendirmeler, True)
    for isabet in isabetler:
        if isabet.type == 'kalkan':
            oyuncu.kalkan += random.randrange(10, 30)
            if oyuncu.kalkan >= 100:
                oyuncu.kalkan = 100
        if isabet.type == 'silah':
            oyuncu.guclendirme()

    if oyuncu.can == 0 and not olum_patlama.alive():
        baslangic = False
    screen.fill(BLACK)
    screen.blit(arkaplan, arkaplan_rect)

    all_sprites.draw(screen)
    ciz(screen, str(score), 18, WIDTH / 2, 10)    
    kalkan(screen, 5, 5, oyuncu.kalkan)

    ciz_can(screen, WIDTH - 100, 5, oyuncu.can, oyuncu_mini_resim)


    pygame.display.flip()       

pygame.quit()
