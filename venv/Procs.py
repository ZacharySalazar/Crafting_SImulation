import pygame
import Stats as S
import Players as P
import Enchantments as E
pygame.init()

combatTextBold = pygame.font.SysFont('segoeuisemibold', 18)


def dependency(n, p1_utility, p2_utility):
    if n == 1:
        return p1_utility
    elif n == 2:
        return p1_utility

class Proc:

    def __init__(self, player, enchant, window):
        self.player = player
        self.player_number = player.player_number
        self.enchant = enchant
        self.window = window

        if self.player_number == 1:
            self.imgX, self.imgY = 75, 300
            self.info_stringX, self.info_stringY = 175, 325
            self.rectX, self.rectY = 180, 360


        elif self.player_number == 2:
            self.imgX, self.imgY = 875, 300
            self.info_stringX, self.info_stringY = 975, 325
            self.rectX, self.rectY = 980, 360

        #Declares weapon_enchant for enchant_cond to check against for updated booleans
        if self.enchant == "Fiery_Weapon":
            self.info_string = f"Weapon Damage increased by {E.Fiery_Weapon_Enchant.buff}!"
            self.img_object = dependency(self.player_number, S.p1_fireball, S.p2_fireball)

        elif self.enchant == "Hastened_Weapon":
            self.info_string = f"Weapon speed increased by {E.Hastened_Weapon_Enchant.buff}!"
            self.img_object = dependency(self.player_number, S.p1_haste, S.p2_haste)

        self.final_info_string = combatTextBold.render(self.info_string, True, (255, 0, 0))

    def update_enchant_cond(self):
        if self.enchant == "Fiery_Weapon":
            self.enchant_cond = self.player.weapon.on_fire
        elif self.enchant == "Hastened_Weapon":
            self.enchant_cond = self.player.weapon.hastened

    def draw_template(self):
        self.update_enchant_cond()

        if self.enchant_cond:
            self.window.blit(self.img_object.img, (self.imgX, self.imgY))
            self.img_object.animate_me()
            self.window.blit(self.final_info_string, (self.info_stringX, self.info_stringY))
            pygame.draw.rect(self.window, ((0, 0, 255)),
                             (self.rectX, self.rectY, round(self.player.enchant_timer / 3), 7))
