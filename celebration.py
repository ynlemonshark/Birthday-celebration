import pygame
import sys
from pygame.locals import QUIT, Rect
from random import randint
from math import radians, sin, cos, sqrt,tan


def setting_import():
    settings_file = open("setting.txt", "r")
    settings = {}
    while True:
        line = settings_file.readline()
        line.replace("\n", "")
        if line:
            line = line.split(":")
            settings[line[0]] = int(line[1])
        else:
            break

    return settings


setting = setting_import()

Display_width = setting["Display_width"]
Display_height = setting["Display_height"]

Surface_width = 1200
Surface_height = 800

display_ratio_x = Display_width / Surface_width
display_ratio_y = Display_height / Surface_height

FPS = setting["FPS"]

pygame.init()
DISPLAY = pygame.display.set_mode((Display_width, Display_height))
SURFACE = pygame.Surface((Surface_width, Surface_height))
FPSCLOCK = pygame.time.Clock()

rocket_size = (60, 60)
rocket_image = pygame.transform.scale(pygame.image.load("resources/rocket.png"), rocket_size)

rocket_sequence = []
file = open("resources/rockets.txt", "r")
while True:
    line = file.readline()
    line = line.replace("\n", "")

    if not line:
        break

    line = line.split("/")
    rocket_sequence.append((int(line[0]), int(line[1])))
file.close()

letter_bricks = {}  # letter_bricks["brick"][index][x or y]
file = open("resources/letter_bricks.txt")
while True:
    line = file.readline()
    line = line.replace("\n", "")

    if not line:
        break

    line = line.split(".")

    line[1] = line[1].split(",")
    extra_positions = []
    for extra_position in line[1]:
        extra_position = extra_position.split("/")
        extra_position[0] = int(extra_position[0]) * 20
        extra_position[1] = int(extra_position[1]) * 20
        extra_positions.append(extra_position)
    letter_bricks[line[0]] = extra_positions

print(letter_bricks)
file.close()

file = open("resources/letters.txt")
bricks = []
bricks2 = []
while True:
    line = file.readline()
    line = line.replace("\n", "")

    if not line:
        break

    line = line.split(",")
    for repeat in range(len(letter_bricks[line[0]])):
        bricks2.append((int(line[1]), int(line[2])))
    bricks.extend(letter_bricks[line[0]])

three = pygame.transform.scale(pygame.image.load("resources/three.png"), (128, 128))
two = pygame.transform.scale(pygame.image.load("resources/two.png"), (128, 128))
one = pygame.transform.scale(pygame.image.load("resources/one.png"), (128, 128))

speed = 220

sounds = (pygame.mixer.Sound("resources/1.mp3"),
          pygame.mixer.Sound("resources/2.mp3"),
          pygame.mixer.Sound("resources/3.mp3"),
          pygame.mixer.Sound("resources/4.mp3"),
          pygame.mixer.Sound("resources/5.mp3"),
          pygame.mixer.Sound("resources/6.mp3"),
          pygame.mixer.Sound("resources/7.mp3"),
          pygame.mixer.Sound("resources/8.mp3"))


class Rocket:
    def __init__(self, color):
        self.position = randint(0, Surface_width)
        self.height = Surface_height
        self.speed = randint(700, 800)
        self.time = 0
        self.color = color

    def rise(self):
        self.time += 1000 / FPS
        if self.time < 800:
            self.height -= self.speed / FPS

    def delete(self):
        return self.time >= 800

    def draw(self):
        SURFACE.blit(rocket_image, (self.position - rocket_size[0] / 2, self.height))


