import os
import random
from item import Weapon
from item import Armor

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self):
        self.name = "Player"
        self.location = None
        self.items = []
        self.armor = Armor("Cloth Shirt", "Everyday clothing.", 0, 0, 35, 100) # current equipped armor 
        self.weapon = Weapon("Sword", "A basic trainee's sword.", 2, 0, 95, 100) # current equipped weapon 
        self.level = 1
        self.mhp = 35 # maximum HP player has in battle
        self.msp = 15 # maximum SP player has in battle
        self.health = 35
        self.skill = self.msp
        self.atk = 2 # attack, increase damage dealt in battle (+1 damage dealt per 2 points of attack)
        self.defe = 2 # defense, reduces damage taken in battle (-1 damage taken per 2 points of attack)
        self.dex = 2 # dexterity, increases hit accuracy (+1% per 2 points of dexterity)
        self.spd = 2 # spd, increases evasion (+1% per 2 points of spd)
        self.carry = 50 # carrying capacity.
        self.curr_carry = self.armor.wgt + self.weapon.wgt # current sum of item weights (does it make sense to add armor and weapon weight?)
        self.exp = 0 # exp for leveling up, level up every 50*level exp
        self.gold = 1000
        self.alive = True

    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, direction):
        if ("(locked)" in direction):
            print("The door is locked.")
            return False
        new_location = self.location.get_destination(direction.lower())
        if new_location is not None:
            self.location = new_location
            return True
        return False

    # return accuracy of player character, based on weapon and dex/2
    def get_acc(self):
        acc = self.weapon.acc + self.dex // 2
        # keep accuracy bounded in [0, 100]
        if acc < 0:
            return 0
        elif acc > 100:
            return 100
        return acc 
    
    # return evasion of player character, based on armor and spd/2
    def get_eva(self):
        eva = self.armor.eva + self.spd // 2
        # keep evasion bounded in [0, 100]
        if eva < 0:
            return 0
        elif eva > 100:
            return 100
        return eva 
    
    # return damage of player character, based on atk/2 + weapon atk - enemy def / 2
    def get_dmg(self, enemy):
        dmg = self.atk // 2 + self.weapon.atk - enemy.defe // 2 
        return dmg if dmg > 0 else 0

    # checks if item causes exceed in current carrying capacity
    def can_pickup(self, item): # again, weapon and armor weight factores, should they be? (yes, for now)
        current_holding = self.curr_carry + item.wgt
        if (current_holding > self.carry):
            return False
        else:
            return True

    # places item in inventory
    def pickup(self, item):
        if (item.is_consumable()):
            # check if item is consumable, and stacks if item exists in inventory.
            i = self.is_in_inventory(item.name)
            if (i != False):
                i.stack += 1
            else: # appends if item does not exist in inventory.
                self.items.append(item)
            if (item.loc != None): # remove item from location picked up
                self.location.remove_item(item)
            item.loc = self # change item location to player character
            self.curr_carry += item.wgt # increase carrying weight
        else:
            self.items.append(item)
            if (item.loc != None): # remove item from location picked up
                self.location.remove_item(item)
            item.loc = self # change item location to player character
            self.curr_carry += item.wgt # increase carrying weight
    
    #checks if item is in inventory
    def is_in_inventory(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False

    # drops item; into the void...
    def drop(self, item):
        self.curr_carry -= item.wgt # remove weight of item being carries
        if (item.is_consumable() and item.stack > 1): # if item is consumable and item is a part of stack, decrement stack
            item.stack -= 1
        else: 
            self.items.remove(item)
            item.loc = None # is this behavior (dropping into void) preferred?
        # item.loc = self.location
        # self.location.add_item(item)
    
    # presents item data
    def show_inventory(self):# remove item from location picked up
        print()
        print("You are currently carrying:")
        print()
        for i in self.items:
            if (i.is_consumable()): # consumable items also specify how many of each is within inventory
                print(f"{i.name} ({i.stack})")
            else:
                print(i.name) # non consumable items don't stack
        print()
        print(f'Current Weapon: {self.weapon.name}, "{self.weapon.desc}"') # display current weapon and armor
        print(f'Current Armor: {self.armor.name}, "{self.armor.desc}"')
        print()
        print(f"You are currently using: {self.curr_carry}/{self.carry} total inventory slots.") # display how many inventory slots are being used
        print()
        input("Press enter to continue...")
    
    # checks if player has enough money to buy item
    def can_buy(self, item):
        if (item.value > self.gold):
            return False
        return True
    
    # code run to buy an item
    def buy(self, item):
        if (item.is_consumable()): # if item is consumable, check if item exists within inventory
            i = self.is_in_inventory(item.name)
            if (i != False): # if item is already in inventory, increment the stack of items
                i.stack += 1
            else: # if not, append item to list of items
                self.items.append(item)
                item.loc = self
            self.curr_carry += item.wgt
        else: # append item to list of items
            self.items.append(item)
            item.loc = self
            self.curr_carry += item.wgt
    
    # sell function, get half of value of item
    def sell(self, item):
        self.gold += (item.value // 2)
        self.drop(item)

    # equip weapon
    def equip_weapon(self, item):
        self.items.remove(item)
        self.items.append(self.weapon)
        self.weapon = item
    
    # equip armor
    def equip_armor(self, item):
        self.items.remove(item)
        self.items.append(self.armor)
        self.armor = item
    
    # "me" command, presents current status of player
    def show_status(self):
        print()
        print("Player status:")
        print()
        print(f"Level: {self.level}/10")
        print(f"Gold: {self.gold}")
        if (self.level >= 10):
            print(f"EXP: --")
        else:
            print(f"EXP: {self.exp}/{self.level * 15}")
        print(f"HP: {self.health}/{self.mhp}")
        print(f"Attack: {self.atk} (+{self.weapon.atk})")
        print(f"Defense: {self.defe} (+{self.armor.defe})")
        print(f"Dexterity: {self.dex}")
        print(f"Speed: {self.spd}")        
        print()
        print(f'Current Weapon: {self.weapon.name}, "{self.weapon.desc}"')
        print(f'Current Armor: {self.armor.name}, "{self.armor.desc}"')
        print(f"Accuracy: {self.get_acc()}")
        print(f"Evasion: {self.get_eva()}")   
        print()
        input("Press enter to continue...")
    
    # level up routine
    def level_up(self):
        """
        Level up routine, checks if eligible for level up, and then generates a random amount of stats (5-10) that
        player can distribute to each stats as they decide.
        """
        if (self.exp >= (15 * self.level) and self.level < 10): # level up every 20 * level exp, check if able to level up
            self.exp %= (15 * self.level)
            self.level += 1
            mhp_up = random.randint(3,7) # random hp distribution
            self.mhp += mhp_up
            self.health += mhp_up
            self.carry += 10
            print(f"Player's levelled up to level {self.level}!")
            points = random.randint(5,10) # random amount of points to distribute to four stats
            print(f"You have {points} points to distribute to stats.") 
            # for each stat (Atk, Def, Dex, Spd), choose to distribute points to each stat
            command_success = False
            while not command_success: # dsitribute points to Atk
                command_success = True
                print()
                print(f"Current: Atk: {self.atk}, Def: {self.defe}, Dex: {self.dex}, Spd: {self.spd}")
                print()
                command = input("How many points of attack to add? ")
                if len(command) == 0:
                    continue
                command_words = command.split()
                if len(command_words) == 0:
                    continue
                value = command_words[0] 
                if (command_words[0].isnumeric()):
                    value = int(value)
                    if (value >= 0 and value <= points):
                        points -= value
                        self.atk += value
                        print()
                        print(f"Attack increased by {value}!")
                        print()
                    else:
                        print()
                        print("Not possible!")
                        print()
                        command_success = False
            if (points > 0):# dsitribute points to Def
                print(f"You have {points} points left.")
                command_success = False
                while not command_success:
                    print()
                    print(f"Current: Atk: {self.atk}, Def: {self.defe}, Dex: {self.dex}, Spd: {self.spd}")
                    print()
                    command_success = True
                    command = input("How many points of defense to add? ")
                    if len(command) == 0:
                        continue
                    command_words = command.split()
                    if len(command_words) == 0:
                        continue
                    value = command_words[0] 
                    if (command_words[0].isnumeric()):
                        value = int(value)
                        if (value >= 0 and value <= points):
                            points -= value
                            self.defe += value
                            print()
                            print(f"Defense increased by {value}!")
                            print()
                        else:
                            print()
                            print("Not possible!")
                            print()
                            command_success = False
            if (points > 0): # dsitribute points to Dex
                print(f"You have {points} points left.")
                command_success = False
                while not command_success:
                    command_success = True
                    print()
                    print(f"Current: Atk: {self.atk}, Def: {self.defe}, Dex: {self.dex}, Spd: {self.spd}")
                    print()
                    command = input("How many points of dexterity to add? ")
                    if len(command) == 0:
                        continue
                    command_words = command.split()
                    if len(command_words) == 0:
                        continue
                    value = command_words[0] 
                    if (command_words[0].isnumeric()):
                        value = int(value)
                        if (value >= 0 and value <= points):
                            points -= value
                            self.dex += value
                            print()
                            print(f"Dexterity increased by {value}!")
                            print()
                        else:
                            print()
                            print("Not possible!")
                            print()
                            command_success = False
            if (points > 0): # dsitribute remaining points to Spd
                self.spd += points
                print(f"Speed increased by {points}!")
                print()
            print()
            input("Press enter to continue...")