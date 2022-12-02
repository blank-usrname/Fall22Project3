import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.level = 1
        self.mhp = 50
        self.health = self.mhp
        self.atk = 5
        self.defe = 5
        self.exp = 0
        self.alive = True
    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, direction):
        new_location = self.location.get_destination(direction.lower())
        if new_location is not None:
            self.location = new_location
            return True
        return False
    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.remove_item(item)
    def show_inventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        input("Press enter to continue...")
    def attack_monster(self, mon):
        clear()
        print("You are attacking " + mon.name)
        print()
        print("Your health is " + str(self.health) + ".")
        print(mon.name + "'s health is " + str(mon.health) + ".")
        print()
        if self.health > mon.health:
            self.health -= (mon.health + self.defe)
            print("You win. Your health is now " + str(self.health) + ".")
            mon.die()
            exp = (mon.level//self.level) + 3
            print("Awarded " + str(exp) + " exp.")
            self.exp += exp
            self.level_up()
        else:
            print("You lose.")
            self.alive = False
        print()
        input("Press enter to continue...")
    def attack_monster2(self, mon):
        clear()
        print("You are attacking " + mon.name)
        if (self.health >= 0 and mon.health >= 0):
            print()
            print("Your health is " + str(self.health) + ".")
            print(mon.name + "'s health is " + str(mon.health) + ".")
            print()
            print("What action will you take?")
            print("[A]ttack, [R]un")
            while (self.health >= 0 and mon.health >= 0):
                continue
        print()
        input("Press enter to continue...")
    def drop(self, item):
        self.items.remove(item)
    def show_status(self):
        clear()
        print("Player status:")
        print()
        print(f"Player level: {self.level}")
        print(f"Player health: {self.health}/{self.mhp}")
        print(f"Attack: {self.atk}")
        print(f"Defense: {self.defe}")
        print()
        input("Press enter to continue...")
    def level_up(self):
        if (self.exp >= (50 * self.level)):
            self.exp %= (50 * self.level)
            self.level += 1
            mhp_up = random.randint(5,10)
            self.mhp += mhp_up
            self.health += mhp_up
            atk_up = random.randint(1,3)
            self.atk += atk_up
            defe_up = random.randint(1,3)
            self.defe += defe_up
            self.exp = self.exp % 100
            print(f"Player's levelled up to level {self.level}!")
            print(f"Max HP increased by {mhp_up}!")
            print(f"Attack increased by {atk_up}!")
            print(f"Defense increased by {defe_up}!")
        else:
            return