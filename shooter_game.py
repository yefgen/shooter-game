#Создай собственный Шутер!

from pygame import *
from random import *
window = display.set_mode((700, 500))
display.set_caption('Shooter')
back = image.load('galaxy.jpg')
background = transform.scale(back, (700, 500))
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
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
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x < 635:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x > 5:
            self.rect.x += self.speed
class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 450:
            self.rect.y += self.speed
        else:
            self.rect.x = randint(50, 600)
            self.speed = randint(1, 4)
            self.rect.y = 0
            lost += 1
player = Player('rocket.png', 290, 380, 10, 70, 100)
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(50, 600), 0, randint(1, 4), 100, 50)
    enemies.add(enemy)
lost = 0
r = 0
font.init()
nfont = font.Font(None, 40)
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    window.blit(background, (0, 0))
    player.draw()
    player.update()
    enemies.draw(window)
    enemies.update()
    text_l = nfont.render('Пропущено:' + str(lost) , True, (255, 255, 255))
    window.blit(text_l, (10, 10))
    text_r = nfont.render('Есть пробитие:' + str(r) , True, (255, 255, 255))
    window.blit(text_r, (10, 50))
    display.update()
    clock.tick(FPS)