class Fire:
    def __init__(self, position, height, color):
        self.position = (position, height)
        self.direction = randint(0, 359)
        self.force = randint(20, 300)
        self.color = color
        self.colors = (0, 0, 0)
        if self.color == 0:
            random1 = randint(0, 63)
            random2 = randint(0, 127)
            self.colors = (255 - random1, random2, random2)
        elif self.color == 1:
            random1 = randint(0, 127)
            random2 = randint(0, 127)
            self.colors = (255 - random1, 100 - random1 / 2 + random2 / 2, random2)
        elif self.color == 2:
            random1 = randint(0, 127)
            random2 = randint(0, 127)
            self.colors = (255 - random1, 255 - random1, random2)
        elif self.color == 3:
            random1 = randint(0, 127)
            random2 = randint(0, 127)
            self.colors = (random2, 255 - random1, random2)
        elif self.color == 4:
            random1 = randint(0, 63)
            random2 = randint(0, 63)
            self.colors = (random2, 255 - random1, 255 - random1)
        elif self.color == 5:
            random1 = randint(0, 63)
            random2 = randint(0, 63)
            self.colors = (random2 + 63, random2 + 63, 255 - random1)
        elif self.color == 6:
            random1 = randint(0, 63)
            random2 = randint(0, 63)
            self.colors = (255 - random1 / 2, random2, 255 - random1)
        if self.color == 7:
            random1 = randint(0, 63)
            random2 = randint(0, 127)
            self.colors = (255 - random1, random2, random2)
        self.time = 0
        self.gravity = 0
        self.life = 1000

    def disperse(self):
        self.position = (self.position[0] + cos(radians(self.direction)) * self.force / FPS,
                         self.position[1] + sin(radians(self.direction)) * self.force / FPS + self.gravity)
        self.time += 1000 / FPS
        self.gravity += 10 / FPS

    def delete(self):
        return self.time >= self.life

    def draw(self):
        image = pygame.Surface((10, 10))
        image.fill((255, 255, 255))
        image_rect = image.get_rect()
        pygame.draw.circle(image, self.colors, image_rect.center, image_rect.width / 2)
        image.set_colorkey((255, 255, 255))
        image.set_alpha(255 - 255 * self.time / self.life)
        SURFACE.blit(image, (self.position[0] - 5, self.position[1] - 5))


sind = sin(radians(330))
cosd = cos(radians(330))
tand = tan(radians(330))
grav = 600

brick_image = pygame.transform.scale(pygame.image.load("resources/brick.png"), (20, 20))


class Brick:
    def __init__(self, goal):
        self.position = [-100, 300]
        self.goal_position = goal
        goal_x = goal[0] - self.position[0]
        goal_y = goal[1] - self.position[1]

        self.speed = sqrt((grav * goal_x ** 2) / (2 * goal_y * cosd ** 2 - 2 * tand * goal_x * cosd ** 2))
        self.life = goal_x / (cosd * self.speed)

        self.time = 0
        self.before_time = self.time

        self.gravity = 0

    def move(self):
        if self.time < self.life:
            self.position[0] += self.speed * cosd / FPS
            self.position[1] += self.speed * sind / FPS

            self.before_time = self.time
            self.time += 1 / FPS

            self.position[1] += grav * self.time ** 2 / 2 - grav * self.before_time ** 2 / 2

    def draw(self):
        if self.time < self.life:
            SURFACE.blit(brick_image, self.position)
        else:
            SURFACE.blit(brick_image, self.goal_position)


brick_start_delay = 20000
brick_create_delay = 30

golden_message = pygame.transform.scale(pygame.image.load("resources/golden_letter.png"), (Surface_width, Surface_height))
golden_message_time = 500

mail_rect = pygame.Rect(400, 300, 400, 200)
mail_image = pygame.transform.scale(pygame.image.load("resources/mail.png"), mail_rect.size)
mail_upper_image = pygame.transform.scale(pygame.image.load("resources/mail_over.png"), mail_rect.size)


