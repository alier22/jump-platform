# Sprite classes for platform game


from settings import *
import pygame as pg
vec = pg.math.Vector2 
# 2차원 벡터 클래스 (위치, 속도, 가속도 표현하고 조작 가능)
# 게임 객체의 이동, 충돌 감지, 힘 및 방향 계산 들을 구현할 수 있다.


class Player(pg.sprite.Sprite):
    def __init__(self,game):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)# 객체의 위치를 나타내는 변수
        self.vel = vec(0, 0)# vel = 속도, 초기 속도 0 , 정지를 의미
        self.acc = vec(0, 0) # acc = 가속도 , 초기 가속도 0으로 설정

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(1009, 372, 339, 419, scale = 0.65),
                                self.game.spritesheet.get_image(1009, 372, 339, 419, scale = 0.65)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(1, 372, 334, 383, scale = 0.65),
                              self.game.spritesheet.get_image(337, 372, 326, 384, scale = 0.65)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(1372, 1, 343, 369, scale = 0.65)
        self.jump_frame.set_colorkey(BLACK)


    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
                
    def jump(self):
        
        # jump only if standing
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            
            self.jumping = True
            self.game.jump_sound.play()
            self.vel.y = -PLAYER_JUMP



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
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


