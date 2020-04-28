import pygame
import os
'''Creates directory and uses directory to find and transforms the image found  to a given size'''
def getPath(directory, imgFile, resizeX, resizeY):
    path = pygame.image.load(os.path.join(directory, imgFile))
    path = pygame.transform.scale(path,(resizeX, resizeY))
    return path

'''Creates and animation List given the unit and action of said unit while putting resize into the getPath function'''
def createUnitAnimation(actionFolder, unitFolder, num_of_images, xSize, ySize):
    animationList = []
    for imageNumber in range(num_of_images):
        animationList.append(getPath(unitFolder + '/' + actionFolder, str(imageNumber) + '.png', xSize, ySize))
    return animationList



def load(image, directory, width = 125, height = 175):

    imageName = image + '.png'

    if directory != None:
        image = pygame.image.load(directory + imageName)
        image = pygame.transform.scale(image, (width, height))
    else:
        image = pygame.image.load(imageName)
    return image

#backgrounds
black_background = load("black_background", "Images/Backgrounds/", 1400, 800)


#interface
icon_display_background = load("icon_display_background", "Images/Interface/", 150, 75)
icon_display_background_large = load("icon_display_background", "Images/Interface/", 150, 100)
restart_button = load("restart_button", "Images/Interface/", 140, 100)

#weapons
waraxe_img = load("waraxe_icon", "Images/Weapons/", 90, 90)
sword_img = load("sword_icon", "Images/Weapons/", 90, 90)
mace_img = load("mace_icon", "Images/Weapons/", 90, 90)
dagger_img = load("dagger_icon", "Images/Weapons/", 90, 90)

#parts
chainblade_img = load("chainblade", "Images/Parts/", 40, 40)
bayonet_img = load("bayonet", "Images/Parts/", 40, 40)
zapper_img = load("zapper", "Images/Parts/", 40, 40)

cannon_img = load("cannon", "Images/Parts/", 40, 40)
repeater_img = load("repeater", "Images/Parts/", 40, 40)
flamethrower_img = load("flamethrower", "Images/Parts/", 40, 40)

big_billy_img = load("bigbilly", "Images/Parts/", 40, 40)
standard_img = load("standard", "Images/Parts/", 40, 40)
deceptive_img = load("deceptive", "Images/Parts/", 40, 40)


#axe hero
axe_idle_left = createUnitAnimation("idleLeft", "Images/Heroes/axe_skele", 12, xSize=190, ySize=200)
axe_idle_right = createUnitAnimation("idleRight", "Images/Heroes/axe_skele", 12, xSize=190, ySize=200)
axe_attack_left = createUnitAnimation("attackLeft", "Images/Heroes/axe_skele", 12, xSize=190, ySize=200)
axe_attack_right = createUnitAnimation("attackRight", "Images/Heroes/axe_skele", 12, xSize=190, ySize=200)

#sword hero
sword_idle_left = createUnitAnimation("idleLeft", "Images/Heroes/sword_skele", 20, xSize=190, ySize=200)
sword_idle_right = createUnitAnimation("idleRight", "Images/Heroes/sword_skele", 20, xSize=190, ySize=200)
sword_attack_left = createUnitAnimation("attackLeft", "Images/Heroes/sword_skele", 10, xSize=190, ySize=200)
sword_attack_right = createUnitAnimation("attackRight", "Images/Heroes/sword_skele", 10, xSize=190, ySize=200)

#Mace hero
mace_idle_left = createUnitAnimation("idleLeft", "Images/Heroes/mace_skele", 20, xSize=190, ySize=200)
mace_idle_right = createUnitAnimation("idleRight", "Images/Heroes/mace_skele", 20, xSize=190, ySize=200)
mace_attack_left = createUnitAnimation("attackLeft", "Images/Heroes/mace_skele", 10, xSize=190, ySize=200)
mace_attack_right = createUnitAnimation("attackRight", "Images/Heroes/mace_skele", 10, xSize=190, ySize=200)

#Dagger hero
dagger_idle_left = createUnitAnimation("idleLeft", "Images/Heroes/dagger_skele", 20, xSize=190, ySize=200)
dagger_idle_right = createUnitAnimation("idleRight", "Images/Heroes/dagger_skele", 20, xSize=190, ySize=200)
dagger_attack_left = createUnitAnimation("attackLeft", "Images/Heroes/dagger_skele", 10, xSize=190, ySize=200)
dagger_attack_right = createUnitAnimation("attackRight", "Images/Heroes/dagger_skele", 10, xSize=190, ySize=200)

#enchantments
fireball = createUnitAnimation("fiery_weapon", "Images/enchantments", 31, xSize=60, ySize=60)
haste = createUnitAnimation("hastened", "Images/enchantments", 20, xSize=60, ySize=60)

#Add other images here when attacking is completed ?????????????????????????????????
p1_weapons = {"Waraxe": [axe_idle_right, axe_attack_right], "Sword": [sword_idle_right, sword_attack_right], "Mace": [mace_idle_right, mace_attack_right], "Dagger": [dagger_idle_right, dagger_attack_right]}
p2_weapons = {"Waraxe": [axe_idle_left, axe_attack_left], "Sword": [sword_idle_left, sword_attack_left], "Mace": [mace_idle_left, mace_attack_left], "Dagger": [dagger_idle_left, dagger_attack_left]}

def get_player_image(player, player_num):
    if player_num == 1:
        weapons_list = p1_weapons
    elif player_num == 2:
        weapons_list = p2_weapons

    idle_list = weapons_list[player.weapon.name][0]
    attack_list = weapons_list[player.weapon.name][1]

    return idle_list, attack_list
