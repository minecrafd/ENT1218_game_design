# these are the essential modules for pygame
import pygame
from pygame.locals import *
import sys
import math
# This is the very first game I made with pygame, so let's start step by step
# pygame.init() need to be call every time the game start
pygame.init()
vec = pygame.math.Vector2  # for two-dimensional

# parameters to build a game
HEIGHT = 1080
WIDTH = 1920
GRAVITY = 10
Mass_Blackhole = 5

# colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set the FPS of the game
FPS = 60
FramePerSec = pygame.time.Clock()  # that is, the fps is 60

# set the display surface and the title
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteor Strike")
DISPLAYSURF.fill(WHITE)
# now we need to create classes inherited from pygame class


# function to calculate the acceleration
def compute_acceleration(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[float, float]:
    distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    acceleration = GRAVITY * Mass_Blackhole / distance
    dx = (p2[0] - p1[0]) / distance  # x-axis acceleration component
    dy = (p2[1] - p1[1]) / distance  # y-axis acceleration component
    acceleration_tuple = (acceleration * dx, acceleration * dy)
    return acceleration_tuple


# Blackhole Object
class Blackhole(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.image.load("./image/blackhole.png")
        self.rect = self.image.get_rect(center=position)

    def get_position(self):
        return self.position

    def draw(self, surface):
        # Draw the meteor image
        surface.blit(self.image, self.rect)


# Meteor Object
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # call the father's init
        self.original_image = pygame.image.load("./image/meteor.png")
        self.image = self.original_image
        # the collision box
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)
        # meteor's physical statements:
        self.force: float = 0.2  # initial force, ranging in (0, 5)
        self.rotation: float = 0
        self.velocity: list[float, float] = [0, 0]
        self.angle: int = 0
        self.launched: bool = False  # determine if the meteor is launched
        self.mass: int = 1

    # Update attribute
    def update(self, blackholes: Blackhole):
        pressed_keys = pygame.key.get_pressed()
        # only before launch can the rotation be changed
        if not self.launched:
            if pressed_keys[K_UP]:
                self.rotation += 0.1
            if pressed_keys[K_DOWN]:
                self.rotation -= 0.1
            if pressed_keys[K_RIGHT] and self.force < 10:
                self.force += 0.2
            if pressed_keys[K_LEFT] and self.force > 0.4:
                self.force -= 0.2
            if pressed_keys[K_SPACE]:
                self.launched = True
                self.velocity = [self.force, 0]
        # update the rotation of meteor (this need to be done every tick)
        self.angle += self.rotation
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # after launched, it should interact with the blackhole and planet
        # meanwhile, the velocity should be determined by every blackhole
        if self.launched:
            for blackhole in blackholes:
                blackhole_pos = blackhole.get_position()
                acceleration = compute_acceleration(self.rect.center, blackhole_pos)
                self.velocity[0] += acceleration[0]
                self.velocity[1] += acceleration[1]

        # This part is for self_rotation
        if self.launched:
            angle = math.atan2(self.velocity[1], self.velocity[0]) + math.pi/2
            self.velocity[0] += self.rotation / 200 * math.cos(angle)
            self.velocity[1] += self.rotation / 200 * math.sin(angle)

        # Update the position based on the velocity
        self.rect.move_ip(self.velocity)

    # draw to display
    def draw(self, surface):
        # Draw the meteor image
        surface.blit(self.image, self.rect)

        # Calculate the position of the arrow
        arrow_start = (self.rect.right + 10, self.rect.centery)
        arrow_end = (arrow_start[0] + self.force * 30, arrow_start[1])

        # Calculate the thickness of the arrow line based on the force
        arrow_thickness = int(self.force * 2)

        # Draw the arrow line
        pygame.draw.line(surface, RED, arrow_start, arrow_end, arrow_thickness)

        # Draw the arrowhead
        arrow_size = 10 + 15 * self.force
        angle = math.atan2(arrow_start[1] - arrow_end[1], arrow_start[0] - arrow_end[0])
        pygame.draw.polygon(surface, RED, ((arrow_end[0],
                                             arrow_end[1] + arrow_size * math.sin(angle + math.pi / 6)),
                                            (arrow_end[0] - arrow_size * math.cos(angle + math.pi / 6), arrow_end[1]),
                                            (arrow_end[0],
                                             arrow_end[1] + arrow_size * math.sin(angle - math.pi / 6))))



P1 = Meteor()
H1 = Blackhole((600, 600))

# Game loop
while True:
    for event in pygame.event.get():
        # When the following condition is satisfied, the program exit
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update([H1])
    DISPLAYSURF.fill(BLACK)
    P1.draw(DISPLAYSURF)

    H1.draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)

