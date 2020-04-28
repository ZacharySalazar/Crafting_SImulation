import Parts
import Weapons as W
import Players as P
import Enchantments as E
import Interfaces as I
import Images
import pygame
pygame.init()

player_name_text = pygame.font.SysFont('Comic Sans MS', 30)


class Creator:
    game_ready = False # Becomes True when both players have Finalized weapon creation
    interface_created = False # Prompts window creation when console has all data about players inputted
    player_characters_created = False # Becomes True when the player character images have been assigned to players

    virtual_weapon = W.Weapons(name="virutal", equip_keybind=0) # Utilized as a copy for player weapons to finalize
                                                                # against!

    virtual_p1 = virtual_p2 = virtual_p3 = None # Utilized as a clone for player weapon creation

    current_player = P.Player_one
    weapon_dict = {1: W.Weapons(image = Images.waraxe_img, name = "Waraxe", equip_keybind=1, damage=8, speed=100, crit=5),
                   2: W.Weapons(image = Images.sword_img, name = "Sword", equip_keybind=2, damage=5, speed=150, crit=5),
                   3: W.Weapons(image = Images.mace_img, name = "Mace", equip_keybind=3, damage=10, speed=50, crit=10),
                   4: W.Weapons(image = Images.dagger_img, name = "Dagger", equip_keybind=4, damage=2, speed=250, crit=30)}

    current_parts_dict = None  #Current dictionary actively being browsed for parts
    blades_dict = {1: Parts.Part(image = Images.chainblade_img, parts_name="ChainBlade", equip_keybind= 1, placement="blades", damage = 10),
                   2: Parts.Part(image = Images.bayonet_img, parts_name="Bayonet", equip_keybind= 2, placement="blades", damage=3, speed=50),
                   3: Parts.Part(image = Images.zapper_img, parts_name="Zapper", equip_keybind= 3, placement="blades", crit=10)}

    nozzels_dict = {1: Parts.Part(image = Images.cannon_img, parts_name="Cannon_Fluid", equip_keybind= 1,  placement="nozzels", damage=5, speed=50),
                    2: Parts.Part(image = Images.repeater_img, parts_name="Repeater_Fluid", equip_keybind= 2, placement="nozzels", speed=100),
                    3: Parts.Part(image = Images.flamethrower_img, parts_name="Flamethrower_Fluid", equip_keybind= 3, placement="nozzels", crit=10)}

    triggers_dict = {1: Parts.Part(image = Images.big_billy_img, parts_name="Big Billy", equip_keybind= 1, placement="triggers", damage=5, speed=50),
                     2: Parts.Part(image = Images.standard_img, parts_name="Standard", equip_keybind= 2, placement="triggers", damage=3, speed=20, crit=5),
                     3: Parts.Part(image = Images.deceptive_img, parts_name="Deceptive", equip_keybind= 3, placement="triggers", damage=-5, speed=-5, crit=20)}

    """Returns the player number alongwith their chosen names!"""
    def get_player(self):
        if self.current_player == P.Player_one:
            return "\n" + "(Player_One" + ": " + self.current_player.name + ")"
        elif self.current_player == P.Player_two:
            return "\n" + "(Player_Two" + ": " + self.current_player.name + ")"

    """Connects player to character images based off the weapon they chose!"""
    def create_player_character(self):
        P.Player_one.idle_list, P.Player_one.attack_list = Images.get_player_image(player=P.Player_one, player_num=1)
        P.Player_one.iteration_list = P.Player_one.idle_list

        P.Player_two.idle_list, P.Player_two.attack_list = Images.get_player_image(player=P.Player_two, player_num=2)
        P.Player_two.iteration_list = P.Player_two.idle_list

    def decide_winner(self):
        if P.Player_one.health <= 0:
            self.Interface.winner_text = player_name_text.render(f"{P.Player_two.name} wins!".upper(), True, (0, 255, 0))
            P.Player_two.winner = True

        elif P.Player_two.health <= 0:
            self.Interface.winner_text = player_name_text.render(f"{P.Player_one.name} wins!".upper(), True, (0, 255, 0))
            P.Player_one.winner = True

    def restart_game(self):
        self.virtual_weapon = W.Weapons(name="virutal", equip_keybind=0)
        self.virtual_p1, self.virtual_p2, self.virtual_p3 = None, None, None
        self.current_player = P.Player_one
        self.interface_created = False

        self.player_characters_created = False
        P.Player_two.name = False # resets for asking for names again
        P.Player_one.winner, P.Player_one.health, P.Player_two.winner, P.Player_two.health = False, 750, False, 750
        P.Player_one.reset_me()
        P.Player_two.reset_me()

        self.game_ready = False

        pygame.display.quit()
        print("restarting game\n\n")

    """Opens and runs the game window after all players, weapons, and parts have been configured!"""
    def run_game(self):
        if not self.interface_created:
            self.Interface = I.Interface(id="interface_one")
            self.interface_created = True
            I.icon_display.create_icons()

        if not self.player_characters_created:
            self.create_player_character()
            self.player_characters_created = True


        self.decide_winner()
        #Determine interface being drawn based on if winner is found or not
        if self.Interface.winner_text == "":
            self.Interface.draw_window()
        else:
            self.Interface.draw_winner()
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.restart_game()



    """Sets up Player choices inclding name, weapons, parts, and enchantments using the console prompts!"""
    def setup(self):
        if not P.Player_two.name:
            self.ask_name()

        if not self.game_ready:
            self.ask_weapon()
            self.ask_for_parts()

        elif self.game_ready:
            self.run_game()

        # if self.current_player == Player_one:
        #     self.current_player = Player_two
        # else:
        #     print('done')

    """Prompts the user to move on to enchants or replace weapons/parts! (Only active when all part slots are filled!"""
    def check_parts_complete(self):
        next_step = int(input(self.get_player() + " Your weapon has all it's parts!\n Press 1: Proceed to Enchantments\n"
                              " Press 2: Replace Weapon\n Press 3: Replace Parts "))

        # Finalizes the weapon and it's parts making the player weapon and parts immutable from here on.
        if next_step == 1:
            self.craft_virtual_weapon()
            self.current_player.weapon = self.virtual_weapon
            self.ask_enchantment()


        elif next_step == 2:
            self.ask_weapon(replacing=True)
        elif next_step == 3:
            self.ask_for_parts()

    """Asks for the player name to assign to their player class!"""
    def ask_name(self):
        name_given = input("What is your name? ")
        self.current_player.name = name_given
        self.current_player.display_name = player_name_text.render(name_given, True, (0, 255, 0))


    """Prompts player for enchant choice and then binds chosen enchant to the player's weapon!"""
    def ask_enchantment(self):
        E.Enchantment.show_enchants()
        enchant_choice = int(input("Choose your enchantment. "))
        enchant_choice = E.Enchantment.determine_enchant(enchant_choice)

        #Officially binds enchant to the player Weapon.
        self.current_player.weapon.enchantment = E.Enchantment(name=enchant_choice, player=self.current_player,
                                                        weapon=self.current_player.weapon)
        self.current_player.report_final_weapon()
        progress = input("Press any button to continue")


        #Change players so that player 2 may begin their Weapon Creation
        if self.current_player == P.Player_one:
            self.current_player = P.Player_two
            self.virtual_p1 = self.virtual_p2 = self.virtual_p3 = None

        elif self.current_player == P.Player_two:
            self.game_ready = True


    """Displays weapons and their stats as well as promopts the user to make a choice!"""
    def ask_weapon(self, replacing=False):
        print(self.get_player() + " here are the weapons you may choose from.")
        W.Waraxe.show_info()
        W.Sword.show_info()
        W.Mace.show_info()
        W.Dagger.show_info()
        weapon_number = int(input("What Base Weapon do you want? "))

        chosen_weapon = self.weapon_dict[weapon_number]
        self.virtual_weapon = chosen_weapon
        if replacing:
            self.display_virtual_weapon()
            self.check_parts_complete()

    """Prompts the player to choose which Parts they wish to browse to augment their weapons with!"""
    def ask_for_parts(self):
        answer = int(input(self.get_player() + " What parts are you looking for?\n1: Blades\n2: Nozzels\n3: Triggers\n"))
        if answer == 1:
            self.browse_parts("blades")
        elif answer == 2:
            self.browse_parts("nozzels")
        elif answer == 3:
            self.browse_parts("triggers")

    """Creates a virutal part for the virtual weapon that the player weapon can copy once it's completely
    assimilated!"""
    def add_virtual_part(self, part):
        if part.placement == "blades":
            self.virtual_p1 = part
        elif part.placement == "nozzels":
            self.virtual_p2 = part
        elif part.placement == "triggers":
            self.virtual_p3 = part

    """Binds all the virtual parts to the virutal weapon for the player to copy"""
    def craft_virtual_weapon(self):
        self.virtual_weapon.p1 = self.virtual_p1
        self.virtual_weapon.p2 = self.virtual_p2
        self.virtual_weapon.p3 = self.virtual_p3

    """Displays the entire virutal weapon including all its current parts!"""
    def display_virtual_weapon(self):
        print("\n=======================================\n"
              "! WEAPON REPORT !\n"
              "=======================================")
        print(f"This is your base weapon: {self.virtual_weapon.name} {self.virtual_weapon.show_stats()}")
        if self.virtual_p1 != None:
            print(f"Part1 Blade: {self.virtual_p1.parts_name} {self.virtual_p1.show_stats()}")
        if self.virtual_p2 != None:
            print(f"Part2 Nozzel: {self.virtual_p2.parts_name} {self.virtual_p2.show_stats()}")
        if self.virtual_p3 != None:
            print(f"Part3 Trigger: {self.virtual_p3.parts_name} {self.virtual_p3.show_stats()}")
        print("\n")

    """Browses available Parts and their stats!"""
    def browse_parts(self, parts_type):
        def show_info_for(self, dict):
            for v in dict.values():
                v.show_info()
            self.current_parts_dict = dict

        if parts_type == "blades" or parts_type[0] == "b":
            show_info_for(self, self.blades_dict)


        elif parts_type == "nozzels":
            show_info_for(self, self.nozzels_dict)


        elif parts_type == "triggers":
            show_info_for(self, self.triggers_dict)


        #Equip to virtual weapon
        key_pressed = int(input("Which part would you like to equip? "))
        adding_part = self.current_parts_dict[key_pressed]
        self.add_virtual_part(adding_part)
        self.display_virtual_weapon()

        # Check if the player has all their weapon slots filled!
        if self.virtual_p1 == None or self.virtual_p2 == None or \
            self.virtual_p3 == None:
            print("Your Weapon is still missing parts. Make sure you have all 3 slots filled.")
            self.ask_for_parts()

        else:
            self.check_parts_complete()




creator = Creator()