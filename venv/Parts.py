import Stats as S
import Images

"""Parts of Weapons that increase weapons and user of that weapon's stats."""
class Part(S.Stats):
    information_text = ""
    #Weapon augments:    damage_mod   stun_mod   speed
    #Damage determines the amount of damage each attack does
    #Speed means higher the number the faster attack (Deducts number from attack cd time)
    #Crit means the higher the number the better the chance to crit for double damage

    def __init__(self, image, parts_name, equip_keybind, placement, damage=0, speed=0, crit=0):
        S.Stats.__init__(self, image, damage, speed, crit)

        self.parts_name = parts_name
        self.equip_keybind = equip_keybind #key pressed to equip the part
        self.placement = placement  #(Used to determine which placement slot is taken up on the weapons)
                                    #blade is edge, nozzel is ranged, handle is balancing

    """Used for repetative text insertion in self.show_info"""
    def no_change(self):
        self.information_text += "No Change"


    """Shows player the stats yielded by Parts when equipped to Weapons
    through printing to console."""
    def show_info(self):
    #Damage
        self.information_text = "\n" + self.indent() + "Damage: "
        if self.damage != None:
            if self.damage > 0:
                self.information_text += "+" + str(self.damage)
            else:
                self.information_text += str(self.damage)
        else:
            self.no_change()

    #Speed
        self.information_text += "\n" + self.indent() + "Speed: "
        if self.speed != None:
            if self.speed > 0:
                self.information_text += "+" + str(self.speed)
            else:
                self.information_text += str(self.speed)
        else:
            self.no_change()

    #Crit
        self.information_text += "\n" + self.indent() + "Crit: "
        if self.crit != None:
            if self.crit > 0:
                self.information_text += "+" + str(self.crit)
        else:
            self.no_change()

        print(f"{self.parts_name}: Press {self.equip_keybind} to equip! {self.information_text}\n")


