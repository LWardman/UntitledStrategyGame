import pygame


class Hexagon(object):
    def __init__(self, x, y, width, height, sprite, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite
        self.colour = colour
        self.tree = False
        self.stone = False
        self.hitboxes = False
        self.contains_building = False
        self.building = None
        self.hitbox_1 = (self.x, self.y, self.width, self.height)
        self.hitbox_2 = (0, 0, 0, 0)
        self.hitbox_3 = (0, 0, 0, 0)
        self.hitbox_4 = (0, 0, 0, 0)

    def draw(self, win, trees, stones):
        win.blit(self.sprite, (self.x, self.y))
        if self.tree:
            win.blit(trees, (self.x + 17, self.y + 17))
        elif self.stone:
            win.blit(stones, (self.x, self.y))
        if self.hitboxes:
            pygame.draw.rect(win, (0, 255, 0), self.hitbox_1, 2)
            pygame.draw.rect(win, (0, 255, 0), self.hitbox_2, 2)
            pygame.draw.rect(win, (0, 255, 0), self.hitbox_3, 2)
            pygame.draw.rect(win, (0, 255, 0), self.hitbox_4, 2)
        if self.contains_building:
            win.blit(self.building, (self.x + 17, self.y + 23))

    def get_hitbox_1(self):
        return pygame.Rect(self.hitbox_1)

    def update_hitboxes(self):
        self.hitbox_1 = pygame.Rect(self.x + 20, self.y + 14, 25, 40)
        self.hitbox_2 = pygame.Rect(self.x + 15, self.y + 20, 35, 25)
        self.hitbox_3 = pygame.Rect(self.x + 10, self.y + 26, 45, 14)
        self.hitbox_4 = pygame.Rect(self.x + 5, self.y + 30, 55, 5)
