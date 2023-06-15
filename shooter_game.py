from pygame import *
from random import randint
wd = display.set_mode((1080,720))
display.set_caption('Галактическая битва миров 228')
fon = transform.scale(image.load("kosmos.jpeg"), (1080,720))
mixer.init()
mixer.music.load('softspace_-_Sun.mp3')
mixer.music.play()
start = True
clock = time.Clock()
fps = 60
font.init()
font1 = font.SysFont('Ubuntu', 42)
font2 = font.SysFont('Ubuntu', 72)
font3 = font.SysFont('Ubuntu', 180)


lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load (player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        wd.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > -25:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 985:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 9, self.rect.top - 15, 20, 35, -6)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 615:
            self.rect.y = 0
            self.rect.x = randint(-10, 1055)
            lost = lost + 1
class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 615:
            self.rect.y = 0
            self.rect.x = randint(-10, 1055)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()
asteroids = sprite.Group()
for  i in range(1,4):
    asteroid = Enemy2('asteroid.png', randint(-10, 1055), 0, 50, 40, randint(1,7))
    asteroids.add(asteroid)
monsters = sprite.Group()
for i in range(1,5):
    monster = Enemy('ufo.png', randint(-10, 1055), 5, 65, 50, randint(1,7))
    monsters.add(monster)
ship = Player('images-removebg-preview.png', 525, 585, 140, 115, 14)
cerdehko = image.load('Без_названия-removebg-preview.png')
cerdehko = transform.scale(cerdehko, (175, 105))
live = 3
finish = False
while start:
    for e in event.get():
        if e.type == QUIT:
            start = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
    if not finish:
        wd.blit(fon, (0,0))
        wd.blit(cerdehko, (925, 10))
        asteroids.update()
        monsters.update()
        ship.update()
        bullets.update()
        text = font1.render('Збито:' + str (score), 1, (255, 255, 255))
        wd.blit(text,(10, 50))
        text_lost = font1.render('Пропущено:' + str (lost), 1, (255, 255, 255))
        wd.blit(text_lost,(10, 10))
        text_live = font2.render(str (live), 1,(42, 226, 235))
        wd.blit(text_live,(996, 20))
        asteroids.draw(wd)
        monsters.draw(wd)
        bullets.draw(wd)
        ship.reset()
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in sprite_list:
            score += 1
            monster = Enemy('ufo.png', randint(-10, 1055), 5, 65, 50, randint(1,6))
            monsters.add(monster)
        if sprite.spritecollide(ship, asteroids, False):
            live -= 1
            sprite.spritecollide(ship, asteroids, True)
        if sprite.spritecollide(ship, monsters, False):
            live -= 1
            sprite.spritecollide(ship, monsters, True)
        if live < 0:
            text_lose = font3.render('Lose', 1, (217, 11, 42))
            wd.blit(text_lose, (380, 220))
            finish = True
        if score > 20:
            text_win = font3.render('Win', 1, (2, 245, 23))
            wd.blit(text_win, (420, 220))
            finish = True
        display.update()
    else:
        time.delay(5000)
        score = 0
        lost = 0 
        live = 3
        finish = False
        for i in bullets:
            i.kill()
        for i1 in monsters:
            i1.kill()
        for i2 in asteroids:
            i2.kill()
        for i in range(1,6):
            monster = Enemy('ufo.png', randint(-10, 1055), 5, 65, 50, randint(1,7))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy2('asteroid.png', randint(-10, 1055), 0, 50, 40, randint(1,7))
            asteroids.add(asteroid)
    clock.tick(fps)