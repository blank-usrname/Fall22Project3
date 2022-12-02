import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.loc = None
    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")
    def put_in_room(self, room):
        self.loc = room
        room.add_item(self)

class Weapon(Item):
    def __init__(self, name, desc, atk, wgt, acc):
        super().__init__(name, desc)
        self.atk = atk
        self.wgt = wgt
        self.acc = acc
        self.loc = None
    def describe(self):
        clear()
        print(self.desc)
        print("Weapon statistics:")
        print(f"Attack bonus: +{self.atk}")
        print(f"Accuracy: {self.acc}%")
        print(f"Weight: +{self.wgt}")
        print()
        input("Press enter to continue...")

class Armor(Item):
    def __init__(self, name, desc, defe, wgt):
        super().__init__(name, desc)
        self.defe = defe
        self.wgt = wgt
        self.acc = acc
        self.loc = None
    def describe(self):
        clear()
        print(self.desc)
        print("Armor statistics:")
        print(f"Defense bonus: +{self.defe}")
        print(f"Weight: +{self.wgt}")
        print()
        input("Press enter to continue...")

class Consumable(Item):
    def __init__(self, name, desc, hp_heal, buff, buff_type):
        super().__init__(name, desc)
        self.hp_heal = hp_heal
        self.buff = buff
        self.buff_type = buff_type
        self.loc = None
    def consume(self, player):
        clear()
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
        input("Press enter to continue...")