import sys

import pygame

# USED CODE FROM
# https://www.reddit.com/r/pygame/comments/k1ktbq/a_better_way_to_generate_a_hexgrid/

# Initialise pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((1000, 800))

# Title
pygame.display.set_caption("Untitled Strategy")

# Player Sprite
purpleChar = pygame.image.load("Assets\\PurplePlayer.png").convert_alpha()

hitboxes = False


# Player class
class Player(object):
    def __init__(self, x, y, width, height, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite
        self.hitbox = (self.x + 6, self.y + 17, self.width, self.height)

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
        if hitboxes:
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def get_hitbox(self):
        return pygame.Rect(self.hitbox)

    def update_hitbox(self):
        self.hitbox = (self.x + 6, self.y + 17, self.width, self.height)


player = Player(392, 389, 20, 20, purpleChar)

# Hexagon sprite
singleHex = pygame.image.load("Assets\\singleTile.png").convert_alpha()
purpleHex = pygame.image.load("Assets\\purpleHexagon.png").convert_alpha()


# Hexagon class
class Hexagon(object):
    def __init__(self, x, y, width, height, sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        win.blit(self.sprite, (self.x, self.y))
        if hitboxes:
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def get_hitbox(self):
        return pygame.Rect(self.hitbox)


hex_list = []
for _ in range(414):
    hex_list.append(Hexagon(00, 00, 60, 38, singleHex))

hex_column = 0
hex_row = 0
for i in hex_list:

    # Columns 0, 2, 4, 6...
    # Removed or hex_column == 0
    if not hex_column % 2:
        i.x = hex_column * 41
        i.y = hex_row * 40

    # Columns 1, 3, 5, 7...
    if hex_column % 2:
        i.x = hex_column * 41
        i.y = (hex_row * 40) + 20

    # Increment row each time
    hex_row += 1

    # Number of rows in hexMap
    if hex_row >= 18:
        hex_column += 1
        hex_row = 0

for i in hex_list:
    i.hitbox = (i.x + 17, i.y + 17, 30, 30)


def redraw_game_window():
    for j in hex_list:
        j.draw(screen)
    player.draw(screen)
    pygame.display.update()


# Game loop
while True:
    # Background Image
    screen.fill((0, 0, 0))

    # Event management
    for event in pygame.event.get():

        # Allow exit
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Testing movement
            if event.key == pygame.K_SPACE:
                player.x += (2 * hex_list[1].width / 3) + 1
                player.y += (hex_list[1].height / 2) + 1
                player.update_hitbox()

    # Checking collisions
    for i in range(len(hex_list)):
        if pygame.Rect.colliderect(hex_list[i].get_hitbox(), player.get_hitbox()):
            hex_list[i] = Hexagon(hex_list[i].x, hex_list[i].y, hex_list[i].width, hex_list[i].height, purpleHex)

    redraw_game_window()
