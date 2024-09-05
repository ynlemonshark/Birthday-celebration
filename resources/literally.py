import pygame
import sys
from pygame.locals import QUIT, Rect


Display_width = 500
Display_height = 500

Surface_width = 500
Surface_height = 500

display_ratio_x = Display_width / Surface_width
display_ratio_y = Display_height / Surface_height

FPS = 40

pygame.init()
DISPLAY = pygame.display.set_mode((Display_width, Display_height))
SURFACE = pygame.Surface((Surface_width, Surface_height))
FPSCLOCK = pygame.time.Clock()

alphabets = ("H", "A", "P", "Y", "B", "I", "R", "T", "D")


def main():
    repeat = 0
    letter = ""
    positions = []
    while True:
        pygame_events = pygame.event.get()
        for pygame_event in pygame_events:
            if pygame_event.type == QUIT:
                pygame.quit()
                sys.exit()
            if pygame_event.type == pygame.MOUSEBUTTONDOWN:
                positions.append((int(pygame_event.pos[0] // 100), int(pygame_event.pos[1] // 100)))
                letter += str(int(pygame_event.pos[0] // 100)) + "/" + str(int(pygame_event.pos[1] // 100)) + ","
            if pygame_event.type == pygame.KEYDOWN:
                print(alphabets[repeat] + "." + letter)
                if pygame_event.key == pygame.K_SPACE:
                    repeat += 1
                letter = ""
                positions = []

        SURFACE.fill((255, 255, 255))
        for index in range(len(positions)):
            pygame.draw.rect(SURFACE, (0, 0, 0), (positions[index][0] * 100, positions[index][1] * 100,
                                                  100, 100))

        DISPLAY.blit(pygame.transform.scale(SURFACE, (Display_width, Display_height)), (0, 0))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()