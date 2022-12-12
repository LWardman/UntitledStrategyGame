import pygame


# Buttons have width and height of 40 pixels
class Building(object):
    def __init__(self, x, y, sprite, lightsprite, building, scale):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.scale = scale
        self.sprite = pygame.transform.scale(sprite, (int(self.width * scale), int(self.height * scale)))
        self.lightsprite = pygame.transform.scale(lightsprite, (int(self.width * scale), int(self.height * scale)))
        self.hitboxes = False
        self.hitbox = self.sprite.get_rect()
        self.hitbox.topleft = (self.x, self.y)
        self.building = building
        self.clicked = False

    def draw(self, win, player):
        pos = pygame.mouse.get_pos()
        if self.hitbox.collidepoint(pos):
            win.blit(self.lightsprite, (self.x, self.y))
        else:
            win.blit(self.sprite, (self.x, self.y))

        if self.hitboxes:
            pygame.draw.rect(win, (0, 0, 255), self.hitbox, 2)

        if self.clicked:
            self.placing_building(win, player)

    def give_building(self, sprite, hex_list, hex_num):
        hex_list[hex_num].contains_building = True
        hex_list[hex_num].building = sprite
        self.clicked = False
        # Can create a list of cases for the building given to determine its location.

    def placing_building(self, win, player):
        mx, my = pygame.mouse.get_pos()
        player.clicked = True
        player.building_not_selected = False
        win.blit(self.building, (mx, my))
