import Stats as S
import Parts
import Enchantments as E
import pygame
import random
import Images
pygame.init()

interface_stats = pygame.font.SysFont('Comic Sans MS', 15)

"""Created Weapons crafted by players to gain certain stats
Weapons have a base however the parts only augment them."""
class Weapons(S.Stats):
    Enchanted = False

    p1 = p2 = p3 = None


    on_fire = False
    hastened = False

    def __init__(self, name, equip_keybind, image=None, damage=0, speed=0, crit=0):
        S.Stats.__init__(self, image, damage, speed, crit)
        self.name = name
        self.equip_keybind = equip_keybind

    """Gives quick text return to display icon box in INTERFACES!"""
    def get_enchantment_quick_text(self):
        if self.enchantment.name == "Fiery_Weapon":
            return f"Chance (+{E.Fiery_Weapon_Enchant.buff} Damage)"
        elif self.enchantment.name == "Hastened_Weapon":
            return f"Chance (+{E.Hastened_Weapon_Enchant.buff} Speed)"

    """Checks if the enchantment Proced or not"""
    def get_enchantment(self):
        rng = random.randint(1, 100)
        if self.enchantment.name == "Fiery_Weapon":
            if rng <= 50: #20
                self.on_fire = True

        elif self.enchantment.name == 'Hastened_Weapon':
            if rng <= 50: #25
                self.hastened = True

    def get_total_damage(self):
        total_damage = self.damage + self.p1.damage + self.p2.damage + self.p3.damage
        return total_damage

    def get_total_speed(self):
        total_speed = self.speed + self.p1.speed + self.p2.speed + self.p3.speed
        return total_speed

    def get_total_crit(self):
        total_crit = self.crit + self.p1.crit + self.p2.crit + self.p3.crit
        return total_crit

    """Checks to see if the damage is critical and if so damage dealt = damage * 1.5
    also checks for fiery weapon"""
    def check_crit_and_fiery_weapon(self):
        rng = random.randint(1, 100)
        if self.on_fire:
            total_deliverance = self.get_total_damage() + 10
        else:
            total_deliverance = self.get_total_damage()

        if rng <= self.get_total_crit():
            return round(total_deliverance * 1.5), True


        else:
            return total_deliverance, False


    def report_final_stats(self, to_interface=False):
        total_damage = self.damage + self.p1.damage + self.p2.damage + self.p3.damage
        total_speed = self.speed + self.p1.speed + self.p2.speed + self.p3.speed
        total_crit = self.crit + self.p1.crit + self.p2.crit + self.p3.crit

        if self.on_fire:
            stats_string = f"Total stats:   (Damage:{total_damage + E.Fiery_Weapon_Enchant.buff})   (Speed: {total_speed})   (Crit: {total_crit})"
        elif self.hastened:
            stats_string = f"Total stats:   (Damage:{total_damage})   (Speed: {total_speed + E.Hastened_Weapon_Enchant.buff})   (Crit: {total_crit})"
        else:
            stats_string = f"Total stats:   (Damage:{total_damage})   (Speed: {total_speed})   (Crit: {total_crit})"

        #Determine if to UI or to Console
        if to_interface:
            stats_text = interface_stats.render(stats_string, True, (0, 255, 0))
            return stats_text
        else:
            print(stats_string)
            self.enchantment.report(self)

    def equip(self, part):
        if part.placement == "blades":
            self.p1 = part
        elif part.placement == "nozzels":
            self.p2 = part
        elif part.placement == "triggers":
            self.p3 = part

        print(f"{part.parts_name} has been added to your weapon!")


    def swing(self, target):
        target.health -= self.damage

    def show_info(self):
        print(f"{self.name}: Press {self.equip_keybind} to equip!\n"
              + self.indent() + f"Damage: {self.damage}\n" + self.indent() + f"Speed: {self.speed}\n"
              + self.indent() + f"Crit: {self.crit}\n")


#Premade Weapons
Waraxe = Weapons(image = Images.waraxe_img, name = "Waraxe", equip_keybind=1, damage=8, speed=100, crit=5)
Sword = Weapons(image = Images.sword_img, name = "Sword", equip_keybind=2, damage=5, speed=150, crit=5)
Mace = Weapons(image = Images.mace_img, name = "Mace", equip_keybind=3, damage=10, speed=50, crit=10)
Dagger = Weapons(image = Images.dagger_img, name = "Dagger", equip_keybind=4, damage=2, speed=250, crit=30)



