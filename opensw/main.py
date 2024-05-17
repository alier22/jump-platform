
#Jumpy! - platform game
import pygame as pg  # type: ignore
import random
from settings import *
from sprites import * 
from os import path

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        
    def load_data(self):
        #load high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE),"w") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = -1
    
    
    def new(self):
        #reset game(게임 죽으면 다시 시작하는거)
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        '''
        p1 = Platform(0,HEIGHT -40, WIDTH, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(WIDTH/2 -50, HEIGHT * 3 /4 , 100, 20)
        self.all_sprites.add(p2) 
        self.platforms.add(p2)
        '''

        self.run()

    def run(self):
        #Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.update()
            self.draw()

    def update(self):
        #Game loop - update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

    def events(self):
        #Game loop - events
        for event in pg.event.get():
            #check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()


    def draw(self):
        #Game loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        #after drawing everything, filp the dispaly
        pg.display.flip( )

    def show_start_screen(self):
        #game splash / start screen
        pass

    def show_go_screen(self):
        #game over/continue
        pass


g =  Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()



