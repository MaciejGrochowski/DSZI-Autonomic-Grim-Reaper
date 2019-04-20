from settings import TILESIZE, PLAYER_SPEED, PLAYER_HIT_RECT
from collisions import *
vec = pg.math.Vector2
from math import floor
from time import sleep


class Reaper(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.reaper
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img_R
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.countsteps = 0


    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.vel = vec(0, -PLAYER_SPEED)
        if keys[pg.K_DOWN]:
            self.vel = vec(0, PLAYER_SPEED)
        if keys[pg.K_RIGHT]:
            self.vel = vec(PLAYER_SPEED, 0)
            if (self.image == self.game.player_img_L):
                self.image = self.game.player_img_R
        if keys[pg.K_LEFT]:
            self.vel = vec(-PLAYER_SPEED, 0)
            if (self.image == self.game.player_img_R):
                self.image = self.game.player_img_L

    def update(self):
        self.get_keys()
        self.rect.center = self.pos
        self.pos += self.vel
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        #print(str(self.game.agent.pos / 64))
        #if(collide_with_people(self, self.game.people, 'x') or collide_with_people(self, self.game.people, 'y')):
           #self.game.drawPeople =  <- kolizje z ludźmi, na kiedyś

    def go_to(self, game, newpos):
        self.target = vec(0,0)
        self.target.x = newpos[0]
        self.target.y = newpos[1]
        self.pos.y = floor(self.pos.y)
        self.pos.x = floor(self.pos.x)
        self.target.x = self.target.x - game.camera.x
        self.target.y = self.target.y - game.camera.y
        self.target.x = (self.target.x - self.target.x%16) + 16
        self.target.y = self.target.y - self.target.y%16 + 16
        print(self.target)
        oldposx = 0
        oldposy = 0
        #print(game.camera.x)
        while(True):
            if(oldposx == self.pos.x and oldposy == self.pos.y):
                break
            oldposx = self.pos.x
            oldposy = self.pos.y
            if self.target.x == self.pos.x and self.target.y == self.pos.y:
                break
            if self.target.x > self.pos.x:
                self.pos.x += 16
                if self.target.x - self.pos.x > 16 and (self.image == self.game.player_img_L):
                    self.image = self.game.player_img_R
                    self.countsteps += 1
                #prawo
            if self.target.x < self.pos.x:
                self.pos.x -= 16
                if self.pos.x - self.target.x > 16 and self.image == self.game.player_img_R:
                        self.image = self.game.player_img_L
                        self.countsteps += 1
                #lewo
            if self.target.y > self.pos.y:
                self.pos.y += 16
                #dol
            if self.target.y < self.pos.y:
                self.pos.y -= 16
                #gora
            hits = pg.sprite.spritecollide(self, self.game.people, True, collide_hit_rect)
            if hits:
                print("Chomik")
                for sprite in hits:
                    sprite.banish()
            print(self.game.people)
            sleep(0.02)
            self.countsteps += 1
            game.update()
            game.draw()
        self.countsteps -= 1



