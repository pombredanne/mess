import random


class Combat:
    dodge_limit = 6
    attack_limit = 6

    def dodge(self):
        roll = random.randint(1, self.dodge_limit)
        return roll > 4

    def attack(self):
        roll = random.randint(1, self.attack_limit)
        return roll > 4


class Character(Combat):
    attack_limit = 10
    experience = 0
    hit_points = 10

    def attack(self):
        roll = random.randint(1, self.attack_limit)
        if self.weapon == 'sword':
            roll += 1
        elif self.weapon == 'axe':
            roll += 2
        return roll > 4

    def get_weapon(self):
        weapon_choice = raw_input("Weapon ([S]word, [A]xe, [B]ow): ").lower()

        if weapon_choice in 'sab':
            if weapon_choice == 's':
                return 'sword'
            elif weapon_choice == 'a':
                return 'axe'
            else:
                return 'bow'
        else:
            return self.get_weapon()

    def __init__(self, **kwargs):
        self.name = raw_input("Name: ")
        self.weapon = self.get_weapon()

        for key, value in kwargs.items():
            setattr(self, key, value)
