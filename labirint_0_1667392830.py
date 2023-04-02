# Розроби свою гру в цьому файлі!
from pygame import *
import math
win_width=700
win_height=500
display.set_caption('Hotline Zhytomyr')
window = display.set_mode((win_width, win_height))
back=image.load('ground.jpg')
back=transform.scale(back,(win_width, win_height))

class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y)) 
 
class Mc(GameSprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed, pos): 
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed=player_x_speed
        self.y_speed=player_y_speed
        self.original_image = image.load('hero.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (player_x, player_y))
    def update(self):
        if gg.rect.x <= win_width-80 and gg.x_speed > 0 or gg.rect.x >= 0 and gg.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if gg.rect.y <= win_height-80 and gg.y_speed > 0 or gg.rect.y >= 0 and gg.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def rotate(self, player_x, player_y):
        direction = Vector2(player_x, player_y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def fire(self, mousepos):
        dx = mousepos[0] - self.rect.centerx
        dy = mousepos[1] - self.rect.centery
        if abs(dx) > 0 or abs(dy) > 0:
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <=420:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self. side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, x, y, dx, dy):
        sprite.Sprite.__init__(self)
        self.image = transform.smoothscale(image.load('bullet.png').convert_alpha(), (7,7))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 40
        self.pos = Vector2(x, y)
        self.dir = Vector2(dx, dy).normalize()
    def update(self):
        self.pos += self.dir * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        
barriers = sprite.Group()
bullets = sprite.Group()
bad = sprite.Group()

car1=GameSprite('car1.png', 450, 250, 250, 120)
car2=GameSprite('car2.png', 100, 80, 250, 120)
car3=GameSprite('car3.png', 320, 190, 100, 170)

barriers.add(car1)
barriers.add(car2)
barriers.add(car3)

gg = Mc('hero.png', 8, win_height - 80, 80, 80, 0, 0, 220)
enemy = Enemy('enemy.png', win_width - 80, 180, 70, 80, 10)
enemy1 = Enemy('enemy.png', win_width - 400, 50, 70, 80, 5)
endup = GameSprite('gpu.png', win_width - 85, 200, 40, 20)

bad.add(enemy)
bad.add(enemy1)

finish = False
run=True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                gg.x_speed = -5
            elif e.key == K_d:
                gg.x_speed = 5
            elif e.key == K_w:
                gg.y_speed = -5
            elif e.key == K_s:
                gg.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_a:
                gg.x_speed = 0
            elif e.key == K_d:
                gg.x_speed = 0
            elif e.key == K_w:
                gg.y_speed = 0
            elif e.key == K_s:
                gg.y_speed = 0
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                gg.fire(mouse.get_pos())
    gg.rotate(*mouse.get_pos())
    if not finish:
        window.blit(back, (0, 0))
        barriers.draw(window)
        bullets.update()
        bullets.draw(window)
        endup.reset()
        gg.reset()
        gg.update()
        sprite.groupcollide(bad, bullets, True, True)
        bad.update()
        bad.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        if sprite.spritecollide(gg, bad, True):
            finish = True
            img = image.load('go.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
        if sprite.collide_rect(gg, endup):
            finish = True
            img = image.load('win.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
        time.delay(50)
        display.update()
