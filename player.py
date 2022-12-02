import os
import random
from item import Weapon
from item import Armor

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.location = None
        self.items = []
        self.armor = Armor("Cloth shirt", "Everyday clothing.", 1, 1) # current equipped armor 
        self.weapon = Weapon("Sword", "A basic trainee's sword.", 1, 1, 90) # current equipped weapon 
        self.level = 1
        self.mhp = 50 # maximum HP player has in battle
        self.health = self.mhp 
        self.atk = 2 # attack, increase damage dealt in battle
        self.defe = 2 # defense, reduces damage taken in battle
        self.carry = 40 + 10 * self.level # carrying capacity goes up with level.
        self.curr_carry = self.armor.wgt + self.weapon.wgt # current sum of item weights (does it make sense to add armor and weapon weight?)
        self.exp = 0 # exp for leveling up, level up every 50*level exp
        self.gold = 200
        self.alive = True
    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, direction):
        new_location = self.location.get_destination(direction.lower())
        if new_location is not None:
            self.location = new_location
            return True
        return False
    def can_pickup(self, item): # again, weapon and armor weight factored, should they be?
        current_holding = self.curr_carry + item.wgt
        if (current_holding > self.carry):
            return False
        else:
            return True
    def pickup(self, item):
        self.items.append(item)
        item.loc = self
        self.location.remove_item(item)
        self.curr_carry += item.wgt
    def is_in_inventory(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    def drop(self, item):
        self.curr_carry -= item.wgt # why isn't this working? consume seems to work however,,,
        self.items.remove(item)
        item.loc = None # is this behavior preferred?
        # item.loc = self.location
        # self.location.add_item(item)
    def show_inventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        print(f"You are currently using: {self.curr_carry}/{self.carry} total inventory slots.")
        print()
        input("Press enter to continue...")
    def drop(self, item):
        self.items.remove(item)
    def equip_weapon(self, item):
        self.items.remove(item)
        self.items.append(self.weapon)
        self.weapon = item
    def equip_armor(self, item):
        self.items.remove(item)
        self.items.append(self.armor)
        self.armor = item
    def show_status(self):
        clear()
        print("Player status:")
        print()
        print(f"Level: {self.level}")
        print(f"EXP: {self.exp}/{self.level * 50}")
        print(f"HP: {self.health}/{self.mhp}")
        print(f"Attack: {self.atk} (+{self.weapon.atk})")
        print(f"Defense: {self.defe} (+{self.armor.defe})")
        print()
        print(f'Current Weapon: {self.weapon.name}, "{self.weapon.desc}"')
        print(f'Current Armor: {self.armor.name}, "{self.armor.desc}"')
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