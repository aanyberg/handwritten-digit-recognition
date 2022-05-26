import pygame
from pygame.locals import *
from application.process_image import get_output_image

WIDTH = 480
HEIGHT = 320

BOUNDRY = 5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RADIUS = 5
LAST_POSITION = (0, 0)

pygame.init()

DISPLAYSURFACE = pygame.display.set_mode((WIDTH * 2, HEIGHT))
DISPLAYSURFACE.fill(WHITE)
pygame.display.set_caption('Digit Drawing Board')

writing = False


def round_lines(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)


def crop(original):
    cropped_image = pygame.Surface((WIDTH - BOUNDRY, HEIGHT - BOUNDRY))
    cropped_image.blit(original, (0, 0), (0, 0, WIDTH - BOUNDRY, HEIGHT - BOUNDRY))
    return cropped_image


def show_output_image(img):
    surf = pygame.pixelcopy.make_surface(img)
    surf = pygame.transform.rotate(surf, -270)
    surf = pygame.transform.flip(surf, False, True)
    DISPLAYSURFACE.blit(surf, (WIDTH + 2, 0))


# Paint a divider line for input and output image
def divider_line():
    pygame.draw.line(DISPLAYSURFACE, RED, [WIDTH, 0], [WIDTH, HEIGHT], 5)


try:
    while True:
        # Get all PyGame events
        event = pygame.event.wait()
        divider_line()

        if event.type == pygame.QUIT:
            raise StopIteration

        if event.type == pygame.MOUSEBUTTONDOWN and event.button != 3:
            pygame.draw.circle(DISPLAYSURFACE, BLACK, event.pos, RADIUS)
            writing = True

        if event.type == pygame.MOUSEBUTTONUP and event.button != 3:
            writing = False
            fname = "out.png"

            img = crop(DISPLAYSURFACE)
            pygame.image.save(img, fname)

            output_img = get_output_image(fname)
            show_output_image(output_img)

        if event.type == pygame.MOUSEMOTION:
            if writing:
                pygame.draw.circle(DISPLAYSURFACE, BLACK, event.pos, RADIUS)
                round_lines(DISPLAYSURFACE, BLACK, event.pos, LAST_POSITION, RADIUS)
            LAST_POSITION = event.pos

        # Clear screen of drawings and images
        if event.type == KEYDOWN:
            if event.unicode == 'n':
                DISPLAYSURFACE.fill(WHITE)

        pygame.display.flip()
except StopIteration:
    pass
