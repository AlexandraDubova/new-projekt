import pygame
import random

from settings import *
from player import Bird
from pipe import Pipe
from button import Button

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((screen_widht, screen_height))
        pygame.display.set_caption("Flappy Bird")

        #definice fontu
        self.font = pygame.font.SysFont('Bauhaus 93', 60)

        #promenne
        self.ground_scroll = 0
        #pujde przc
        self.pipe_speed = 4
        self.flying = False
        self.game_over = False
        #pujde przc
        self.pipe_gap = 150
        self.last_pipe = pygame.time.get_ticks()
        self.score = 0
        self.pass_pipe = False
        
        #obrazky
        self.bg = pygame.image.load("img/bg.png")
        self.ground_img = pygame.image.load("img/ground.png")
        self.restart_img = pygame.image.load("img/restart.png")
        self.exit_img = pygame.image.load("img/exit.png")
        self.menu_img = pygame.image.load("img/menu.png")
        self.bg_dark = pygame.image.load("img/bg-n.png")
        self.pipe_light = pygame.image.load("img/pipe.png")
        self.pipe_dark = pygame.image.load("img/pipe-n.png")

        #zvuky

        # zvuky
        self.snd_flap = pygame.mixer.Sound("audio/letani.wav")
        self.snd_score = pygame.mixer.Sound("audio/prulet.wav")
        self.snd_hit = pygame.mixer.Sound("audio/konec.wav")

        #nastaveni hlasitosti zvuku
        self.sound_on = True

        self.volume = 0.5
        self.snd_flap.set_volume(self.volume)
        self.snd_score.set_volume(self.volume)
        self.snd_hit.set_volume(self.volume)

        self.restart_btn = Button(
            screen_widht // 2 - 60,
            screen_height // 2 - 20,
            self.restart_img
                        )

        self.menu_btn = Button(
            screen_widht // 2 - 60,
            screen_height // 2 + 40,
            self.menu_img
                        )

        self.exit_btn = Button(
            screen_widht // 2 - 60,
            screen_height // 2 + 100,
            self.exit_img
        )

        self.dark_mode = False

        #skupiny sprite 
        self.bird_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()

        self.flappy = Bird(100, int(screen_height / 2))
        self.bird_group.add(self.flappy)
        
        self.state = 'MENU'

        self.difficulty = 'MEDIUM'  # nastaveni vychozi obtížnosti

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def reset_game(self):
        self.pipe_group.empty()
        self.flappy.rect.x = 100
        self.flappy.rect.y = int(screen_height / 2)
        self.score = 0
        self.game_over = False
        self.flying = False
        return self.score
    
    def run(self):
        self.running = True
        while self.running :

            if self.state == 'MENU':
                self.menu()

            elif self.state == 'PLAYING':
                self.play_game()

            elif self.state == 'SETTINGS':
                self.settings()

            elif self.state == 'GAME_OVER':
                self.game_over_screen()
            
            pygame.display.update()
            self.clock.tick(fps)

    def play_game(self):
            #pozadi
            bg_img = self.bg_dark if self.dark_mode else self.bg
            self.screen.blit(bg_img, (0,0))
            self.screen.blit(self.ground_img, (self.ground_scroll, 768))

            self.bird_group.draw(self.screen)
            self.bird_group.update(self.flying, self.game_over)
            self.pipe_group.draw(self.screen)

            #zeme
            self.screen.blit(self.ground_img, (self.ground_scroll, 768))

            #skore
            if len(self.pipe_group) > 0:
                if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.left\
                    and self.bird_group.sprites()[0].rect.right < self.pipe_group.sprites()[0].rect.right\
                    and self.pass_pipe == False:
                        self.pass_pipe = True

                if self.pass_pipe == True:
                    if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.right:
                        self.score += 1
                        self.pass_pipe = False
                        if self.sound_on:
                            self.snd_score.play()


            self.draw_text(str(self.score), self.font, white, int(screen_widht / 2), 20)

            #kolize
            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
                if not self.game_over:
                    if self.sound_on:
                        self.snd_hit.play()
                self.game_over = True
        

            #kontrola jestli ptak nespadl na zem
            if self.flappy.rect.bottom >= 768:
                self.game_over = True
                self.flying = False

            if self.game_over == False and self.flying == True:

                #generovani novych rour
                time_now = pygame.time.get_ticks()
                if time_now - self.last_pipe > pipe_frequency:

                    pipe_height = 320
                    
                    top_limit = 120
                    bottom_limit = screen_height - 120

                    top_pipe_bottom = random.randint(top_limit + pipe_height, bottom_limit - self.pipe_gap)
                    
                    pipe_img = self.pipe_dark if self.dark_mode else self.pipe_light

                    btm_pipe = Pipe(screen_widht,  top_pipe_bottom + self.pipe_gap , -1, self.pipe_speed, self.pipe_gap, pipe_img)
                    top_pipe = Pipe(screen_widht,   top_pipe_bottom , 1, self.pipe_speed, self.pipe_gap, pipe_img)
                    self.pipe_group.add(btm_pipe)
                    self.pipe_group.add(top_pipe)
                    self.last_pipe = time_now



        
                self.ground_scroll -= self.pipe_speed
                if abs(self.ground_scroll) > 35:
                    self.ground_scroll = 0

                self.pipe_group.update()

            if self.game_over:
                self.state = 'GAME_OVER'
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if self.sound_on:
                        self.snd_flap.play()
                    
                    if not self.flying:
                        self.flying = True
                        


    def menu(self):
        bg_img = self.bg_dark if self.dark_mode else self.bg    
        self.screen.blit(bg_img, (0,0))
        self.screen.blit(self.ground_img, (self.ground_scroll, 768))
        self.draw_text('PLAY', self.font, white, int(screen_widht / 2) - 50, int(screen_height / 2) - 150)

        self.draw_text('SETTINGS', self.font, white, int(screen_widht / 2) - 100, int(screen_height / 2) - 90)   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()


                if int(screen_height / 2) - 170 < y < int(screen_height / 2) - 110:
                    self.reset_game()
                    self.state = 'PLAYING'
                    return

                elif int(screen_height / 2) - 110 < y < int(screen_height / 2) - 50:
                    self.state = 'SETTINGS'
                    return

        
    def settings(self):
        bg_img = self.bg_dark if self.dark_mode else self.bg
        self.screen.blit(bg_img, (0,0))
        self.screen.blit(self.ground_img, (self.ground_scroll, 768))

        color_options = {
            'EASY': (0, 255, 0),
            'MEDIUM': (255, 255, 0),
            'HARD': (255, 0, 0)
        }

        y_start = 250
        spacing = 80

        self.draw_text("EASY", self.font, color_options["EASY"] if self.difficulty == 'EASY' else white, screen_widht / 2 - 50, y_start)
        self.draw_text("MEDIUM", self.font, color_options["MEDIUM"] if self.difficulty == 'MEDIUM' else white, screen_widht / 2 - 100, y_start + spacing)
        self.draw_text("HARD", self.font, color_options["HARD"] if self.difficulty == 'HARD' else white, screen_widht / 2 - 60, y_start + spacing * 2) 

        self.draw_text("BACK", self.font, white, screen_widht / 2 - 60, screen_height - 250) 

        self.draw_text(f"DARK MODE: {'ON' if self.dark_mode else 'OFF'}", self.font, white, screen_widht / 2 - 200, y_start + spacing * 4 )
        
        self.draw_text(f"SOUND: {'ON' if self.sound_on else 'OFF'}", self.font, white, screen_widht / 2 - 130, y_start + spacing * 5 - 20 )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()

                if  y_start < y < y_start + 40:
                    self.difficulty = 'EASY'
                    self.apply_difficulty()
                
                elif y_start + spacing < y < y_start + spacing + 40:
                    self.difficulty = 'MEDIUM'
                    self.apply_difficulty()

                elif y_start + spacing * 2 < y < y_start + spacing * 2 + 40:
                    self.difficulty = 'HARD'
                    self.apply_difficulty() 

                elif y_start + spacing * 4 < y < y_start + spacing * 4 + 40:
                    self.dark_mode = not self.dark_mode

                elif y_start + spacing * 5 < y < y_start + spacing * 5 + 40:
                    self.sound_on = not self.sound_on
                
                elif screen_height - 260 < y < screen_height - 210:
                    self.state = 'MENU'
                    return
        

    def apply_difficulty(self):
        if self.difficulty == 'EASY':
            self.pipe_gap = 170
            self.pipe_speed = 3

        elif self.difficulty == 'MEDIUM':
            self.pipe_gap = 150
            self.pipe_speed = 4

        elif self.difficulty == 'HARD':
            self.pipe_gap = 120
            self.pipe_speed = 5

        self.pipe_group.empty()
        self.last_pipe = pygame.time.get_ticks()

    def game_over_screen(self):
        bg_img = self.bg_dark if self.dark_mode else self.bg
        self.screen.blit(bg_img, (0, 0))
        self.screen.blit(self.ground_img, (0, 768))

        self.draw_text(
            "GAME OVER",
            self.font,
            white,
            screen_widht // 2 - 140,
            140
        )
        self.draw_text(
            f"SCORE: {self.score}",
            self.font,
            white,
            screen_widht // 2 - 110,
            200
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if self.restart_btn.draw(self.screen):
                    self.reset_game()
                    self.state = 'PLAYING'
                    return

                if self.menu_btn.draw(self.screen):
                    self.state = 'MENU'
                    return

                if self.exit_btn.draw(self.screen):
                    pygame.quit()
                    raise SystemExit
                
        
        self.restart_btn.draw(self.screen)
        self.menu_btn.draw(self.screen)
        self.exit_btn.draw(self.screen)