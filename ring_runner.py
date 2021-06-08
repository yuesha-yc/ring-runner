"""
Author: Yichen (Kevin) Wang
Date: May 27, 2021
Program name: Ring Runner
"""

import pygame.math
import pygame
import os
import threading
import random

# Game Initiation
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Ring Runner')

Ico = pygame.image.load('assets/Player/LaserOn/PlayerRunLaserOn1.png')
pygame.display.set_icon(Ico)

PLAYER_LASER_ON_PATH = "assets/Player/LaserOn"
PLAYER_LASER_OFF_PATH = "assets/Player/LaserOff"

RUNNING = [pygame.image.load(os.path.join(PLAYER_LASER_ON_PATH, 'PlayerRunLaserOn1.png')),
           pygame.image.load(os.path.join(PLAYER_LASER_ON_PATH, 'PlayerRunLaserOn2.png'))]
JUMPING = pygame.image.load(os.path.join(PLAYER_LASER_ON_PATH, 'PlayerJumpLaserOn.png'))
DUCKING = [pygame.image.load(os.path.join(PLAYER_LASER_ON_PATH, 'PlayerDuckLaserOn1.png')),
           pygame.image.load(os.path.join(PLAYER_LASER_ON_PATH, 'PlayerDuckLaserOn2.png'))]

SMALL_ROBOT = [pygame.image.load(os.path.join('assets/Robot',
                                               'Robot1.png')),
               pygame.image.load(os.path.join('assets/Robot',
                                               'Robot1.png')),
               pygame.image.load(os.path.join('assets/Robot',
                                               'Robot1.png'))]
LARGE_ROBOT = [pygame.image.load(os.path.join('assets/Robot',
                                               'Robot2.png')),
               pygame.image.load(os.path.join('assets/Robot',
                                               'Robot2.png')),
               pygame.image.load(os.path.join('assets/Robot',
                                               'Robot2.png'))]

DRONE = [pygame.image.load(os.path.join('assets/Drone', 'Drone1.png')),
         pygame.image.load(os.path.join('assets/Drone', 'Drone2.png'))]

STAR = pygame.image.load(os.path.join('assets/Other', 'Star.png'))

BULLET = pygame.image.load(os.path.join('assets/Other', 'Bullet.png'))

BG = pygame.image.load(os.path.join('assets/Other', 'NewTrack.png'))

class Bullet:
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.image = BULLET
        self.width = self.image.get_width()
        self.flying = False

    def update(self):
        self.x += 10

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Player:

    X_POS = 80
    Y_POS = 330
    Y_POS_DUCK = 365
    JUMP_VEL = 7.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.bullet_count = 5
        self.bullet = Bullet(self.dino_rect.x + 100, self.dino_rect.y)

        self.gravity_multiplier = 0.8

    def update(self, userInput):

        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_RIGHT] and self.bullet_count > 0:
            self.shoot()
        if userInput[pygame.K_UP] or userInput[pygame.K_SPACE] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= self.gravity_multiplier
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def shoot(self):
        self.bullet_count -= 1
        self.bullet.flying = True
        # Re-create a bullet
        self.bullet = Bullet(self.dino_rect.x + 100, self.dino_rect.y)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Star:

    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = STAR
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:

    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallRobot(Obstacle):

    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeRobot(Obstacle):

    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Drone(Obstacle):

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, highscore
    run = True
    clock = pygame.time.Clock()
    player = Player()
    star = Star()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 350
    points = 0
    font = pygame.font.Font('assets/minecraft_font.ttf', 20)
    big_font = pygame.font.Font('assets/minecraft_font.ttf', 60)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        if points % 1000 == 0:
            player.gravity_multiplier -= 0.1
        if points >= 1000 and points % 1000 <= 100 and points % 20 < 10:
            warn_text = big_font.render("WARNING! GRAVITY DECREASE!", True, (205, 13, 22))
            warn_rect = warn_text.get_rect()
            warn_rect.center = (550, 200)
            SCREEN.blit(warn_text, warn_rect)
        if points == 5000:
            menu(-1)

        text = font.render('Points: ' + str(points), True, (0, 0, 0))
        gravity_text = font.render("Current Gravity: " + str(player.gravity_multiplier / 0.8 * 9.8) + "m/s^2", True, (0, 0, 0))
        textRect = text.get_rect()
        gravity_text_rect = gravity_text.get_rect()
        textRect.center = (1000, 40)
        gravity_text_rect.center = (900, 100)
        SCREEN.blit(text, textRect)
        SCREEN.blit(gravity_text, gravity_text_rect)

        highscore_text = font.render('Highscore: ' + str(highscore), True, (0, 0, 0))
        highscore_rect = highscore_text.get_rect()
        highscore_rect.center = (980, 70)
        SCREEN.blit(highscore_text, highscore_rect)

    def bullet_count():
        text = font.render('Bullet Count: ' + str(player.bullet_count), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.x = 40
        textRect.y = 40
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        background()

        star.draw(SCREEN)
        star.update()

        player.draw(SCREEN)
        player.bullet.draw(SCREEN)
        player.bullet.update()
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallRobot(SMALL_ROBOT))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeRobot(LARGE_ROBOT))
            elif random.randint(0, 2) == 2:
                obstacles.append(Drone(DRONE))

        for obstacle in obstacles:
            # TODO: Fix the bullet not able to collide with obstacle
            if player.bullet.image.get_rect().colliderect(obstacle.rect):
                print("COLLIDE")
                obstacles.remove(obstacle)
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)

        score()
        bullet_count()

        # Recharge one bullet per around 1 second
        if player.bullet_count < 5 and pygame.time.get_ticks() % 1000 < 50:
            player.bullet_count += 1

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points, highscore
    highscore = 0
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('assets/minecraft_font.ttf', 30)
        big_font = pygame.font.Font('assets/minecraft_font.ttf', 50)

        if death_count == -1:
            text = font.render('Press any Key to Restart', True, (0, 0, 0))
            warn_text = big_font.render("CONGRATULATIONS! YOU ESCAPED!", True, (14, 105, 173))
            warn_rect = warn_text.get_rect()
            warn_rect.center = (550, 300)
            SCREEN.blit(warn_text, warn_rect)

        elif death_count == 0:
            text = font.render('PRESS ANY KEY TO START', True, (0, 0,0))
            text2 = font.render('You are an astronaut on a space station', True, (0, 0, 0))
            text3 = font.render('Your plan to escape but you have to shut down', True, (0, 0, 0))
            text4 = font.render('The evil AI who hacked this space station', True, (0, 0, 0))

            text2Rect = text2.get_rect()
            text3Rect = text3.get_rect()
            text4Rect = text4.get_rect()
            text2Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
            text3Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 0)
            text4Rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)

            SCREEN.blit(text2, text2Rect)
            SCREEN.blit(text3, text3Rect)
            SCREEN.blit(text4, text4Rect)

        elif death_count > 0:
            text = font.render('Press any Key to Restart', True, (0, 0, 0))
            score = font.render('Your Score: ' + str(points), True, (0, 0, 0))
            highscore = points
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            text_death = font.render('You got caught by an AI sentinel', True, (0, 0, 0))
            text_death_rect = text_death.get_rect()
            text_death_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text_death, text_death_rect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT
                                 // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                main()


t1 = threading.Thread(target=menu(death_count=0), daemon=True)
t1.start()
