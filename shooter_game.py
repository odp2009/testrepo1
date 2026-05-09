from pygame import *
from random import randint


miss = 0
hit = 0
lives = 3
#SPRITES#
class GameSprite(sprite.Sprite):
    def __init__(self, image_spr, x, y, speed, width, height):
        super().__init__()
        self.height = height
        self.width = width
        self.image = transform.scale(image.load(image_spr), (self.width, self.height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_LEFT] or keys_pressed[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys_pressed[K_RIGHT] or keys_pressed[K_d]) and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10, 10, 35)
        bullet.add(group_bullets)

class Enemy(GameSprite):
    def update(self):
        global miss
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            self.rect.y = 0 
            self.rect.x = randint(0,635)
            self.speed = randint(1,3)
            miss += 1

class Obstacle(GameSprite):
    def update(self):
        global miss
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            self.rect.y = 0 
            self.rect.x = randint(0,635)
            self.speed = randint(1,3)
            

       
        

#SETUP#
width = 700
height = 500
window = display.set_mode((width,height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"),(width,height))
clock = time.Clock()
FPS = 60

#MUSIC#
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")
boom = mixer.Sound("boom.mp3")
fahh = mixer.Sound("fahh.mp3")
yipee = mixer.Sound("yippee.mp3")

#TEXT#
font.init()
style = font.SysFont('Arial', 36)
txt_win = style.render("YOU WIN!!!", True, (90, 255, 90)) 
txt_lose = style.render("YOU LOSE!!!", True, (255, 0, 0))

#SPRITES#
sprite_player = Player("rocket.png", 300, 380, 5, 65, 100)
group_bullets = sprite.Group()
group_ufos = sprite.Group()
group_asteroids = sprite.Group()
for i in range(5):
    sprite_ufo = Enemy("ufo.png", randint(0, 650), 5, randint(2, 3), 100, 50)
    group_ufos.add(sprite_ufo)
for i in range(2):
    sprite_asteroid = Obstacle("asteroid.png", randint(0, 650), 5, randint(2,3), 100, 50)
    group_asteroids.add(sprite_asteroid)



#GAME LOOP#
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            keys_pressed = key.get_pressed() 
            if (keys_pressed[K_SPACE]):
                sprite_player.fire()
                fire.play()

            
        
    if finish != True:
        window.blit(background, (0,0))
        sprite_player.reset()
        sprite_player.update()
        group_ufos.update()
        group_bullets.update()
        group_asteroids.update()
        group_ufos.draw(window)
        group_bullets.draw(window)
        group_asteroids.draw(window)
        text_miss = style.render("Missed:" + str(miss) , 1 , (255, 255, 255))
        window.blit(text_miss, (10,10))
        text_hit = style.render("Hit:" + str(hit) , 1 , (255, 255, 255))
        window.blit(text_hit, (10,50))
        text_lives = style.render("Lives:" + str(lives), 1 ,(255, 255, 255))
        window.blit(text_lives, (550,20))

        bullet_collisions = sprite.groupcollide(group_ufos, group_bullets, True, True)
        for c in bullet_collisions:
            hit += 1
            sprite_ufo = Enemy("ufo.png", randint(0, 650), 5, randint(2, 3), 100, 50)
            group_ufos.add(sprite_ufo)
        
        sprite.groupcollide(group_asteroids, group_bullets, False, True)

        if sprite.spritecollide(sprite_player, group_ufos, True) or sprite.spritecollide(sprite_player, group_asteroids, True):
            lives -= 1
            boom.play()





        if miss > 5 or lives == 0:
            window.blit(txt_lose, (280, 230))
            finish = True
            fahh.play()
            
        elif hit > 10:
            window.blit(txt_win, (280, 230))
            finish = True
            yipee.play()
            
            

        clock.tick(FPS)
        display.update()






