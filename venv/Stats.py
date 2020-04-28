import Images

"""Enables inheretence to all attribute referencing classes"""
class Stats:
    def __init__(self, image, damage=0, speed=0, crit=0):
        self.image = image
        self.damage = damage
        self.speed = speed
        self.crit = crit

    """Shortcut for indenting text"""
    def indent(self):
        indenting = "         "
        return indenting

    def show_stats(self):
        return_string = f" (Damage: {self.damage}) (Speed: {self.speed}) (Crit: {self.crit})"
        return return_string


class Frame:
    current_iteration = 0

    def __init__(self, iteration_list, img):
        self.iteration_list = iteration_list
        self.img = img

    def animate_me(self):
        if self.current_iteration >= len(self.iteration_list):
            self.current_iteration = 0

        self.img = self.iteration_list[self.current_iteration]
        self.current_iteration += 1

p1_fireball = Frame(iteration_list=Images.fireball, img=Images.fireball[0])
p2_fireball = Frame(iteration_list=Images.fireball, img=Images.fireball[0])

p1_haste = Frame(iteration_list=Images.haste, img=Images.haste[0])
p2_haste = Frame(iteration_list=Images.haste, img=Images.haste[0])

class Combat_Text:
    finished = False

    def __init__(self, x, y, damage, enchant=False):
        self.x = x
        self.starting_y = y + 50
        self.y = self.starting_y
        self.anchor_y = y
        self.damage = damage

    def float(self):
        if not self.finished:
            self.y -= .2
            if self.y <= self.anchor_y:
                self.finished = True
