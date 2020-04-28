import pygame
import Images
import Players as P
import Stats as S
import Procs
import Parts
import Weapons as W

update = pygame.display.update
pygame.init()
#win = pygame.display.set_mode((1400, 800))
green = (0, 255, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

combatTextBold = pygame.font.SysFont('segoeuisemibold', 18)

display_icon_title = pygame.font.SysFont("algerian", 14)
display_icon_text = pygame.font.SysFont('segoeuisemibold', 10)




class Icon:

    def __init__(self, weap_part, x, y, is_weap):
        self.weap_part = weap_part
        self.x = x
        self.y = y
        self.is_weap = is_weap # determines if the class is a weapon or not (defaulting back to being a part)

def create_icons():

    Player_one_weapon_icon = Icon(weap_part = P.Player_one.weapon, x=100, y=650, is_weap = True)
    Player_one_p1_icon = Icon(weap_part = P.Player_one.weapon.p1, x=225, y=700, is_weap = False)
    Player_one_p2_icon = Icon(weap_part = P.Player_one.weapon.p2, x=275, y=700, is_weap = False)
    Player_one_p3_icon = Icon(weap_part = P.Player_one.weapon.p3, x=325, y=700, is_weap = False)
    Player_one_icon_list = [Player_one_weapon_icon, Player_one_p1_icon, Player_one_p2_icon, Player_one_p3_icon]

    Player_two_weapon_icon = Icon(weap_part = P.Player_two.weapon, x=900, y=650, is_weap = True)
    Player_two_p1_icon= Icon(weap_part = P.Player_two.weapon.p1, x=1025, y=700, is_weap = False)
    Player_two_p2_icon= Icon(weap_part = P.Player_two.weapon.p2, x=1075, y=700, is_weap = False)
    Player_two_p3_icon= Icon(weap_part = P.Player_two.weapon.p3, x=1125, y=700, is_weap = False)
    Player_two_icon_list = [Player_two_weapon_icon, Player_two_p1_icon, Player_two_p2_icon, Player_two_p3_icon]

    Players_icon_lists = Player_one_icon_list + Player_two_icon_list


class Icon_Display:
    current_icon = None
    damage_display = 0
    speed_display = 0
    crit_display = 0
    x = y = tx = ty = dx = dy = sx = sy = cx = cy = ex = ey = 0 #t() title  d() damage  s() speed  c() crit
    image = Images.icon_display_background
    string_len = 0

    def create_icons(self):

        Player_one_weapon_icon = Icon(weap_part=P.Player_one.weapon, x=100, y=650, is_weap=True)
        Player_one_p1_icon = Icon(weap_part=P.Player_one.weapon.p1, x=225, y=700, is_weap=False)
        Player_one_p2_icon = Icon(weap_part=P.Player_one.weapon.p2, x=275, y=700, is_weap=False)
        Player_one_p3_icon = Icon(weap_part=P.Player_one.weapon.p3, x=325, y=700, is_weap=False)
        Player_one_icon_list = [Player_one_weapon_icon, Player_one_p1_icon, Player_one_p2_icon, Player_one_p3_icon]

        Player_two_weapon_icon = Icon(weap_part=P.Player_two.weapon, x=900, y=650, is_weap=True)
        Player_two_p1_icon = Icon(weap_part=P.Player_two.weapon.p1, x=1025, y=700, is_weap=False)
        Player_two_p2_icon = Icon(weap_part=P.Player_two.weapon.p2, x=1075, y=700, is_weap=False)
        Player_two_p3_icon = Icon(weap_part=P.Player_two.weapon.p3, x=1125, y=700, is_weap=False)
        Player_two_icon_list = [Player_two_weapon_icon, Player_two_p1_icon, Player_two_p2_icon, Player_two_p3_icon]

        self.Players_icon_lists = Player_one_icon_list + Player_two_icon_list

    """Adjust text locations to fit inside the display_icon_box!"""
    def adjust_text_locations(self):
        if self.string_len > 10:
            self.tx = self.x + 15
        else:
            self.tx = self.x + 40

        self.dx, self.sx, self.cx, self.ex = self.x + 5, self.x + 5, self.x + 5, self.x + 5
        self.ty = self.y + 4
        self.dy = self.y + 25
        self.sy = self.y + 40
        self.cy = self.y + 55
        self.ey = self.y + 70

    """retrieves data from icon hovered over by the mouse and sends the information
    to the icon display class! (CALLED IN INTERFACE CONTROLS)"""
    def retrieve_data(self, icon):
        if self.current_icon != icon:
            self.current_icon = icon
            if isinstance(icon.weap_part, Parts.Part):
                self.image = Images.icon_display_background
                self.title_display = display_icon_title.render(f"{icon.weap_part.parts_name}", True, green)
                self.string_len = len(self.current_icon.weap_part.parts_name)

            elif isinstance(icon.weap_part, W.Weapons):
                self.image = Images.icon_display_background_large
                self.title_display = display_icon_title.render(f"{icon.weap_part.name}", True, green)
                self.string_len = len(self.current_icon.weap_part.name)
                self.enchantment_display = display_icon_text.render(f"Enchant: {icon.weap_part.get_enchantment_quick_text()}", True, green)

            self.damage_display = display_icon_text.render(f"Damage: {icon.weap_part.damage}", True, green)
            self.speed_display = display_icon_text.render(f"Speed: {icon.weap_part.speed}", True, green)
            self.crit_display = display_icon_text.render(f"Crit: {icon.weap_part.crit}", True, green)

            #Adjust to be right of and above icon being seen by the mouse
            if icon.is_weap:
                self.x = self.current_icon.x + 30
            else:
                self.x = self.current_icon.x + 15

            self.y = self.current_icon.y - 100
            self.adjust_text_locations()

icon_display = Icon_Display()

class Interface:

    winner_text = "" # Text becomes winner's name when game ends displayed to screen (AS A SURFACE)

    def __init__(self, id):
        self.id = id
        self.window = pygame.display.set_mode((1400, 800))

        self.p1_proc_manager = Procs.Proc(player=P.Player_one, enchant=P.Player_one.weapon.enchantment.name, window=self.window)
        self.p2_proc_manager = Procs.Proc(player=P.Player_two, enchant=P.Player_two.weapon.enchantment.name, window=self.window)


    """Listens for player exit commands and relays information from icons
    based off current mouse position!"""
    def interface_controls(self):
        event = pygame.event.poll()
        mousePosition = pygame.mouse.get_pos()


        # only prompts detection when mouse towards bottom of screen

        if mousePosition[1] >= 600:
            for icon in icon_display.Players_icon_lists:
                if mousePosition[0] in range(icon.x, icon.x + icon.weap_part.image.get_width()) and \
                    mousePosition[1] in range(icon.y, icon.y + icon.weap_part.image.get_height()):

                    icon_display.retrieve_data(icon)
                    self.window.blit(icon_display.image, (icon_display.x, icon_display.y))
                    self.window.blit(icon_display.title_display, (icon_display.tx, icon_display.ty))
                    self.window.blit(icon_display.damage_display, (icon_display.dx, icon_display.dy))
                    self.window.blit(icon_display.speed_display, (icon_display.sx, icon_display.sy))
                    self.window.blit(icon_display.crit_display, (icon_display.cx, icon_display.cy))

                    if isinstance(icon.weap_part, W.Weapons):
                        self.window.blit(icon_display.enchantment_display, (icon_display.ex, icon_display.ey))


        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_ESCAPE]:
            print(pygame.quit())
            exit()


    def draw_player_icons(self):
        for icon in icon_display.Players_icon_lists:
            self.window.blit(icon.weap_part.image, (icon.x, icon.y))

    def draw_player_names(self):
        self.window.blit(P.Player_one.display_name, (150, 45))
        self.window.blit(P.Player_two.display_name, (950, 45))


    """Draws player health bars and determines their color based of Percent of health remaining!"""
    def draw_player_health(self):
        def color_of_health(health, max_health):
            if health > max_health * .70:
                return green
            elif health > max_health * .40:
                return yellow
            else:
                return red

        #Player one health bar
        pygame.draw.rect(self.window, (color_of_health(P.Player_one.health, P.Player_one.max_health)),
                         (100, 100, round(P.Player_one.health) / 2, 15))

        #Player two health bar
        pygame.draw.rect(self.window, (color_of_health(P.Player_two.health, P.Player_two.max_health)),
                         (900, 100, round(P.Player_two.health / 2), 15))


    """Draws the images and text for when procs are active!"""
    def show_procs(self, player):
        self.p1_proc_manager.draw_template()
        self.p2_proc_manager.draw_template()


    """Shows when an enchantment has become effective"""
    def draw_player_procs(self):
        self.show_procs(P.Player_one)
        self.show_procs(P.Player_two)


    """Draws both players Final Stats of their weapons and it's parts to the interface!"""
    def draw_player_stats(self):
        player1_stats_text = P.Player_one.weapon.report_final_stats(to_interface=True)
        player2_stats_text = P.Player_two.weapon.report_final_stats(to_interface=True)
        self.window.blit(player1_stats_text, (100, 150))
        self.window.blit(player2_stats_text, (900, 150))

    """Draws the delay and attack speed of each player as well as the time before their next attack!"""
    def draw_player_timed_attacks(self):
        player1_delay, player1_final_speed, player1_next_attack = P.Player_one.report_next_attack()
        player2_delay, player2_final_speed, player2_next_attack = P.Player_two.report_next_attack()
        self.window.blit(player1_delay, (100, 200))
        self.window.blit(player1_final_speed, (100, 225))
        self.window.blit(player1_next_attack, (150, 250))

        self.window.blit(player2_delay, (900, 200))
        self.window.blit(player2_final_speed, (900, 225))
        self.window.blit(player2_next_attack, (950, 250))


    """Draws each player"""
    def animate_draw_players(self):
        P.Player_one.animate_me()
        self.window.blit(P.Player_one.img, (500, 400))

        P.Player_two.animate_me()
        self.window.blit(P.Player_two.img, (600, 400))

        P.Player_one.attack(P.Player_two)
        P.Player_two.attack(P.Player_one)


    def draw_combat_text(self):
        for text in P.combat_text_list:
            self.window.blit(text.damage, (text.x, text.y))
            text.float()
            if text.finished:
                P.combat_text_list.remove(text)


    def all_player_calls(self):
        self.draw_player_names()
        self.draw_player_health()
        self.draw_player_stats()
        self.draw_player_timed_attacks()
        self.draw_player_procs()
        self.draw_player_icons()
        self.animate_draw_players()

    """Main drawing method using all other methods"""
    def draw_window(self):
        #event = pygame.event.poll()
        self.window.blit(Images.black_background, (0, 0))
        self.all_player_calls()
        self.draw_combat_text()

        #allow exit controls
        self.interface_controls()
        update()

    def draw_winner(self):
        self.window.blit(Images.black_background, (0, 0))
        self.window.blit(self.winner_text, (550, 250))

        def check_winner(self, player):
            if player.winner:
                player.animate_me()
                self.window.blit(player.img, (550, 300))

                self.window.blit(Images.restart_button, (572, 530))


        check_winner(self, P.Player_one)
        check_winner(self, P.Player_two)

        #controls used in Creations module
        update()

