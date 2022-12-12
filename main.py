import sys
import pygame
import player
import hex
import building

# Initialise pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((1200, 800))

# Title
pygame.display.set_caption("Untitled Strategy")

# Writing font
font = pygame.font.Font("freesansbold.ttf", 32)

# Hexagon sprites
plainHex = pygame.image.load("Assets\\plainTile.png").convert_alpha()
lightplainHex = pygame.image.load("Assets\\lightplainTile.png").convert_alpha()
purpleHex = pygame.image.load("Assets\\purpleHexagon.png").convert_alpha()
lightpurpleHex = pygame.image.load("Assets\\lightpurpleHexagon.png").convert_alpha()
sprite_list = [plainHex, lightplainHex, purpleHex, lightpurpleHex]

# Creating the hex map
hex_list = []
for _ in range(414):
    hex_list.append(hex.Hexagon(00, 00, 60, 38, plainHex, "plain"))

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
    i.update_hitboxes()

# Creating boundary tiles
brownHex = pygame.image.load("Assets\\brownHexagon.png").convert_alpha()
# Left edge
bounds = [i for i in range(17)]
# Top and bottom edges
bounds += [j for j in range(1, 414) if (j % 18 == 17 or j % 18 == 0)]
# Right edge
bounds += [k for k in range(397, 414)]
# Make all boundary hexagons brown
for hex_num in bounds:
    hex_list[hex_num] = hex.Hexagon(hex_list[hex_num].x, hex_list[hex_num].y, 60, 38, brownHex, "brown")
    hex_list[hex_num].update_hitboxes()

# Creating water tiles
waterHex = pygame.image.load("Assets\\waterHexagon.png").convert_alpha()
waterTiles = [47, 48, 49, 55, 56, 69, 140, 185, 204, 307, 308, 390]
for hex_num in waterTiles:
    hex_list[hex_num] = hex.Hexagon(hex_list[hex_num].x, hex_list[hex_num].y, 60, 38, waterHex, "water")
    hex_list[hex_num].update_hitboxes()

# Player Sprite
purpleChar = pygame.image.load("Assets\\PurplePlayer.png").convert_alpha()

# Initialise the player
player = player.Player(392, 389, purpleChar, "purple", hex_list)
player.move_to_hex(hex_list, 190)

# UI icons
goldIcon = pygame.image.load("Assets\\goldCoin.png").convert_alpha()
woodIcon = pygame.image.load("Assets\\woodResource.png").convert_alpha()
stoneIcon = pygame.image.load("Assets\\stoneResource.png").convert_alpha()

# Trees
trees = pygame.image.load("Assets\\trees.png").convert_alpha()
treeLocations = [57, 58, 59, 60, 73, 74, 75, 76]
for i in treeLocations:
    hex_list[i].tree = True

# Stone
stones = pygame.image.load("Assets\\stones.png").convert_alpha()
stoneLocations = [332, 333, 334, 335, 361, 362, 363]
for i in stoneLocations:
    hex_list[i].stone = True

# Loading building buttons
fort1ButtonImg = pygame.image.load("Assets\\fortLvl1Button.png").convert_alpha()
lightfort1ButtonImg = pygame.image.load("Assets\\lightfort1button.png").convert_alpha()

fort2ButtonImg = pygame.image.load("Assets\\fortLvl2Button.png").convert_alpha()
lightfort2ButtonImg = pygame.image.load("Assets\\lightfort2button.png").convert_alpha()

fort3ButtonImg = pygame.image.load("Assets\\fortLvl3Button.png").convert_alpha()
lightfort3ButtonImg = pygame.image.load("Assets\\lightfort3button.png").convert_alpha()

# Loading buildings
fort1 = pygame.image.load("Assets\\fortLvl1.png").convert_alpha()
fort2 = pygame.image.load("Assets\\fortLvl2.png").convert_alpha()
fort3 = pygame.image.load("Assets\\fortLvl3.png").convert_alpha()

# Initialise building buttons
fort1Button = building.Building(980, 200, fort1ButtonImg, lightfort1ButtonImg, fort1, 1.5)
fort2Button = building.Building(1050, 200, fort2ButtonImg, lightfort2ButtonImg, fort2, 1.5)
fort3Button = building.Building(1120, 200, fort3ButtonImg, lightfort3ButtonImg, fort3, 1.5)

# Update button list if buttons are added
button_list = [fort1Button, fort2Button, fort3Button]


def redraw_game_window():
    for hexa in hex_list:
        hexa.draw(screen, trees, stones)
    player.draw(screen, hex_list, sprite_list)
    screen.blit(goldIcon, (1000, 40))
    screen.blit(woodIcon, (1000, 80))
    screen.blit(stoneIcon, (1000, 120))
    fort1Button.draw(screen, player)
    fort2Button.draw(screen, player)
    fort3Button.draw(screen, player)
    player.show_resources(screen, font)
    pygame.display.update()
    #print(clock.get_fps())
    clock.tick(60)


player.update_resources(hex_list)

clock = pygame.time.Clock()

# Game loop
while True:
    # Reset background
    screen.fill((0, 0, 0))
    print(player.type_surrounding_hexagons(hex_list))

    # Event management
    ev = pygame.event.get()
    for event in ev:

        mousePos = pygame.mouse.get_pos()

        # Check button collisions
        for button in button_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if pygame.Rect(button.hitbox).collidepoint(mousePos) and not button.clicked:
                    button.clicked = True
                    print("Building clicked")
                elif pygame.Rect(button.hitbox).collidepoint(mousePos) and button.clicked:
                    button.clicked = False
                    print("Building deselected")
                    player.building_not_selected = True

        # Selecting the player
        if pygame.Rect(player.hitbox_3).collidepoint(mousePos) and not player.clicked:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    player.clicked = True
                elif event.button == 3:
                    if pygame.Rect(player.hitbox_3).collidepoint(mousePos):
                        print("right click")

        # Moving the player to surrounding hexagons
        elif player.clicked:
            for i in player.surrounding_hexagons(hex_list):
                if hex_list[i].hitbox_1.collidepoint(mousePos) or hex_list[i].hitbox_2.collidepoint(mousePos) or hex_list[i].hitbox_3.collidepoint(mousePos) or hex_list[i].hitbox_4.collidepoint(mousePos):
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if i in bounds + waterTiles:
                            continue
                        else:
                            if player.building_not_selected:
                                player.move_to_hex(hex_list, i)
                                player.update_hitboxes()
                                player.update_resources(hex_list)
                                player.clicked = False
                            else:
                                for button in button_list:
                                    if button.clicked and (hex_list[i].colour == "lightpurple"):
                                        button.give_building(button.building, hex_list, i)
                                        player.building_not_selected = True

            # Deselecting the player
            if not pygame.Rect(player.hitbox_3).collidepoint(mousePos) and player.clicked:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        player.clicked = False
                        print("Player deselected")

            # Deselecting building
            if not pygame.Rect(player.hitbox_3).collidepoint(mousePos) and player.clicked:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        player.clicked = False
                        print("Player deselected")

        # Allow exit
        if event.type == pygame.QUIT:
            sys.exit()

    redraw_game_window()
