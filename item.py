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
    def is_equippable(self):
        return False
    def is_consumable(self):
        return False 

class Weapon(Item):
    def __init__(self, name, desc, atk, wgt, acc, value):
        super().__init__(name, desc, wgt, value) # weight has additional effect on weapons of lowering one's evasion (does this one make any sense?)
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

class Armor(Item):
    def __init__(self, name, desc, defe, wgt,value):
        super().__init__(name, desc, wgt,value) # weight has additional effect of lowering one's evasion (does this one make any sense?)
        self.defe = defe # bonus to defense
    def describe(self):
        clear()
        print(self.desc)
        print(f"{self.name} statistics:")
        print(f"Defense bonus: +{self.defe}")
        print(f"Weight: +{self.wgt}")
        print()
        input("Press enter to continue...")
    def is_equippable(self):
        return True
    def is_weapon(self):
        return False
    def is_consumable(self):
        return False 

class Consumable(Item):
    def __init__(self, name, desc, wgt, hp_heal, buff, buff_type, value):
        super().__init__(name, desc, wgt, value)
        self.hp_heal = hp_heal
        self.buff = buff
        self.buff_type = buff_type
        self.loc = None
    def consume(self, player): # this function seems to fit more in player compared to item,,, will change soon
        print(f"Used the {self.name}.")
        print()
        # if (sp_heal != 0): # two different ifs used here,,, deciding if hp/sp healing items are mutually exclusive... atm no...
        #     print(f"HP healed by {hp_heal}.")
        #     print(f"HP healed by {hp_heal}.")
        match self.buff_type:
            case "mhp":
                print(f"Max HP increased by {self.buff}!")
                player.mhp += self.buff
                player.health += self.buff
            case "mhp":
                print(f"Max HP increased by {self.buff}!")
                player.mhp += self.buff
                player.health += self.buff
            case "atk":
                print(f"Attack increased by {self.buff}!")
                player.atk += self.buff
            case "def":
                print(f"Defense increased by {self.buff}!")
                player.defe += self.buff
            case "heal":
                player.health += self.hp_heal
                if (player.health > player.mhp):
                    player.health = player.mhp
                    print(f"HP is maxed out.")
                else:
                    print(f"HP healed by {self.hp_heal}.")
            case "all":
                print(f"Max HP increased by {self.hp_heal}!")
                print(f"All stats increased by {self.buff}!")
                player.mhp += self.hp_heal
                player.health += self.hp_heal
                player.atk += self.buff
                player.defe += self.buff            
        print()
        player.items.remove(self)
        player.curr_carry -= self.wgt
        input("Press enter to continue...")
    def is_equippable(self):
        return False
    def is_consumable(self):
        return True 