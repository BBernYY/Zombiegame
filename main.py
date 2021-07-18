import pygame
import random
import os
import json
from pygame import mixer
pygame.init()
from pygame.rect import Rect
WX, WY = 900, 500
FPS = 60
WIN = pygame.display.set_mode((WX, WY))
VEL = 10
current = 0
BG = pygame.image.load(os.path.join("assets", "lvl1", "bg.png"))
DATA = []
pygame.display.set_caption("Zombiespel - Beta 0.4")
gameIcon = pygame.image.load(os.path.join("assets", "lvl1", "zombie.png"))
pygame.display.set_icon(gameIcon)
pygame.mixer.music.set_volume(0.25)
for i in os.listdir("mods"):
    ext = os.path.splitext(i)[1]
    print(ext)
    if ext == ".json":
        f = open(os.path.join("mods", i), 'r')
        DATA.append(json.load(f))
        f.close()
def getpath(dir):
    global ans
    ans = dir
    for i in DATA:
        i_target_path = os.path.join("assets", "lvl" + str(i["lvltarget"]), i["imagetarget"])
        if i_target_path == dir:
            ans = os.path.join("mods", i["image"])
    return ans
class zombie:
    FACTOR = 0.25
    WIDTH, HEIGHT = round(16 / FACTOR), round(16 / FACTOR)
    RECT = pygame.Rect(100, 300, WIDTH, HEIGHT)
    RAWEAT = os.path.join("assets", "lvl1", "brains.wav")
    LVL = 1
    XP = 0
    XPPEREAT = 1
    XPNEEDED = 1
    ANGLE = 0
    EATSOUND = 0
    ROT = 0
    TICKS_AFTER_START = 0
    START_TICKS = 0
    RAW = pygame.image.load(getpath(os.path.join("assets", "lvl" + str(LVL), "zombie.png")))
    RAW0 = pygame.image.load(getpath(os.path.join("assets", "lvl" + str(LVL), "zombie.png")))
    RAW90 = pygame.transform.rotate(pygame.image.load(getpath(os.path.join("assets", "lvl" + str(LVL), "zombie.png"))), 90)
    RAW180 = pygame.transform.rotate(pygame.image.load(getpath(os.path.join("assets", "lvl" + str(LVL), "zombie.png"))), 180)
    RAW270 = pygame.transform.rotate(pygame.image.load(getpath(os.path.join("assets", "lvl" + str(LVL), "zombie.png"))), 270)
pygame.mixer.music.load(os.path.join("assets", "song.wav"))
pygame.mixer.music.play(-1)
class nut:
    RAW = os.path.join("assets", "lvl1", "brain.png")
    RAWOPEN = os.path.join("assets", "lvl1", "openBrain.png")
    FACTOR = 0.25
    WIDTH, HEIGHT = round(16 / FACTOR), round(16 / FACTOR)
    IMAGE = pygame.transform.scale(pygame.image.load(RAW), (WIDTH, HEIGHT))
    RECT = pygame.Rect(random.randint(0, WX - WIDTH), random.randint(0, WY - HEIGHT), WIDTH, HEIGHT)
    NUTMIDX, NUTMIDY = WIDTH / 2, HEIGHT / 2
