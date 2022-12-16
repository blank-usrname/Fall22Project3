import os
import random

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, wgt, value):
        self.name = name
        self.wgt = wgt # weight has impact on holding capacity
        self.value = value # sell price of item, buying price is 2x
        self.desc = desc
        self.loc = None
    def describe(self):
        clear()
        print(self.desc)
        print(f"Weight: +{self.wgt}") 
        print()
        input("Press enter to continue...")
    def put_in_room(self, room):
        self.loc = room
        room.add_item(self)
    # functions to check type of an item
    def is_equippable(self): 
        return False
    def is_consumable(self):
        return False 
    def is_chest(self):
        return False

class Weapon(Item):
    def __init__(self, name, desc, atk, wgt, acc, value):
        super().__init__(name, desc, wgt, value) 
        self.atk = atk # bonus to attack power
        self.acc = acc # accuracy of weapon
        self.loc = None
    def describe(self):
        clear()
        print()
        print(self.desc)
        print()
        print(f"{self.name} statistics:")
        print(f"Attack bonus: +{self.atk}")
        print(f"Accuracy: {self.acc}%")
        print(f"Weight: +{self.wgt}") 
        print()
        input("Press enter to continue...")
    def is_equippable(self):
        return True
    def is_weapon(self):
        return True
    def is_consumable(self):
        return False 
    def is_chest(self):
        return False

class Armor(Item):
    def __init__(self, name, desc, defe, wgt, eva, value):
        super().__init__(name, desc, wgt, value)
        self.defe = defe # bonus to defense
        self.eva = eva # evasion bonus/penalty?
    def describe(self):
        clear()
        print(self.desc)
        print(f"{self.name} statistics:")
        print(f"Defense bonus: +{self.defe}")
        print(f"Evasion: {self.eva}")
        print(f"Weight: {self.wgt}")
        print()
        input("Press enter to continue...")
    def is_equippable(self):
        return True
    def is_weapon(self):
        return False
    def is_consumable(self):
        return False 
    def is_chest(self):
        return False

class Chest(Item):
    def __init__(self, name, desc, wgt, value, item):
        super().__init__(name, desc, wgt, value)
        self.value = 0 # doesn't make sense,,, for a chest
        self.wgt = 1000000 # doesn't make sense,,, for a chest
        self.item = item # contents of a chest
    def is_equippable(self):
        return False
    def is_weapon(self):
        return False
    def is_consumable(self):
        return False 
    def is_chest(self):
        return True
    def unlock(self, player): # chest unlock function,
        key = player.is_in_inventory("Chest Key")
        if (key != False): # check if player has a chest key
            if self.item.wgt + player.curr_carry >= player.carry: # check if player can carry contents of chest
                print("Unable to hold item, too heavy!")
            else: # unlock chest and take contents, remove chest from world
                player.drop(key)
                player.pickup(self.item)
                self.loc.remove_item(self)
        else:
            print("You do not have a key!")

class Consumable(Item):
    def __init__(self, name, desc, wgt, hp_heal, buff, buff_type, value, stack):
        super().__init__(name, desc, wgt, value)
        self.hp_heal = hp_heal # variable associated with consumable items that heal HP
        self.buff = buff # variable assocaited with consumable items that provide a permanant boost in a stat
        self.buff_type = buff_type # specify which stat is being buffed
        self.loc = None
        self.stack = stack # variable counting how many of item player is holding
    def consume(self, player): # this function seems to fit more in player compared to item,,, will change soon
        print(f"Used the {self.name}.")
        print()
        match self.buff_type:
            case "mhp": # consuming increases player's max HP by buff
                print(f"Max HP increased by {self.buff}!")
                player.mhp += self.buff
                player.health += self.buff
            case "atk": # consuming increases player's attack by buff
                print(f"Attack increased by {self.buff}!")
                player.atk += self.buff
            case "def": # consuming increases player's defense by buff
                print(f"Defense increased by {self.buff}!")
                player.defe += self.buff
            case "heal": # consuming recovers player's health by hp_heal
                player.health += self.hp_heal
                if (player.health > player.mhp): # check for HP overflow
                    player.health = player.mhp
                    print(f"HP is maxed out.")
                else:
                    print(f"HP healed by {self.hp_heal}.")
            case "all": # consuming increases player's max HP by hp_heal and all non-HP stats by buff
                print(f"Max HP increased by {self.hp_heal}!")
                print(f"All other stats increased by {self.buff}!")
                player.mhp += self.hp_heal
                player.health += self.hp_heal
                player.atk += self.buff
                player.defe += self.buff
                player.dex += self.buff
                player.spd += self.buff
        print()
        player.drop(self)
        input("Press enter to continue...")
    def is_equippable(self):
        return False
    def is_consumable(self):
        return True 
    def is_chest(self):
        return False

