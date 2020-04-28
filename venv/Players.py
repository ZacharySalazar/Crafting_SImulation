import Weapons as W
import Parts
import pygame
import Stats as S
import Enchantments as E
import Images
pygame.init()

interface_stats = pygame.font.SysFont('Comic Sans MS', 15)
critical_text = pygame.font.SysFont('algerian', 16)
player_name_text = pygame.font.SysFont('Comic Sans MS', 30)
combat_text_list = []

class Player(S.Frame):

    name = False
    winner = False
    max_health = 200
    health = 750

    weapon = W.Waraxe

    attack_on_cd = True #
    attack_speed = 600 # number to be reached before attack is used. (lower speed = faster attack)
    attack_timer = 0 # counter to reach attack_speed
    enchant_timer = 700 # timer for the fiery weapon enchant
    haste_timer = 0 # timer for the haste weapon enchant

    def __init__(self, player_number, iteration_list, img):
        S.Frame.__init__(self, iteration_list, img)
        self.player_number = player_number


    def reset_me(self):
        self.attack_timer = 0
        self.enchant_timer = 700
        self.haste_timer = 0
        self.weapon.enchant = None

    """Animates the player character by setting their img equal to an increasing iteration!"""
    def animate_me(self):
        if self.current_iteration >= len(self.iteration_list):
            self.current_iteration = 0

        self.img = self.iteration_list[self.current_iteration]
        self.current_iteration += 1

    """Sends combat text above enemy head"""
    def send_combat_text(self, damage_dealt, crit):
        #sends combat text above player2
        if self.player_number == 1:
            if crit:
                combat_text = S.Combat_Text(750, 360, damage=critical_text.render("Critical " + "-" + str(damage_dealt), True, (255, 0, 0)))
            else:
                combat_text = S.Combat_Text(750, 360, damage=interface_stats.render("-" + str(damage_dealt), True, (255, 0, 0)))
            combat_text_list.append(combat_text)

        #sends combat text above player1
        elif self.player_number == 2:
            if crit:
                combat_text = S.Combat_Text(500, 360, damage=critical_text.render("Critical " + "-" + str(damage_dealt), True, (255, 0, 0)))
            else:
                combat_text = S.Combat_Text(500, 360, damage=interface_stats.render("-" + str(damage_dealt), True, (255, 0, 0)))
            combat_text_list.append(combat_text)

    """Determines if the target is player one or player two and returns that data!"""
    def get_target(self):
        if self.player_number == 1:
            target = Player_two
        elif self.player_number == 2:
            target = Player_one

        return target

    """Constantly updating buff and proc timers!"""
    def manage_procs(self):
        if self.weapon.on_fire:
            self.enchant_timer -= 1

            if self.enchant_timer <= 0:
                self.weapon.on_fire = False
                self.enchant_timer = 700

        if self.weapon.hastened:

            if self.enchant_timer <= 0:
                self.weapon.hastened = False
                self.enchant_timer = 700


        if self.weapon.hastened:
            self.enchant_timer -= 1
            return E.Hastened_Weapon_Enchant.buff #adds 100 speed
        else:
            return 0 #adds 0 speed

    """Checked each time player attacks, initaites procs and 
    applies fire damage to fiery_weapon enchantments"""
    def proc_chance(self):
        self.weapon.get_enchantment()

    def attack(self, target):
        final_attack_speed = self.attack_speed - self.weapon.get_total_speed() - self.manage_procs()


        if self.attack_on_cd:
            self.attack_timer += 1
            if self.attack_timer >= final_attack_speed:
                self.attack_on_cd = False
                self.current_iteration = 0

        else:
            self.iteration_list = self.attack_list
            if self.iteration_list[self.current_iteration] == self.iteration_list[-1]:
                #Deal logic damage
                self.proc_chance()
                current_attack_damage, critical = self.weapon.check_crit_and_fiery_weapon() # rounded in case float due to crit multipliers
                target.health -= current_attack_damage


                #Reset attributes for next attack
                self.attack_on_cd = True
                self.attack_timer = 0
                self.iteration_list = self.idle_list

                #Sends combat text above enemy head
                if critical:
                    crit = True
                else:
                    crit = False

                self.send_combat_text(current_attack_damage, crit)

    """Finds total incrememnt to surmount in order to attack with haste buff!"""
    def get_hastened_speed(self):
        hastened_speed = (self.attack_speed - int(self.weapon.get_total_speed())) - E.Hastened_Weapon_Enchant.buff
        return hastened_speed

    """Finds total incrememnt to surmount in order to attack WITHOUT haste buff!"""
    def get_normal_speed(self):
        normal_speed = self.attack_speed - int(self.weapon.get_total_speed())
        return normal_speed

    """Finds total speed for the weapon when hastened and when NOT hastened!"""
    def check_speed(self):
        if self.weapon.hastened:
            return int(self.weapon.get_total_speed()) + E.Hastened_Weapon_Enchant.buff
        else:
            return int(self.weapon.get_total_speed())
    """Reports the players attack delay and speed. Used by the interface module"""
    def report_next_attack(self):
        first_string = f"Attack Speed = Delay({self.attack_speed}) - Weapon Speed ({self.check_speed()})"
        final_string = f"{self.name.capitalize()}'s Next attack at: {self.attack_speed} - {int(self.check_speed())}"
        if self.weapon.hastened:
            next_attack = f"{self.attack_timer} / {self.get_hastened_speed()}"
        else:
            next_attack = f"{self.attack_timer} / {self.get_normal_speed()}"

        first_string = interface_stats.render(first_string, True, (173, 216, 230))
        final_string = interface_stats.render(final_string, True, (173, 216, 230))
        next_attack = interface_stats.render(next_attack, True, (173, 216, 230))
        return first_string, final_string, next_attack


    def examine_weapon(self):
        print(f"\nThis is your base weapon: {self.weapon.name} {self.weapon.show_stats()}")
        if self.weapon.p1 != None:
            print(f"Part1 Blade: {self.weapon.p1.parts_name} {self.weapon.p1.show_stats()}")
        if self.weapon.p2 != None:
            print(f"Part2 Nozzel: {self.weapon.p2.parts_name} {self.weapon.p2.show_stats()}")
        if self.weapon.p3 != None:
            print(f"Part3 Trigger: {self.weapon.p3.parts_name} {self.weapon.p3.show_stats()}")
        print("\n")

    def report_final_weapon(self):

        print("\n=======================================\n"
              "! FINAL WEAPON REPORT !\n"
              "=========================================")
        print(f"Player: {self.name}")
        print(f"Weapon: {self.weapon.name}")
        print(f"part1: {self.weapon.p1.parts_name}, part2: {self.weapon.p2.parts_name}, part3: {self.weapon.p3.parts_name}")
        self.weapon.report_final_stats()


Player_one = Player(player_number=1, iteration_list=Images.sword_attack_left, img=Images.sword_attack_left[0])
Player_two = Player(player_number=2, iteration_list=Images.sword_attack_left, img=Images.sword_attack_left[0])

