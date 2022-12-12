import pygame


class Player(object):
    def __init__(self, x, y, sprite, colour, hex_list):
        self.x = x
        self.y = y
        self.hitboxes = False
        self.width = 18
        self.height = 32
        self.sprite = sprite
        self.colour = colour
        self.current_gold = 0
        self.current_wood = 0
        self.current_stone = 0
        self.clicked = False
        self.building_not_selected = True
        self.surrounding_hex = self.surrounding_hexagons(hex_list)
        self.hitbox_1 = (self.x, self.y + 5, self.width, self.height)
        self.hitbox_2 = (self.x - 30, self.y - 10, self.width + 60, self.height + 35)
        self.hitbox_3 = (self.x - 15, self.y, self.width + 30, self.height + 15)

    def draw(self, win, hex_list, sprite_list):  # Bounds and water tiles used later
        # Draw player icon
        win.blit(self.sprite, (self.x, self.y))

        # If hitboxes should be viewable
        if self.hitboxes:
            pygame.draw.rect(win, (255, 0, 0), self.hitbox_1, 2)
            pygame.draw.rect(win, (255, 0, 0), self.hitbox_2, 2)
            pygame.draw.rect(win, (255, 0, 0), self.hitbox_3, 2)

        # Change the colour of the players tile
        for hexa in hex_list:
            if pygame.Rect.colliderect(hexa.get_hitbox_1(), self.hitbox_1):
                hexa.sprite, hexa.colour = sprite_list[2], "purple"
                hexa.update_hitboxes()

        # Show the hexagons the player can move to
        self.colour_hexagons(hex_list, sprite_list)

    def move_to_hex(self, hex_list, hex_num):
        self.x = hex_list[hex_num].x + 23
        self.y = hex_list[hex_num].y + 9
        self.update_hitboxes()
        self.surrounding_hex = self.surrounding_hexagons(hex_list)

    def surrounding_hexagons(self, hex_list):
        if self.clicked:
            # Initialize surrounding hex list
            surrounding_hex = []
            # For all hexagons on the map
            for i in range(len(hex_list)):
                # Check if tile is adjacent to the player and highlight it
                if pygame.Rect(hex_list[i].hitbox_1).colliderect(self.hitbox_2):
                    surrounding_hex.append(i)
            del surrounding_hex[3]
            return surrounding_hex

    def type_surrounding_hexagons(self, hex_list):
        return type(self.surrounding_hexagons(hex_list))

    def colour_hexagons(self, hex_list, sprite_list):
        if self.clicked:
            for i in range(len(hex_list)):
                if i in self.surrounding_hexagons(hex_list):
                    if hex_list[i].colour == "plain":
                        hex_list[i].sprite, hex_list[i].colour = sprite_list[1], "lightplain"
                    elif hex_list[i].colour == "purple":
                        hex_list[i].sprite, hex_list[i].colour = sprite_list[3], "lightpurple"
                else:
                    if hex_list[i].colour == "lightplain":
                        hex_list[i].sprite, hex_list[i].colour = sprite_list[0], "plain"
                    elif hex_list[i].colour == "lightpurple":
                        hex_list[i].sprite, hex_list[i].colour = sprite_list[2], "purple"

        else:
            for i in range(len(hex_list)):
                if hex_list[i].colour == "lightplain":
                    hex_list[i].sprite, hex_list[i].colour = sprite_list[0], "plain"
                elif hex_list[i].colour == "lightpurple":
                    hex_list[i].sprite, hex_list[i].colour = sprite_list[2], "purple"

    def update_hitboxes(self):
        self.hitbox_1 = (self.x, self.y + 5, self.width, self.height)
        self.hitbox_2 = (self.x - 30, self.y - 10, self.width + 60, self.height + 35)
        self.hitbox_3 = (self.x - 15, self.y, self.width + 30, self.height + 15)

    def show_resources(self, win, font):
        gold = font.render(str(self.current_gold), True, (255, 255, 255))
        win.blit(gold, (1040, 40))
        wood = font.render(str(self.current_wood), True, (255, 255, 255))
        win.blit(wood, (1040, 80))
        stone = font.render(str(self.current_stone), True, (255, 255, 255))
        win.blit(stone, (1040, 120))

    def update_resources(self, hex_list):
        new_gold = 0
        new_wood = 0
        new_stone = 0
        for hexa in hex_list:
            if hexa.colour == self.colour or hexa.colour == "light" + self.colour:
                if hexa.tree:
                    new_wood += 1
                elif hexa.stone:
                    new_stone += 1
                else:
                    new_gold += 1
        self.current_gold += int(new_gold / 2)
        self.current_wood += new_wood
        self.current_stone += new_stone
