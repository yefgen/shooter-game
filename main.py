from pygame import *
import random
from time import time as tm

window = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
display.set_caption('Shooter')

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
# mixer.music.play()

shoot_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        if pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if pressed[K_d] and self.rect.x < 625:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 450:
            self.rect.y += self.speed
        else:
            self.rect.x = random.randint(50, 600)
            self.speed = random.randint(1, 4)
            self.rect.y = 0
            lost += 1

class Asteriod(GameSprite):
    def update(self):
        if self.rect.y < 450:
            self.rect.y += self.speed
        else:
            self.rect.x = random.randint(50, 600)
            self.speed = random.randint(1, 4)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

player = Player('rocket.png', 290, 380, 10, 70, 100)
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', random.randint(50, 600), 0, random.randint(1, 4), 100, 50)
    enemies.add(enemy)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteriod('asteroid.png', random.randint(50, 600), 0, random.randint(2, 5), 40, 40)
    asteroids.add(asteroid)

lost = 0
shooted = 0
game = True
finish = False

font.init()
nfont = font.Font(None, 40)

num_fire = 0
rel_time = False

lives = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    player.fire()
                    num_fire += 1
                    shoot_sound.play()

                if num_fire > 4 and not rel_time:
                    rel_time = True
                    last_shoot = tm()

    if not finish:
        window.blit(background, (0, 0))
        player.draw()
        player.update()
        enemies.draw(window)
        enemies.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()

        text_lost = nfont.render('Пропущено: ' + str(lost), True, (255,255,255))
        window.blit(text_lost, (10, 10))

        text_shooted = nfont.render('Сбито врагов: ' + str(shooted), True, (255,255,255))
        window.blit(text_shooted, (10, 50))

        lives_text = nfont.render(str(lives), True, (255,255,255))
        window.blit(lives_text, (670, 450))

        collides = sprite.groupcollide(bullets, enemies, True, True)
        for col in collides:
            shooted += 1
            enemy = Enemy('ufo.png', random.randint(50, 600), 0, random.randint(1, 4), 100, 50)
            enemies.add(enemy)

        sprite.groupcollide(bullets, asteroids, True, False)

        if sprite.spritecollide(player, enemies, True):
            lives -= 1
            enemy = Enemy('ufo.png', random.randint(50, 600), 0, random.randint(1, 4), 100, 50)
            enemies.add(enemy)

        if sprite.spritecollide(player, asteroids, True):
            lives -= 1
            asteroid = Asteriod('asteroid.png', random.randint(50, 600), 0, random.randint(2, 5), 40, 40)
            asteroids.add(asteroid)

        if lives < 1 or lost >= 3:
            finish = True
            lose = nfont.render('YOU LOSE!', True, (255, 0, 0))
            window.blit(lose, (300, 220))

        if shooted >= 10:
            finish = True
            win = nfont.render('YOU WIN!', True, (0, 255, 0))
            window.blit(win, (300, 220))

        if rel_time:
            now_time = tm()
            if now_time - last_shoot < 3:
                reload = nfont.render('Перезарядка', True, (255, 0, 0))
                window.blit(reload, (280, 420))
            else:
                num_fire = 0
                rel_time = False

        display.update()

    else:
        finish = False
        shooted = 0
        lost = 0
        for bul in bullets:
            bul.kill()
        for enemy in enemies:
            enemy.kill()
        for ast in asteroids:
            ast.kill()

        time.delay(5000)

        lives = 3

        num_fire = 0
        rel_time = False

        for i in range(5):
            enemy = Enemy('ufo.png', random.randint(50, 600), 0, random.randint(1, 4), 100, 50)
            enemies.add(enemy)

        for i in range(3):
            asteroid = Asteriod('asteroid.png', random.randint(50, 600), 0, random.randint(2, 5), 40, 40)
            asteroids.add(asteroid)
    clock.tick(FPS)