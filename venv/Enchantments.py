import random
import Stats as S

class Enchant:

    def __init__(self, buff):
        self.buff = buff

Fiery_Weapon_Enchant = Enchant(buff=10)
Hastened_Weapon_Enchant = Enchant(buff=200)


class Enchantment:
    hastened = False
    hasten_timer = 0

    def __init__(self, name, player, weapon):
        self.name = name
        self.player = player
        self.weapon = weapon

    def determine_enchant(n):
        if n == 1:
            return "Fiery_Weapon"
        elif n == 2:
            return "Hastened_Weapon"

    def report(self, weapon):
        if weapon.enchantment.name == "Fiery_Weapon":
            print(f"ENCHANT: 50% chance on hit to make your attacks deal {Fiery_Weapon_Enchant.buff} extra fire damage for a short time. (Stacks with crits for large numbers!)\n")
        elif weapon.enchantment.name == "Hastened_Weapon":
            print(f"ENCHANT: 50% chance on hit to increase Weapon speed by {Hastened_Weapon_Enchant.buff} for a short time. (Procs more often!)\n")

    """Displays enchants for the Creation module!"""
    def show_enchants():
        print(f"\n1: Fiery_Weapon: 50% chance on hit to make your attacks deal {Fiery_Weapon_Enchant.buff} extra fire damage for a short time. (Stacks with crits for large numbers!)")
        print(f"2: Hastened_Weapon: 50% chance on hit to increase Weapon speed by {Hastened_Weapon_Enchant.buff} for a short time. (Procs more often!)")

    """Run after every attack to cast ability and manage buff / proc timers!"""
    def check_enhancement(self, target):
        self.ability(target)
        self.manage_procs()