def main():
    Rocket_delay = -3000
    Rocket_index = 0
    Rockets = []
    Fires = []
    Bricks = []
    Brick_start_delay = 0
    Brick_create_delay = 0
    Golden_message_delay = golden_message_time
    Brick_number = 0

    Mail_sitation = 5
    mail_time = 0

    number_delay = -3800 + speed * 9
    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()
            if pygame_event.type == pygame.KEYUP:
                if Mail_sitation == 0:
                    Mail_sitation = 1
            if pygame_event.type == pygame.MOUSEBUTTONDOWN:
                if Mail_sitation == 1 and mail_rect.collidepoint((pygame_event.pos[0] / display_ratio_x,
                                                                  pygame_event.pos[1] / display_ratio_y)):
                    Mail_sitation = 2

        if Rocket_index < len(rocket_sequence):
            Rocket_delay += 1000 / FPS
            if Rocket_delay >= rocket_sequence[Rocket_index][1] * speed:
                Rocket_delay = 0
                Rockets.append(Rocket(rocket_sequence[Rocket_index][0]))
                Rocket_index += 1

        if Mail_sitation == 2:
            mail_time += 1000 / FPS


        if Brick_start_delay < brick_start_delay:
            Brick_start_delay += 1000 / FPS
        else:
            Brick_create_delay += 1000 / FPS
            while Brick_create_delay >= brick_create_delay:
                if Brick_number >= len(bricks):
                    break
                else:
                    Brick_create_delay -= brick_create_delay
                    Bricks.append(Brick((bricks[Brick_number][0] + bricks2[Brick_number][0],
                                         bricks[Brick_number][1] + bricks2[Brick_number][1])))
                    Brick_number += 1

        if Brick_number >= len(bricks) and Golden_message_delay > 0 and Bricks[-1].life <= Bricks[-1].time:
            Golden_message_delay -= 1000 / FPS
            if Golden_message_delay < 0:
                Golden_message_delay = 0

        SURFACE.fill((31, 31, 31))

        for index in range(len(Bricks)):
            Bricks[index].move()
            Bricks[index].draw()

        if Brick_number >= len(bricks) and Golden_message_delay > 0 and Bricks[-1].life <= Bricks[-1].time:
            golden_message.set_alpha(Golden_message_delay / golden_message_time * 255)
            SURFACE.blit(golden_message, (0, 0))

        for index in range(len(Rockets)):
            Rockets[index].rise()
            Rockets[index].draw()
            if Rockets[index].delete():
                for repeat in range(randint(40, 50)):
                    Fires.append(Fire(Rockets[index].position, Rockets[index].height, Rockets[index].color))
                sounds[Rockets[index].color].play()
                Rockets[index] = 0
        for repeat in range(Rockets.count(0)):
            Rockets.remove(0)

        for index in range(len(Fires)):
            Fires[index].disperse()
            Fires[index].draw()
            if Fires[index].delete():
                Fires[index] = 0

        for repeat in range(Fires.count(0)):
            Fires.remove(0)
        if number_delay <= speed * 9:
            number_delay += 1000 / FPS
            if speed * 9 >= number_delay > speed * 6:
                SURFACE.blit(one, (536, 336))
            if speed * 6 >= number_delay > speed * 3:
                SURFACE.blit(two, (536, 336))
            if speed * 3 >= number_delay > 0:
                SURFACE.blit(three, (536, 336))

        if Mail_sitation == 1 or Mail_sitation == 2:
            SURFACE.blit(mail_image, mail_rect.topleft)
            if mail_time <= 500:
                mail_upper = pygame.transform.scale(mail_upper_image,
                                                    (mail_rect.width, (1 - (mail_time / 500)) * mail_rect.height))
                mail_upper_rect = mail_upper.get_rect()
                mail_upper_rect.topleft = mail_rect.topleft
            elif 1000 >= mail_time > 500:
                mail_upper = pygame.transform.scale(mail_upper_image,
                                                    (mail_rect.width, (mail_time - 500) / 500 * mail_rect.height))
                mail_upper = pygame.transform.rotate(mail_upper, 180)
                mail_upper_rect = mail_upper.get_rect()
                mail_upper_rect.bottomleft = mail_rect.topleft
            SURFACE.blit(mail_upper, mail_upper_rect.topleft)

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()