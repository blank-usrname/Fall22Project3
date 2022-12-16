import os
import random
import system
from item import Item
from item import Consumable

import updater

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Monster:
    # TO ADD: variability in drops, additional monster types(?) (such as bosses?)
    # AI type, is that necessary?
    def __init__(self, name, level, room):
        self.name = name
        self.room = room
        self.level = level
        self.gold = 0 # determines gold drop of enemy
        self.health = 10
        self.mhp = self.health
        self.atk = 3
        self.defe = 3
        self.acc = 80
        self.spd = 2
        self.exp = 0 # determines exp drop of enemy
        self.modifier() # modifier func, models stats based on specific monster type
        room.add_monster(self)
        updater.register(self)
    
    def modifier(self):
        # modifies stats of enemy based on their type
        match self.name:
            case "Slime":
                # built to be generally weak, unagile, and low defenses, shirks away from combat, easy pickings.
                self.mhp = 20 + 5 * (self.level)
                self.health = self.mhp
                self.atk = 3 + 1 * (self.level)
                self.defe = 0 + 1 * (self.level)
                self.acc = 95
                self.spd = 0
                self.gold = self.level * 110
                self.exp = self.level * 8
            case "Imp":
                # imps have higher than average hp, and high agility, high attack, middling defenses, and lower accuracy
                # lower potential for growth over time
                self.mhp = 40 + 3 * (self.level)
                self.health = self.mhp
                self.atk = 7 + 2 * (self.level)
                self.defe = 4 + 2 * (self.level)
                self.acc = 70
                self.spd = 8 + 4 * (self.level)
                self.gold = self.level * 160
                self.exp = self.level * 11
            case "Phantasm":
                # phantasms have lower than average hp, lower than average attack and defense, but good agility, accuracy,
                # and in combat, act much more varied in their combat, gneerally a scary threat
                self.mhp = 20 + 2 * (self.level)
                self.health = self.mhp
                self.atk = 5 + 2 * (self.level)
                self.defe = 5 + 2 * (self.level)
                self.acc = 85
                self.spd = 8 + 4 * (self.level)
                self.gold = self.level * 220
                self.exp = self.level * 15
            case "Straggler":
                # mini-boss, high HP, extreme attack, but low defenses, and does not act very much in combat
                self.mhp = 145
                self.health = self.mhp
                self.atk = 65
                self.defe = 25
                self.acc = 100
                self.spd = 0
                self.gold = 1500
            case "Boss":
                # boss, generally good stats except speed, somewhat inaccurte, can charge up attack to provide
                # great temp boost to attack, focus up to provide a small permenant boost to attack,
                # heal a small amount of HP.
                self.mhp = 125
                self.health = self.mhp
                self.atk = 40
                self.defe = 25
                self.acc = 75
                self.spd = 5
                self.gold = 3000
                self.exp = 0
    
    def get_acc(self):
        # return accuracy of monster (used in system.attack function)
        return self.acc
    
    def get_dmg(self, target):
        # return damage output of monster (used in system.attack function)
        dmg = self.atk // 2 - target.defe // 2 
        return dmg if dmg > 0 else 0

    def update(self):
        if (self.name != "Boss" or self.name != "Straggler"): 
            # what is *supposed* to happen is that the Boss and the Straggler don't move from their initial positions.
            target_loc = self.room.random_neighbor()
            if random.random() < .5 and (not target_loc.has_monsters()) and (not target_loc.has_npcs()):
                # monsters will not move into areas with a mosnter or npc already there
                self.move_to(target_loc)

    def move_to(self, room):
        self.room.remove_monster(self)
        self.room = room
        room.add_monster(self)

    def die(self):
        self.room.remove_monster(self)
        updater.deregister(self)
    
    def drop(self):
        # define drop items for enemy types, Straggler will always drop a key, Slimes drop slime gel (tl;dr: better salve)
        match self.name:
            case "Straggler":
                item = Item("Chest Key", "Use to unlock a chest", 0, 150)
                return item
            case "Slime":
                chance = random.random()
                if chance <= .5:
                    item = Consumable("Slime Gel", "Strangly soothing?", 1, 35, 0, "heal", 200, 1)
                    return item 
                else:
                    return False
        return False 


    def show_status(self):
        # display status of enemy
        print()
        print(f"{self.name} status:")
        print()
        print(f"Level: {self.level}")
        print(f"HP: {self.health}/{self.mhp}")
        print(f"Attack: {self.atk}")
        print(f"Defense: {self.defe}")
        print(f"Accuracy: {self.acc}")
        print(f"Evasion: {self.spd}")
        print()
        input("Press enter to continue...")

    def heal(self, amount):
        # heal function, utilized by phantasm and boss in their fights
        self.health += amount
        if (self.health > self.mhp):
            self.health = self.mhp

    def behavior(self, target):
        # function that defines AI per enemy type
        temp_atk = 0
        match self.name:
            case "Slime":
                # slimes weak, will not choose to attack half the time
                choice = random.random()
                if (choice <= .5):
                    print("Slime loafed around!")
                else:
                    system.attack(self, target)
            case "Imp":
                # Imp has 25% chance of wasting turn, 20% chance performing 2-4 multihit attack, and 55% chance normal attack 
                choice = random.random()
                if (choice <= .25):
                    print("Imp cackled devilishly!")
                elif (choice <= .45):
                    reps = random.randint(2,4)
                    print(f"Imp pierces into Player {reps} times!")
                    for i in range (reps):
                        system.attack(self, target)
                else:
                    system.attack(self, target)
            case "Phantasm":
                # Imp has 20% chance of draining HP, 25% chance performing 2-4 multihit attack, 40% chance normal attack, and 15% wasting turn 
                choice = random.random()
                if (choice <= .2):
                    print("Phantasm drains into Player's soul!")
                    drain = self.atk + random.randint(self.level * 0,self.level * 2)
                    print(f"Phantasm drained {drain} HP!")
                    self.heal(drain)
                    target.health -= drain
                elif (choice <= .45):
                    reps = random.randint(2,4)
                    print(f"Imp pierces into Player {reps} times!")
                    for i in range (reps):
                        system.attack(self, target)
                elif (choice <= .85):
                    system.attack(self, target)
                else:
                    print("Phantasm floated about!")
            case "Straggler":
                # Straggler normally wastes turn 90% of the time, to account for their high strength
                choice = random.random()
                if (choice <= .9):
                    print("The Straggler relaxed and vibed!")
                else:
                    system.attack(self, target)
            case "Boss":
                # Boss has 10% chance of performing "charge attack", where the attack is temporarily boosted by
                # anywhere between 0-(atk/2) increased attack power, 15% chance of being "fired up", buffing attack,
                # 15% chance of healing 5-20 HP, and 60% chance of attacking normally.
                choice = random.random()
                if (choice <= .1):
                    print("Boss charges!")
                    temp = self.atk
                    self.atk = self.atk + random.randint(0, self.atk // 2)
                    system.attack(self, target)
                    self.atk = temp
                elif (choice <= .25):
                    atk_bonus = random.randint(5,10)
                    print(f"Boss is fired up!")
                    print(f"Boss's attack is raised by {atk_bonus}!")
                    self.atk += atk_bonus
                elif (choice <= .40):
                    print("Boss eats a banana!")
                    heal_amnt = random.randint(5,20)
                    self.heal(heal_amnt)
                    print(f"Boss heals {heal_amnt} HP!")
                else:
                    system.attack(self, target)  
                    