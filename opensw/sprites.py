# Sprite classes for platform game


from settings import *
import pygame as pg
vec = pg.math.Vector2 
# 2차원 벡터 클래스 (위치, 속도, 가속도 표현하고 조작 가능)
# 게임 객체의 이동, 충돌 감지, 힘 및 방향 계산 들을 구현할 수 있다.


class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH /2 , HEIGHT /2)
        self.pos = vec(WIDTH/2, HEIGHT/2)# 객체의 위치를 나타내는 변수
        self.vel = vec(0, 0)# vel = 속도, 초기 속도 0 , 정지를 의미
        self.acc = vec(0, 0) # acc = 가속도 , 초기 가속도 0으로 설정

    def jump(self):
        
        # jump only if standing
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -40



    def update(self):
        self.acc = vec(0, PLAYER_GRAV) 
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]: 
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]: 
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #wrap around the side of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.top = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y