class draw:
    WINTYPE = "MENU"
    def GAME():
        zombie.IMAGE = pygame.transform.scale(zombie.RAW, (zombie.WIDTH, zombie.HEIGHT))
        WIN.blit(BG, (0, 0))
        lvlfont = pygame.font.SysFont('couriernew', 50)
        WIN.blit(lvlfont.render(str(zombie.LVL), False, (255, 255, 255)), (0, 0))
        lvlfont = pygame.font.SysFont('couriernew', 15)
        WIN.blit(lvlfont.render(str(zombie.XP) + ' / ' + str(zombie.XPNEEDED), False, (255, 255, 255)), (50, 0))
        WIN.blit(zombie.IMAGE, (zombie.RECT.x, zombie.RECT.y))
        WIN.blit(nut.IMAGE, (nut.RECT.x, nut.RECT.y))
        pygame.display.update()
    def MENU():
        WIN.blit(BG, (0, 0))
        menufont = pygame.font.SysFont('couriernew', 50)
        WIN.blit(menufont.render("Zombiespel", False, (255, 255, 255)), (WX // 2 - 150, WY // 2 - 100))
        menufont = pygame.font.SysFont('couriernew', 20)
        WIN.blit(menufont.render("Press space to start", False, (255, 255, 255)), (WX // 2 - 125, WY // 2 + 200))
        pygame.display.update()
def catchcheck(rect1, rect2):
    global current
    if rect1.colliderect(rect2) and current == 0:
        zombie.EATSOUND = pygame.mixer.Sound(zombie.RAWEAT)
        current = pygame.time.get_ticks()
        zombie.EATSOUND.play()
        nut.IMAGE = pygame.transform.scale(pygame.image.load(nut.RAWOPEN), (nut.WIDTH, nut.HEIGHT))
    if rect1.colliderect(rect2) and (pygame.time.get_ticks() - 1000) > current:
        current = 0
        zombie.XP += zombie.XPPEREAT
        nut.RECT = pygame.Rect(random.randint(0, WX - nut.WIDTH), random.randint(0, WY - nut.HEIGHT), nut.WIDTH, nut.HEIGHT)
        nut.IMAGE = pygame.transform.scale(pygame.image.load(nut.RAW), (nut.WIDTH, nut.HEIGHT))
        zombie.TOUCHTIME = 0
def keycheck():
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_a]:
        zombie.RECT.x -= VEL
        zombie.RAW = zombie.RAW90
    if keys_pressed[pygame.K_d]:
        zombie.RECT.x += VEL
        zombie.RAW = zombie.RAW270
    if keys_pressed[pygame.K_w]:
        zombie.RECT.y -= VEL
        zombie.RAW = zombie.RAW0
    if keys_pressed[pygame.K_s]:
        zombie.RECT.y += VEL
        zombie.RAW = zombie.RAW180
    if keys_pressed[pygame.K_SPACE] and draw.WINTYPE == "MENU":
        draw.WINTYPE = "GAME"
        zombie.START_TICKS = 0 - pygame.time.get_ticks()
        print('hello')
def levelupcheck():
    global BG
    if zombie.XP >= zombie.XPNEEDED:
        zombie.LVL += 1
        zombie.XP = 0
        if zombie.LVL <= 5:
            zombie.RAW = pygame.image.load(getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "zombie.png")))
            zombie.RAW0 = pygame.image.load(getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "zombie.png")))
            zombie.RAW90 = pygame.transform.rotate(pygame.image.load(getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "zombie.png"))), 90)
            zombie.RAW180 = pygame.transform.rotate(pygame.image.load(getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "zombie.png"))), 180)
            zombie.RAW270 = pygame.transform.rotate(pygame.image.load(getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "zombie.png"))), 270)
            zombie.RAWEAT = getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "brains.wav"))
            nut.RAW = getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "brain.png"))
            nut.RAWOPEN = getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "openBrain.png"))
            nut.IMAGE = pygame.transform.scale(pygame.image.load(nut.RAW), (nut.WIDTH, nut.HEIGHT))
            BG = pygame.image.load(getpath(os.path.join("assets", "lvl" + str(zombie.LVL), "bg.png")))
def getpath(dir):
    global ans
    ans = dir
    for i in DATA:
        i_target_path = os.path.join("assets", "lvl" + str(i["lvltarget"]), i["imagetarget"])
        if i_target_path == dir:
            ans = os.path.join("mods", i["image"])
    return ans
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        zombie.TICKS_AFTER_START = pygame.time.get_ticks() + zombie.START_TICKS
        zombie.XPNEEDED = zombie.LVL**4 * 1000
        zombie.XPPEREAT = zombie.TICKS_AFTER_START//10000 * 100 + 100
        if draw.WINTYPE == "GAME":
            draw.GAME()
        else:
            draw.MENU()
        keycheck()
        levelupcheck()
        catchcheck(zombie.RECT, nut.RECT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
if __name__ == "__main__":
    main()